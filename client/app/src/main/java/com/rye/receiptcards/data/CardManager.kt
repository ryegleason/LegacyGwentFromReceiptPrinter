/*
 * Copyright (C) 2020 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.rye.receiptcards.data

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import com.rye.receiptcards.data.model.request
import com.rye.receiptcards.proto.Reqrep
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.util.*


/* Handles operations on cardLiveData and holds details about it. */
class CardManager {

    private val _cardForID = MutableLiveData<Map<UUID, Card>>()
    private val _deckCards = MutableLiveData<List<Card>>()
    private val _handCards = MutableLiveData<List<Card>>()
    private val _playedCards = MutableLiveData<List<Card>>()

    val deckCards: LiveData<List<Card>> = _deckCards
    val handCards: LiveData<List<Card>> = _deckCards
    val playedCards: LiveData<List<Card>> = _deckCards

    suspend fun draw(target: Reqrep.Zone) {
        val response = request(Reqrep.Req.newBuilder().setReqType(Reqrep.Req.ReqType.DRAW).setDrawTo(target))
        if (response is Result.Success) {
            processResponse(response.data)
        }
    }

    suspend fun moveCard(card: Card, source: Reqrep.Zone, destination: Reqrep.Zone, fromTop: Boolean = true, cardsDown: Int = 0) {
        val requestBuilder = Reqrep.Req.newBuilder()
        requestBuilder.reqType = Reqrep.Req.ReqType.MOVE
        requestBuilder.moveBuilder.cardUuid = UUIDToProtoUUID(card.id)
        requestBuilder.moveBuilder.sourceZone = source
        requestBuilder.moveBuilder.targetZone = destination
        requestBuilder.moveBuilder.fromTop = fromTop
        requestBuilder.moveBuilder.numDown = cardsDown
        val response = request(requestBuilder)
        if (response is Result.Success) {
            processResponse(response.data)
        }
    }

    suspend fun shuffle() {
        val response = request(Reqrep.Req.newBuilder().setReqType(Reqrep.Req.ReqType.SHUFFLE))
        if (response is Result.Success) {
            processResponse(response.data)
        }
    }

    suspend fun processResponse(response: Reqrep.Rep) {
        if (response.success) {
            // Add new cards
            if (response.newCards.imagesCount > 0) {

                // Load images (may be slow)
                val images = withContext(Dispatchers.Default) {
                    Array<Bitmap>(response.newCards.imagesCount) { index ->
                        return@Array response.newCards.getImages(index).let {
                            BitmapFactory.decodeByteArray(it.toByteArray(), 0, it.size())
                        }
                    }
                }

                val updatedMap = _cardForID.value?.toMutableMap() ?: mutableMapOf()

                for (index in 1..response.newCards.cardUuidsCount) {
                    val uuid = protoUUIDToUUID(response.newCards.getCardUuids(index))
                    val newCard = Card(uuid, images[response.newCards.getImageIndices(index)])
                    updatedMap[uuid] = newCard
                }

                _cardForID.postValue(updatedMap)
            }

            val updatedMap = _cardForID.value?.toMutableMap() ?: mutableMapOf()
            var updateMapFlag = false

            for (move in response.movesList) {
                val targetCard = getCardForId(protoUUIDToUUID(move.cardUuid))
                targetCard?.let {
                    val sourceList = zoneToList(move.sourceZone)
                    if (sourceList != null) {
                        removeCardFromAll(it, sourceList)
                    }

                    if (move.targetZone == Reqrep.Zone.NONE) {
                        updatedMap.remove(targetCard.id)
                        updateMapFlag = true
                    } else {
                        val targetList = zoneToList(move.targetZone)
                        if (targetList != null) {
                            addCard(targetCard, targetList)
                        }
                    }
                }
            }

            if (updateMapFlag) {
                _cardForID.postValue(updatedMap)
            }
        }
    }

    private fun zoneToList(zone: Reqrep.Zone) : MutableLiveData<List<Card>>? {
        return when (zone) {
            Reqrep.Zone.DECK -> {
                _deckCards
            }
            Reqrep.Zone.HAND -> {
                _handCards
            }
            Reqrep.Zone.PLAYED -> {
                _playedCards
            }
            else -> null
        }
    }

    private fun addCard(card: Card, cardList: MutableLiveData<List<Card>>) {
        val currentList = cardList.value
        if (currentList == null) {
            cardList.postValue(listOf(card))
        } else {
            val updatedList = currentList.toMutableList()
            updatedList.add(0, card)
            cardList.postValue(updatedList)
        }
    }

    private fun removeCardFromAll(card: Card, firstList: MutableLiveData<List<Card>>): Boolean {
        if (!removeCard(card, firstList)) {
            return when (firstList) {
                _deckCards -> {
                    removeCard(card, _handCards) || removeCard(card, _playedCards)
                }
                _handCards -> {
                    removeCard(card, _deckCards) || removeCard(card, _playedCards)
                }
                _playedCards -> {
                    removeCard(card, _handCards) || removeCard(card, _deckCards)
                }
                else -> {
                    removeCard(card, _handCards) || removeCard(card, _deckCards) || removeCard(card, _playedCards)
                }
            }
        }
        return true
    }

    private fun removeCard(card: Card, cardList: MutableLiveData<List<Card>>): Boolean {
        val currentList = cardList.value
        if (currentList != null) {
            val updatedList = currentList.toMutableList()
            if (updatedList.remove(card)) {
                cardList.postValue(updatedList)
                return true
            }
        }
        return false
    }

    /* Returns card given an ID. */
    fun getCardForId(id: UUID): Card? {
        return _cardForID.value?.get(id)
    }


    companion object {
        private var INSTANCE: CardManager? = null

        fun getDataSource(): CardManager {
            return synchronized(CardManager::class) {
                val newInstance = INSTANCE ?: CardManager()
                INSTANCE = newInstance
                newInstance
            }
        }
    }
}
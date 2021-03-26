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

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import com.rye.receiptcards.data.model.request
import com.rye.receiptcards.proto.Reqrep
import java.util.*


/* Handles operations on cardLiveData and holds details about it. */
class CardManager {

    private val _cardForID = MutableLiveData<Map<UUID, Card>>()
    private val _deckCards = MutableLiveData<List<Card>>()
    private val _handCards = MutableLiveData<List<Card>>()
    private val _playedCards = MutableLiveData<List<Card>>()

    val deckCards: LiveData<List<Card>> = _deckCards
    val handCards: LiveData<List<Card>> = _handCards
    val playedCards: LiveData<List<Card>> = _playedCards

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

    fun processResponse(response: Reqrep.Rep) {
        if (response.success) {
            // Add new cards
            val updatedMap = _cardForID.value?.toMutableMap() ?: mutableMapOf()
            val updatedDeck = _deckCards.value?.toMutableList() ?: mutableListOf()
            val updatedHand = _handCards.value?.toMutableList() ?: mutableListOf()
            val updatedPlayed = _playedCards.value?.toMutableList() ?: mutableListOf()

            if (response.newCards.imageUrisCount > 0) {

                for (index in 1 until response.newCards.cardUuidsCount) {
                    val uuid = protoUUIDToUUID(response.newCards.getCardUuids(index))
                    val newCard = Card(uuid, response.newCards.getImageUris(response.newCards.getImageIndices(index)))
                    updatedMap[uuid] = newCard
                }
            }

            for (move in response.movesList) {
                val targetCard = updatedMap[protoUUIDToUUID(move.cardUuid)]
                targetCard?.let {
                    if (move.sourceZone != Reqrep.Zone.NONE) {
                        updatedDeck.remove(targetCard)
                        updatedHand.remove(targetCard)
                        updatedPlayed.remove(targetCard)
                    }

                    when (move.targetZone!!) {
                        Reqrep.Zone.NONE -> {
                            updatedMap.remove(targetCard.id)
                        }
                        Reqrep.Zone.DECK -> {
                            updatedDeck.add(targetCard)
                        }
                        Reqrep.Zone.HAND -> {
                            updatedHand.add(targetCard)
                        }
                        Reqrep.Zone.PLAYED -> {
                            updatedPlayed.add(targetCard)
                        }
                        Reqrep.Zone.UNRECOGNIZED -> {
                            // Do nothing
                        }
                    }
                }
            }

            _cardForID.postValue(updatedMap)
            _deckCards.postValue(updatedDeck)
            _handCards.postValue(updatedHand)
            _playedCards.postValue(updatedPlayed)
        }
    }

    /* Returns card given an ID. */
    fun getCardForId(id: UUID): Card? {
        return _cardForID.value?.get(id)
    }

    fun reset() {
        println("Reset called")
        _cardForID.value = mapOf()
        _deckCards.value = listOf()
        _handCards.value = listOf()
        _playedCards.value = listOf()
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
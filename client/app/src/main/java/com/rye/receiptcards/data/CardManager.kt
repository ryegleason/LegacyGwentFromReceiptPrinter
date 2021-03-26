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
import com.rye.receiptcards.proto.Reqrep
import java.util.*


/* Handles operations on cardLiveData and holds details about it. */
class CardManager {

    private val _cardForID = MutableLiveData<Map<UUID, Card>>()
    private val _deckCards = MutableLiveData<List<Card>>()
    private val _handCards = MutableLiveData<List<Card>>()
    private val _playedCards = MutableLiveData<List<Card>>()

    val cardForID: LiveData<Map<UUID, Card>> = _cardForID
    val deckCards: LiveData<List<Card>> = _deckCards
    val handCards: LiveData<List<Card>> = _deckCards
    val playedCards: LiveData<List<Card>> = _deckCards

    fun draw(target: Reqrep.Zone) {
        val currentList = _deckCards.value
        if (currentList != null && currentList.isNotEmpty()) {
            moveCard(currentList[0], Reqrep.Zone.DECK, Reqrep.Zone.HAND)
        }
    }

    fun moveCard(card: Card, source: Reqrep.Zone, destination: Reqrep.Zone, fromTop: Boolean = true, cardsDown: Int = 0) : Boolean {
        if (source == destination) {
            return true
        }

        return if (removeCard(card, zoneToList(source))) {
            addCard(card, zoneToList(destination))
            true
        } else {
            false
        }
    }

    fun shuffle() {
        TODO("Implement")
    }

    private fun zoneToList(zone: Reqrep.Zone) : MutableLiveData<List<Card>> {
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
            else -> MutableLiveData<List<Card>>()
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
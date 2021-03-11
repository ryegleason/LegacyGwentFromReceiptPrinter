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

package com.example.recyclersample.data

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData

enum class Zone {
    DECK,HAND,PLAYED
}

/* Handles operations on cardLiveData and holds details about it. */
class DataSource {
    private val initialCardList = flowerList()
    private val deckCards = MutableLiveData(initialCardList)
    private val handCards = MutableLiveData<List<Card>>()
    private val playedCards = MutableLiveData<List<Card>>()

    fun drawCard() {
        val currentList = deckCards.value
        if (currentList != null && currentList.isNotEmpty()) {
            moveCard(currentList[0], Zone.DECK, Zone.HAND)
        }
    }

    fun moveCard(card: Card, source: Zone, destination: Zone) : Boolean {
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

    private fun zoneToList(zone: Zone) : MutableLiveData<List<Card>> {
        return when (zone) {
            Zone.DECK -> {
                deckCards;
            }
            Zone.HAND -> {
                handCards;
            }
            Zone.PLAYED -> {
                playedCards;
            }
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
    fun getCardForId(id: Long): Card? {
        initialCardList.let { flowers ->
            return flowers.firstOrNull{ it.id == id}
        }
    }

    fun getDeck(): LiveData<List<Card>> {
        return deckCards
    }

    fun getHand(): LiveData<List<Card>> {
        return handCards
    }

    fun getPlayed(): LiveData<List<Card>> {
        return playedCards
    }

    /* Returns a random flower asset for flowers that are added. */
    fun getRandomFlowerImageAsset(): Int? {
        val randomNumber = (initialCardList.indices).random()
        return initialCardList[randomNumber].image
    }

    companion object {
        private var INSTANCE: DataSource? = null

        fun getDataSource(): DataSource {
            return synchronized(DataSource::class) {
                val newInstance = INSTANCE ?: DataSource()
                INSTANCE = newInstance
                newInstance
            }
        }
    }
}
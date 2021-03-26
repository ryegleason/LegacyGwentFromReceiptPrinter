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

package com.rye.receiptcards.cardDetail

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.rye.receiptcards.data.CardManager
import com.rye.receiptcards.data.Card
import com.rye.receiptcards.proto.Reqrep
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
import java.util.*

class CardDetailViewModel(private val cardManager: CardManager) : ViewModel() {

    fun getDeckSize() : Int {
        return cardManager.deckCards.value?.size ?: 0
    }

    /* Queries datasource to returns a card that corresponds to an id. */
    fun getCardForId(id: UUID) : Card? {
        return cardManager.getCardForId(id)
    }

    fun moveCard(card: Card, sourceZone: Reqrep.Zone, targetZone: Reqrep.Zone, fromTop: Boolean = true, cardsDown: Int = 0) {
        GlobalScope.launch {
            cardManager.moveCard(card, sourceZone, targetZone, fromTop, cardsDown)
        }
    }
}

class CardDetailViewModelFactory : ViewModelProvider.Factory {

    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(CardDetailViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return CardDetailViewModel(
                cardManager = CardManager.getDataSource()
            ) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}
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

package com.rye.receiptcards.handDetail

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.rye.receiptcards.data.DataSource
import com.rye.receiptcards.data.Card
import com.rye.receiptcards.data.Zone
import java.util.*

class HandDetailViewModel(private val datasource: DataSource) : ViewModel() {

    /* Queries datasource to returns a flower that corresponds to an id. */
    fun getCardForId(id: UUID) : Card? {
        return datasource.getCardForId(id)
    }

    fun playCard(card: Card) {
        datasource.moveCard(card, Zone.HAND, Zone.PLAYED)
    }

    fun putInDeck(card: Card) {
        datasource.moveCard(card, Zone.HAND, Zone.DECK)
    }

}

class HandDetailViewModelFactory : ViewModelProvider.Factory {

    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(HandDetailViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return HandDetailViewModel(
                datasource = DataSource.getDataSource()
            ) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}
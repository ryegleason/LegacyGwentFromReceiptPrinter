package com.rye.receiptcards.deckselect

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider

class DeckSelectViewModelFactory : ViewModelProvider.Factory {

    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(DeckSelectViewModel::class.java)) {
            return DeckSelectViewModel() as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}
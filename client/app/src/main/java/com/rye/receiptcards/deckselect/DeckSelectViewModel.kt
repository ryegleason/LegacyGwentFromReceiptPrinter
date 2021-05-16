package com.rye.receiptcards.deckselect

import androidx.lifecycle.*
import com.rye.receiptcards.proto.Reqrep
import kotlinx.coroutines.launch
import com.rye.receiptcards.data.Result
import com.rye.receiptcards.data.model.request

class DeckSelectViewModel : ViewModel() {

    private val _cardsResult = MutableLiveData<Reqrep.Rep>()
    val cardsResult: LiveData<Reqrep.Rep> = _cardsResult

    fun getDeckCards(deckIndex: Int) {
        viewModelScope.launch {
            val requestBuilder = Reqrep.Req.newBuilder()
            requestBuilder.reqType = Reqrep.Req.ReqType.SELECT_DECK
            requestBuilder.deckIndex = deckIndex
            val result = request(requestBuilder)

            if (result is Result.Success) {
                _cardsResult.value = result.data
            } else {
                println(result.toString())
                _cardsResult.value = Reqrep.Rep.newBuilder().setSuccess(false).build()
            }
        }
    }

    fun resume() {
        viewModelScope.launch {
            val result = request(Reqrep.Req.newBuilder().setReqType(Reqrep.Req.ReqType.RESUME))
            if (result is Result.Success) {
                _cardsResult.value = result.data
            } else {
                println(result.toString())
                _cardsResult.value = Reqrep.Rep.newBuilder().setSuccess(false).build()
            }
        }
    }
}

class DeckSelectViewModelFactory : ViewModelProvider.Factory {

    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(DeckSelectViewModel::class.java)) {
            return DeckSelectViewModel() as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}
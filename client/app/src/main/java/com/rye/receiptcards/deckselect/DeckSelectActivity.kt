package com.rye.receiptcards.deckselect

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View
import android.widget.*
import android.widget.AdapterView.OnItemSelectedListener
import androidx.lifecycle.Observer
import androidx.lifecycle.ViewModelProvider
import com.rye.receiptcards.R
import com.rye.receiptcards.proto.Reqrep
import com.rye.receiptcards.ui.login.EXTRA_DECKS_INFO

class DeckSelectActivity() : AppCompatActivity() {

    private lateinit var deckSelectViewModel: DeckSelectViewModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_deck_select)

        val games = ArrayList<String>()
        val allDecks = ArrayList<String>()
        val decksForGame = HashMap<String, MutableList<String>>()

        for (deck in Reqrep.DecksInfo.parseFrom(intent.getByteArrayExtra(EXTRA_DECKS_INFO)).decksList) {
            allDecks.add(deck.name)
            if (deck.game in decksForGame.keys) {
                decksForGame[deck.game]!!.add(deck.name)
            } else {
                games.add(deck.game)
                decksForGame[deck.game] = mutableListOf(deck.name)
            }
        }

        val gameChooser = findViewById<Spinner>(R.id.gameChooser)
        val deckChooser = findViewById<Spinner>(R.id.deckChooser)
        val beginButton = findViewById<Button>(R.id.begin)
        val loadBar = findViewById<ProgressBar>(R.id.loadBar)

        deckSelectViewModel = ViewModelProvider(this, DeckSelectViewModelFactory())
            .get(DeckSelectViewModel::class.java)

        gameChooser.adapter = ArrayAdapter(this, android.R.layout.simple_spinner_dropdown_item, games)

        gameChooser.onItemSelectedListener = object: OnItemSelectedListener{
            override fun onItemSelected(
                parent: AdapterView<*>?,
                view: View?,
                position: Int,
                id: Long
            ) {
                deckChooser.adapter = ArrayAdapter(this@DeckSelectActivity,
                    android.R.layout.simple_spinner_dropdown_item,
                    decksForGame[parent!!.getItemAtPosition(position)]!!)
            }

            override fun onNothingSelected(parent: AdapterView<*>?) {
                deckChooser.adapter = ArrayAdapter(this@DeckSelectActivity,
                android.R.layout.simple_spinner_dropdown_item,
                allDecks)
            }
        }

        deckChooser.onItemSelectedListener = object: OnItemSelectedListener {
            override fun onItemSelected(
                parent: AdapterView<*>?,
                view: View?,
                position: Int,
                id: Long
            ) {
                beginButton.isEnabled = true
            }

            override fun onNothingSelected(parent: AdapterView<*>?) {
                beginButton.isEnabled = false
            }

        }

        beginButton.setOnClickListener {
            loadBar.visibility = View.VISIBLE
            beginButton.isEnabled = false
            deckSelectViewModel.getDeckCards(allDecks.indexOf(deckChooser.selectedItem))
        }

        deckSelectViewModel.cardsResult.observe(this@DeckSelectActivity, Observer {
            val loginResult = it ?: return@Observer

            loadBar.visibility = View.GONE
            if (!loginResult.success) {
                showFetchFailed()
            } else {
                // TODO put something here
                Toast.makeText(applicationContext, "Deck get!", Toast.LENGTH_SHORT).show()
            }
        })
    }

    private fun showFetchFailed(){
        Toast.makeText(applicationContext, "Deck download failed", Toast.LENGTH_SHORT).show()
    }
}
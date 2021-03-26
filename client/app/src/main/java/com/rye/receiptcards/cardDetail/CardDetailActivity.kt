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

import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.ImageView
import android.widget.NumberPicker
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import com.rye.receiptcards.R
import com.rye.receiptcards.proto.Reqrep
import java.util.*

const val CARD_ID = "com.rye.receiptcards.CARD_ID"
const val FROM_ZONE = "com.rye.receiptcards.FROM_ZONE"

class CardDetailActivity : AppCompatActivity() {

    private val cardDetailViewModel by viewModels<CardDetailViewModel> {
        CardDetailViewModelFactory()
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.card_detail_activity)

        var currentCardId: UUID? = null
        var fromZone: Reqrep.Zone? = null

        /* Connect variables to UI elements. */
        val cardImage: ImageView = findViewById(R.id.card_detail_image)
        val playButton: Button = findViewById(R.id.play_button)
        val handButton: Button = findViewById(R.id.hand_button)
        val topButton: Button = findViewById(R.id.top_button)
        val bottomButton: Button = findViewById(R.id.bottom_button)
        val numberPicker: NumberPicker = findViewById(R.id.cards_in_picker);

        numberPicker.minValue = 0
        numberPicker.maxValue = cardDetailViewModel.getDeckSize()
        numberPicker.wrapSelectorWheel = false

        val bundle: Bundle? = intent.extras
        if (bundle != null) {
            currentCardId = bundle.get(CARD_ID) as UUID?
            fromZone = bundle.get(FROM_ZONE) as Reqrep.Zone?
        }

        when (fromZone) {
            Reqrep.Zone.HAND -> {
                handButton.isEnabled = false
                handButton.visibility = View.GONE
            }
            Reqrep.Zone.PLAYED -> {
                playButton.isEnabled = false
                playButton.visibility = View.GONE
            }
            Reqrep.Zone.DECK -> {
                topButton.isEnabled = false
                bottomButton.isEnabled = false
                topButton.visibility = View.GONE
                bottomButton.visibility = View.GONE
                numberPicker.visibility = View.GONE
            }
        }

        /* If currentCardId is not null, get corresponding card and set name, image and
        description */
        currentCardId?.let {
            val currentCard = cardDetailViewModel.getCardForId(it)
            if (currentCard?.image == null) {
                cardImage.setImageResource(R.drawable.ire)
            } else {
                cardImage.setImageBitmap(currentCard.image)
            }

            playButton.setOnClickListener {
                if (currentCard != null && fromZone != null) {
                    cardDetailViewModel.moveCard(currentCard, fromZone, Reqrep.Zone.PLAYED)
                }
                finish()
            }

            handButton.setOnClickListener {
                if (currentCard != null && fromZone != null) {
                    cardDetailViewModel.moveCard(currentCard, fromZone, Reqrep.Zone.HAND)
                }
                finish()
            }

            topButton.setOnClickListener {
                if (currentCard != null && fromZone != null) {
                    cardDetailViewModel.moveCard(currentCard, fromZone, Reqrep.Zone.DECK, fromTop = true, cardsDown = numberPicker.value)
                }
                finish()
            }

            bottomButton.setOnClickListener {
                if (currentCard != null && fromZone != null) {
                    cardDetailViewModel.moveCard(currentCard, fromZone, Reqrep.Zone.DECK, fromTop = false, cardsDown = numberPicker.value)
                }
                finish()
            }
        }


    }
}
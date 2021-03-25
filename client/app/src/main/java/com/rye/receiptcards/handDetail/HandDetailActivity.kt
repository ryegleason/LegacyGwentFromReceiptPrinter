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

import android.os.Bundle
import android.widget.Button
import android.widget.ImageView
import android.widget.NumberPicker
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import com.rye.receiptcards.R
import com.rye.receiptcards.cardList.CARD_ID
import java.util.*

class HandDetailActivity : AppCompatActivity() {

    private val flowerDetailViewModel by viewModels<HandDetailViewModel> {
        HandDetailViewModelFactory()
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.hand_detail_activity)

        var currentFlowerId: UUID? = null

        /* Connect variables to UI elements. */
        val flowerImage: ImageView = findViewById(R.id.flower_detail_image)
        val playButton: Button = findViewById(R.id.play_button)
        val topButton: Button = findViewById(R.id.top_button)
        val bottomButton: Button = findViewById(R.id.bottom_button)
        val numberPicker: NumberPicker = findViewById(R.id.cards_in_picker);

        numberPicker.minValue = 0;
        numberPicker.maxValue = 60;
        numberPicker.wrapSelectorWheel = false;

        val bundle: Bundle? = intent.extras
        if (bundle != null) {
            currentFlowerId = bundle.get(CARD_ID) as UUID?
        }

        /* If currentFlowerId is not null, get corresponding flower and set name, image and
        description */
        currentFlowerId?.let {
            val currentFlower = flowerDetailViewModel.getCardForId(it)
            if (currentFlower?.image == null) {
                flowerImage.setImageResource(R.drawable.ire)
            } else {
                flowerImage.setImageResource(currentFlower.image)
            }

            playButton.setOnClickListener {
                if (currentFlower != null) {
                    flowerDetailViewModel.playCard(currentFlower)
                }
                finish()
            }

            topButton.setOnClickListener {
                if (currentFlower != null) {
                    flowerDetailViewModel.putInDeck(currentFlower)
                }
                finish()
            }

            bottomButton.setOnClickListener {
                if (currentFlower != null) {
                    flowerDetailViewModel.putInDeck(currentFlower)
                }
                finish()
            }
        }

    }
}
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

package com.example.recyclersample.cardList

import android.app.Activity
import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.recyclerview.widget.RecyclerView
import com.example.recyclersample.addFlower.AddFlowerActivity
import com.example.recyclersample.flowerDetail.FlowerDetailActivity
import com.example.recyclersample.R
import com.example.recyclersample.addFlower.CARD_NAME
import com.example.recyclersample.data.Card

const val CARD_ID = "card id"

class HandFragment : Fragment() {
    private val newFlowerActivityRequestCode = 1
    private val handViewModel by viewModels<HandViewModel> {
        HandViewModelFactory()
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        super.onCreate(savedInstanceState)
//        setContentView(R.layout.fragment_hand)
        val root = inflater.inflate(R.layout.fragment_hand, container, false)

        /* Instantiates headerAdapter and flowersAdapter. Both adapters are added to concatAdapter.
        which displays the contents sequentially */
        val flowersAdapter = CardsAdapter { flower -> adapterOnClick(flower) }

        val recyclerView: RecyclerView = root.findViewById(R.id.recycler_view)
        recyclerView.adapter = flowersAdapter

        handViewModel.flowersLiveData.observe(viewLifecycleOwner, {
            it?.let {
                flowersAdapter.submitList(it as MutableList<Card>)
            }
        })

        val draw: View = root.findViewById(R.id.draw)
        draw.setOnClickListener {
            drawOnClick()
        }

        return root
    }

    /* Opens FlowerDetailActivity when RecyclerView item is clicked. */
    private fun adapterOnClick(card: Card) {
        val intent = Intent(context, FlowerDetailActivity()::class.java)
        intent.putExtra(CARD_ID, card.id)
        startActivity(intent)
    }

    /* Adds flower to flowerList when FAB is clicked. */
    private fun drawOnClick() {
        val intent = Intent(context, AddFlowerActivity::class.java)
        startActivityForResult(intent, newFlowerActivityRequestCode)
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, intentData: Intent?) {
        super.onActivityResult(requestCode, resultCode, intentData)

        /* Inserts flower into viewModel. */
        if (requestCode == newFlowerActivityRequestCode && resultCode == Activity.RESULT_OK) {
            intentData?.let { data ->
                val flowerName = data.getStringExtra(CARD_NAME)

                handViewModel.insertFlower(flowerName)
            }
        }
    }
}
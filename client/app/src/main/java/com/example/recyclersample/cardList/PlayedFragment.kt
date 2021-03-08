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

import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.recyclerview.widget.RecyclerView
import com.example.recyclersample.flowerDetail.FlowerDetailActivity
import com.example.recyclersample.R
import com.example.recyclersample.data.Card

class PlayedFragment : Fragment() {
    private val playedViewModel by viewModels<PlayedViewModel> {
        PlayedViewModelFactory()
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        super.onCreate(savedInstanceState)
        val root = inflater.inflate(R.layout.fragment_played, container, false)

        /* Instantiates headerAdapter and flowersAdapter. Both adapters are added to concatAdapter.
        which displays the contents sequentially */
        val flowersAdapter = CardsAdapter { flower -> adapterOnClick(flower) }

        val recyclerView: RecyclerView = root.findViewById(R.id.recycler_view)
        recyclerView.adapter = flowersAdapter

        playedViewModel.flowersLiveData.observe(viewLifecycleOwner, {
            it?.let {
                flowersAdapter.submitList(it as MutableList<Card>)
            }
        })

        return root
    }

    /* Opens FlowerDetailActivity when RecyclerView item is clicked. */
    private fun adapterOnClick(card: Card) {
        val intent = Intent(context, FlowerDetailActivity()::class.java)
        intent.putExtra(CARD_ID, card.id)
        startActivity(intent)
    }
}
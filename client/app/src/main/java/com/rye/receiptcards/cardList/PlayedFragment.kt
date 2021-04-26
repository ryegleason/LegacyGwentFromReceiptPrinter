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

package com.rye.receiptcards.cardList

import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.floatingactionbutton.FloatingActionButton
import com.rye.receiptcards.R
import com.rye.receiptcards.cardDetail.CARD_ID
import com.rye.receiptcards.cardDetail.CardDetailActivity
import com.rye.receiptcards.cardDetail.FROM_ZONE
import com.rye.receiptcards.data.Card
import com.rye.receiptcards.proto.Reqrep

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

        val cardsAdapter = CardsAdapter { card -> adapterOnClick(card) }

        val recyclerView: RecyclerView = root.findViewById(R.id.recycler_view)
        val drawToPlay: FloatingActionButton = root.findViewById(R.id.draw_to_play)

        recyclerView.adapter = cardsAdapter

        playedViewModel.played.observe(viewLifecycleOwner, {
            it?.let {
                cardsAdapter.submitList(it as MutableList<Card>)
            }
        })

        drawToPlay.setOnClickListener {
            drawToPlayOnClick()
        }

        return root
    }

    /* Opens CardDetailActivity when RecyclerView item is clicked. */
    private fun adapterOnClick(card: Card) {
        val intent = Intent(context, CardDetailActivity()::class.java)
        intent.putExtra(CARD_ID, card.id)
        intent.putExtra(FROM_ZONE, Reqrep.Zone.PLAYED)
        startActivity(intent)
    }

    private fun drawToPlayOnClick() {
        playedViewModel.drawToPlay()
    }
}
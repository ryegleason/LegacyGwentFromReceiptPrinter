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

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.rye.receiptcards.R
import com.rye.receiptcards.data.Card

class CardsAdapter(private val onClick: (Card) -> Unit) :
    ListAdapter<Card, CardsAdapter.CardViewHolder>(CardDiffCallback) {

    private lateinit var parent: ViewGroup

    /* ViewHolder for Card, takes in the inflated view and the onClick behavior. */
    class CardViewHolder(itemView: View, val onClick: (Card) -> Unit) :
        RecyclerView.ViewHolder(itemView) {
        val cardImageView: ImageView = itemView.findViewById(R.id.card_image)
        private var currentCard: Card? = null

        init {
            itemView.setOnClickListener {
                currentCard?.let {
                    onClick(it)
                }
            }
        }

        /* Bind card name and image. */
        fun bind(card: Card) {
            currentCard = card
        }
    }

    /* Creates and inflates view and return CardViewHolder. */
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): CardViewHolder {
        this.parent = parent
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.card_item, parent, false)
        return CardViewHolder(view, onClick)
    }

    /* Gets current flower and uses it to bind view. */
    override fun onBindViewHolder(holder: CardViewHolder, position: Int) {
        val card = getItem(position)
        holder.bind(card)
        Glide.with(parent.rootView).load(card.imageURI).placeholder(R.drawable.placeholder).into(holder.cardImageView)
    }
}

object CardDiffCallback : DiffUtil.ItemCallback<Card>() {
    override fun areItemsTheSame(oldItem: Card, newItem: Card): Boolean {
        return oldItem == newItem
    }

    override fun areContentsTheSame(oldItem: Card, newItem: Card): Boolean {
        return oldItem.id == newItem.id
    }
}
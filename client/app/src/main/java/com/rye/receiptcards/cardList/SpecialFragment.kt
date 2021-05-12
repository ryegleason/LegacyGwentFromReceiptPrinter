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
import android.opengl.Visibility
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.LinearLayout
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import com.rye.receiptcards.R
import com.rye.receiptcards.cardDetail.CARD_ID
import com.rye.receiptcards.cardDetail.CardDetailActivity
import com.rye.receiptcards.cardDetail.FROM_ZONE
import com.rye.receiptcards.proto.Reqrep
import com.rye.receiptcards.shop.ShopActivity

class SpecialFragment : Fragment() {
    private val specialViewModel by viewModels<SpecialViewModel> {
        SpecialViewModelFactory()
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        super.onCreate(savedInstanceState)
        val root = inflater.inflate(R.layout.fragment_special, container, false)

        val sideboardButton: Button = root.findViewById(R.id.sideboard_button)
        val creepButton: Button = root.findViewById(R.id.creep_button)
        val randArrowButton: Button = root.findViewById(R.id.rand_arrow_button)
        val leftArrowButton: Button = root.findViewById(R.id.left_arrow_button)
        val forwardArrowButton: Button = root.findViewById(R.id.forward_arrow_button)
        val rightArrowButton: Button = root.findViewById(R.id.right_arrow_button)
        val shopNoHoldButton: Button = root.findViewById(R.id.shop_no_hold_button)
        val shopHoldButton: Button = root.findViewById(R.id.shop_hold_button)

        specialViewModel.specialActions.observe(viewLifecycleOwner, {
            it?.let {
                setVisibleIffContains(sideboardButton, Reqrep.SpecialAction.SIDEBOARD, it)
                setVisibleIffContains(creepButton, Reqrep.SpecialAction.CREEP, it)
                setVisibleIffContains(randArrowButton, Reqrep.SpecialAction.RAND_ARROW, it)
                setVisibleIffContains(leftArrowButton, Reqrep.SpecialAction.LEFT_ARROW, it)
                setVisibleIffContains(forwardArrowButton, Reqrep.SpecialAction.FORWARD_ARROW, it)
                setVisibleIffContains(rightArrowButton, Reqrep.SpecialAction.RIGHT_ARROW, it)
                setVisibleIffContains(shopNoHoldButton, Reqrep.SpecialAction.SHOP_NO_HOLD, it)
                setVisibleIffContains(shopHoldButton, Reqrep.SpecialAction.SHOP_HOLD, it)
            }
        })

        creepButton.setOnClickListener {
            specialViewModel.doSpecialAction(Reqrep.SpecialAction.CREEP)
        }

        randArrowButton.setOnClickListener {
            specialViewModel.doSpecialAction(Reqrep.SpecialAction.RAND_ARROW)
        }

        leftArrowButton.setOnClickListener {
            specialViewModel.doSpecialAction(Reqrep.SpecialAction.LEFT_ARROW)
        }

        forwardArrowButton.setOnClickListener {
            specialViewModel.doSpecialAction(Reqrep.SpecialAction.FORWARD_ARROW)
        }

        rightArrowButton.setOnClickListener {
            specialViewModel.doSpecialAction(Reqrep.SpecialAction.RIGHT_ARROW)
        }

        shopNoHoldButton.setOnClickListener {
            specialViewModel.doSpecialAction(Reqrep.SpecialAction.SHOP_NO_HOLD)
            val intent = Intent(context, ShopActivity()::class.java)
            startActivity(intent)
        }

        shopHoldButton.setOnClickListener {
            specialViewModel.doSpecialAction(Reqrep.SpecialAction.SHOP_HOLD)
            val intent = Intent(context, ShopActivity()::class.java)
            startActivity(intent)
        }


        return root
    }

    private fun setVisibleIffContains(view: View, specialAction: Reqrep.SpecialAction, set: Set<Reqrep.SpecialAction>) {
        if (set.contains(specialAction)) {
            view.visibility = View.VISIBLE
        } else {
            view.visibility = View.GONE
        }
    }
}
package com.rye.receiptcards.shop

import android.content.Intent
import android.os.Bundle
import android.widget.ImageView
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.Observer
import androidx.lifecycle.ViewModelProvider
import com.bumptech.glide.Glide
import com.rye.receiptcards.R
import com.rye.receiptcards.cardDetail.CARD_ID
import com.rye.receiptcards.cardDetail.CardDetailActivity
import com.rye.receiptcards.cardDetail.FROM_ZONE
import com.rye.receiptcards.data.Card
import com.rye.receiptcards.proto.Reqrep

class ShopActivity : AppCompatActivity() {

    private lateinit var shopActivityViewModel: ShopActivityViewModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_shop)

        val secretShop = findViewById<ImageView>(R.id.secret_shop_image)
        val itemDeck = findViewById<ImageView>(R.id.item_deck_image)
        val consumable = findViewById<ImageView>(R.id.consumable_image)

        shopActivityViewModel = ViewModelProvider(this, ShopActivityViewModelFactory())
            .get(ShopActivityViewModel::class.java)

        shopActivityViewModel.shopCards.observe(this@ShopActivity, Observer {
            var shopCards = it ?: listOf<Card?>(null, null, null)
            if (shopCards.size != 3) {
                shopCards = listOf<Card?>(null, null, null)
            }

            val secretShopCard = shopCards[0]
            val itemDeckCard = shopCards[1]
            val consumableCard = shopCards[2]
            if (secretShopCard != null) {
                Glide.with(this).load(secretShopCard.imageURI).placeholder(R.drawable.placeholder).into(secretShop)
                secretShop.setOnClickListener {
                    cardOnClick(secretShopCard)
                }
            } else {
                secretShop.setImageResource(R.drawable.sold_out)
                secretShop.setOnClickListener(null)
            }

            if (itemDeckCard != null) {
                Glide.with(this).load(itemDeckCard.imageURI).placeholder(R.drawable.placeholder).into(itemDeck)
                itemDeck.setOnClickListener {
                    cardOnClick(itemDeckCard)
                }
            } else {
                itemDeck.setImageResource(R.drawable.sold_out)
                itemDeck.setOnClickListener(null)
            }

            if (consumableCard != null) {
                Glide.with(this).load(consumableCard.imageURI).placeholder(R.drawable.placeholder).into(consumable)
                consumable.setOnClickListener {
                    cardOnClick(consumableCard)
                }
            } else {
                consumable.setImageResource(R.drawable.sold_out)
                consumable.setOnClickListener(null)
            }
        })
    }

    /* Opens CardDetailActivity when card is clicked. */
    private fun cardOnClick(card: Card) {
        val intent = Intent(this, CardDetailActivity()::class.java)
        intent.putExtra(CARD_ID, card.id)
        intent.putExtra(FROM_ZONE, Reqrep.Zone.SPECIAL)
        startActivity(intent)
    }
}
package com.rye.receiptcards

import android.os.Bundle
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.fragment.app.viewModels
import androidx.navigation.findNavController
import androidx.navigation.ui.AppBarConfiguration
import androidx.navigation.ui.setupWithNavController
import com.google.android.material.bottomnavigation.BottomNavigationView
import com.rye.receiptcards.cardList.DeckViewModel
import com.rye.receiptcards.cardList.DeckViewModelFactory
import com.rye.receiptcards.data.CardManager
import com.rye.receiptcards.deckselect.EXTRA_DECK_RESPONSE
import com.rye.receiptcards.proto.Reqrep
import com.rye.receiptcards.ui.login.EXTRA_DECKS_INFO


class MainActivity : AppCompatActivity() {

    private val mainViewModel by viewModels<MainViewModel> {
        MainViewModelFactory()
    }
    private lateinit var navView : BottomNavigationView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)


        mainViewModel.processResponse(Reqrep.Rep.parseFrom(intent.getByteArrayExtra(EXTRA_DECK_RESPONSE)))

        navView = findViewById(R.id.nav_view)

//        val navHostFragment = supportFragmentManager.findFragmentById(R.id.nav_host_fragment) as NavHostFragment
//        val navController = navHostFragment.navController
        val navController = findNavController(R.id.nav_host_fragment)
        // Passing each menu ID as a set of Ids because each
        // menu should be considered as top level destinations.
        val appBarConfiguration = AppBarConfiguration(
            setOf(
                R.id.navigation_deck, R.id.navigation_hand, R.id.navigation_played
            )
        )
//        setupActionBarWithNavController(navController, appBarConfiguration)
        navView.setupWithNavController(navController)
    }
}
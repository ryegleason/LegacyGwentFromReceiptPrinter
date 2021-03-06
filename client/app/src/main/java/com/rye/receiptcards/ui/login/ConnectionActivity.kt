package com.rye.receiptcards.ui.login

import android.app.Activity
import android.content.Intent
import androidx.lifecycle.Observer
import androidx.lifecycle.ViewModelProvider
import android.os.Bundle
import androidx.annotation.StringRes
import androidx.appcompat.app.AppCompatActivity
import android.text.Editable
import android.text.TextWatcher
import android.view.View
import android.view.inputmethod.EditorInfo
import android.widget.Button
import android.widget.EditText
import android.widget.ProgressBar
import android.widget.Toast
import androidx.preference.PreferenceManager

import com.rye.receiptcards.R
import com.rye.receiptcards.data.model.setUUID
import com.rye.receiptcards.deckselect.DeckSelectActivity
import java.util.*

const val EXTRA_DECKS_INFO = "com.rye.receiptcards.DECKS_INFO"


class ConnectionActivity : AppCompatActivity() {

    private lateinit var loginViewModel: LoginViewModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContentView(R.layout.activity_connection)
        val sharedPreferences = PreferenceManager.getDefaultSharedPreferences(this /* Activity context */)
        val savedUUID = sharedPreferences.getString(getString(R.string.saved_uuid_key), "")
        if (savedUUID != "") {
            setUUID(UUID.fromString(savedUUID))
        } else {
            val newUUID = UUID.randomUUID()
            setUUID(newUUID)
            with (sharedPreferences.edit()) {
                putString(getString(R.string.saved_uuid_key), newUUID.toString())
                apply()
            }
        }

        val ip = findViewById<EditText>(R.id.ip)
        val port = findViewById<EditText>(R.id.port)
        val login = findViewById<Button>(R.id.login)
        val loading = findViewById<ProgressBar>(R.id.loading)

        loginViewModel = ViewModelProvider(this, LoginViewModelFactory())
            .get(LoginViewModel::class.java)

        loginViewModel.loginFormState.observe(this@ConnectionActivity, Observer {
            val loginState = it ?: return@Observer

            // disable login button unless both username / password is valid
            login.isEnabled = loginState.isDataValid

            if (loginState.ipError != null) {
                ip.error = getString(loginState.ipError)
            }
            if (loginState.portError != null) {
                port.error = getString(loginState.portError)
            }
        })

        loginViewModel.loginResult.observe(this@ConnectionActivity, Observer {
            val loginResult = it ?: return@Observer

            loading.visibility = View.GONE
            if (loginResult.error != null) {
                showLoginFailed(loginResult.error)
            }
            if (loginResult.success == true) {
                with (sharedPreferences.edit()) {
                    putString(getString(R.string.saved_ip_key), ip.text.toString())
                    putInt(getString(R.string.saved_port_key), port.text.toString().toInt())
                    apply()
                }
                updateUiWithSuccess(loginResult)
            }
        })

        ip.afterTextChanged {
            loginViewModel.loginDataChanged(
                ip.text.toString(),
                port.text.toString()
            )
        }

        port.apply {
            afterTextChanged {
                loginViewModel.loginDataChanged(
                    ip.text.toString(),
                    port.text.toString()
                )
            }

            setOnEditorActionListener { _, actionId, _ ->
                when (actionId) {
                    EditorInfo.IME_ACTION_DONE ->
                        loginViewModel.login(
                            ip.text.toString(),
                            port.text.toString()
                        )
                }
                false
            }

            login.setOnClickListener {
                loading.visibility = View.VISIBLE
                loginViewModel.login(ip.text.toString(), port.text.toString())
            }
        }

        ip.setText(sharedPreferences.getString(getString(R.string.saved_ip_key), ""))
        port.setText(sharedPreferences.getInt(getString(R.string.saved_port_key), 27068).toString())
    }

    private fun updateUiWithSuccess(loginResult: LoginResult) {
        val intent = Intent(this, DeckSelectActivity::class.java).apply {
            putExtra(EXTRA_DECKS_INFO, loginResult.decksInfo!!.toByteArray())
        }
        startActivity(intent)
    }

    private fun showLoginFailed(@StringRes errorString: Int) {
        Toast.makeText(applicationContext, errorString, Toast.LENGTH_SHORT).show()
    }
}

/**
 * Extension function to simplify setting an afterTextChanged action to EditText components.
 */
fun EditText.afterTextChanged(afterTextChanged: (String) -> Unit) {
    this.addTextChangedListener(object : TextWatcher {
        override fun afterTextChanged(editable: Editable?) {
            afterTextChanged.invoke(editable.toString())
        }

        override fun beforeTextChanged(s: CharSequence, start: Int, count: Int, after: Int) {}

        override fun onTextChanged(s: CharSequence, start: Int, before: Int, count: Int) {}
    })
}
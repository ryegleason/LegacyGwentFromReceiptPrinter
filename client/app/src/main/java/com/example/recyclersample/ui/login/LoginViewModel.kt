package com.example.recyclersample.ui.login

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import android.util.Patterns
import androidx.core.text.isDigitsOnly
import com.example.recyclersample.data.LoginRepository
import com.example.recyclersample.data.Result

import com.example.recyclersample.R

class LoginViewModel(private val loginRepository: LoginRepository) : ViewModel() {

    private val _loginForm = MutableLiveData<LoginFormState>()
    val loginFormState: LiveData<LoginFormState> = _loginForm

    private val _loginResult = MutableLiveData<LoginResult>()
    val loginResult: LiveData<LoginResult> = _loginResult

    fun login(ip: String, port: String) {
        // can be launched in a separate asynchronous job
        val result = loginRepository.login(ip, port)

        if (result is Result.Success) {
            _loginResult.value = LoginResult(success = true)
        } else {
            _loginResult.value = LoginResult(error = R.string.login_failed)
        }
    }

    fun loginDataChanged(ip: String, port: String) {
        if (!isIPValid(ip)) {
            _loginForm.value = LoginFormState(ipError = R.string.invalid_ip)
        } else if (!isPortValid(port)) {
            _loginForm.value = LoginFormState(portError = R.string.invalid_port)
        } else {
            _loginForm.value = LoginFormState(isDataValid = true)
        }
    }

    private fun isIPValid(ip: String): Boolean {
        return Patterns.IP_ADDRESS.matcher(ip).matches() || Patterns.WEB_URL.matcher(ip).matches()
    }

    private fun isPortValid(port: String): Boolean {
        return port.isBlank() || (port.isDigitsOnly() && 0 <= port.toInt() && port.toInt() <= 65535)
    }
}
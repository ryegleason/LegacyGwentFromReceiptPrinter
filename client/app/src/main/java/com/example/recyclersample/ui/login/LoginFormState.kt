package com.example.recyclersample.ui.login

/**
 * Data validation state of the login form.
 */
data class LoginFormState(
    val ipError: Int? = null,
    val portError: Int? = null,
    val isDataValid: Boolean = false
)
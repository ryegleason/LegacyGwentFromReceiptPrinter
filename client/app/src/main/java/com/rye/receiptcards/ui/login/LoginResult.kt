package com.rye.receiptcards.ui.login

import com.rye.receiptcards.proto.Reqrep

/**
 * Authentication result : success (user details) or error message.
 */
data class LoginResult(
    val success: Boolean? = null,
    val error: Int? = null,
    val decksInfo: Reqrep.DecksInfo? = null
)
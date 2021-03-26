package com.rye.receiptcards.data

import com.rye.receiptcards.data.model.connect
import java.io.IOException

/**
 * Class that requests authentication and user information from the remote data source and
 * maintains an in-memory cache of login status and user credentials information.
 */

class LoginRepository {

    var isLoggedIn = false


    suspend fun login(ip: String, port: String): Result<Boolean> {
        // handle login
        val serverPort = if (port.isBlank()) {
            27068
        } else {
            port.toInt()
        }

        return try {
            connect("$ip:$serverPort")
            isLoggedIn = true
            Result.Success(isLoggedIn)
        } catch (e: Throwable) {
            e.printStackTrace()
            Result.Error(IOException("Error logging in", e))
        }
    }
}
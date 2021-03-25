package com.rye.receiptcards.data

import com.rye.receiptcards.data.model.ConnectionInfo
import java.io.IOException

/**
 * Class that requests authentication and user information from the remote data source and
 * maintains an in-memory cache of login status and user credentials information.
 */

class LoginRepository {

    // in-memory cache of the loggedInUser object
    var user: ConnectionInfo? = null
        private set

    val isLoggedIn: Boolean
        get() = user != null

    init {
        // If user credentials will be cached in local storage, it is recommended it be encrypted
        // @see https://developer.android.com/training/articles/keystore
        user = null
    }

    suspend fun login(ip: String, port: String): Result<ConnectionInfo> {
        // handle login
        val serverPort = if (port.isBlank()) {
            27068
        } else {
            port.toInt()
        }

        return try {
            val connectionInfo = ConnectionInfo("$ip:$serverPort")
            connectionInfo.connect()
            setLoggedInUser(connectionInfo)
            Result.Success(connectionInfo)
        } catch (e: Throwable) {
            e.printStackTrace()
            Result.Error(IOException("Error logging in", e))
        }
    }

    private fun setLoggedInUser(connectionInfo: ConnectionInfo) {
        this.user = connectionInfo
        // If user credentials will be cached in local storage, it is recommended it be encrypted
        // @see https://developer.android.com/training/articles/keystore
    }
}
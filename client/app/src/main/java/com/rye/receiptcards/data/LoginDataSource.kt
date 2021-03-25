package com.rye.receiptcards.data

import com.rye.receiptcards.data.model.ConnectionInfo
import java.io.IOException

/**
 * Class that handles authentication w/ login credentials and retrieves user information.
 */
class LoginDataSource {

    fun login(ip: String, port: String): Result<ConnectionInfo> {
        val serverPort = if (port.isBlank()) {
            27068
        } else {
            port.toInt()
        }

        return try {
            val connectionInfo = ConnectionInfo("$ip:$serverPort")
            Result.Success(connectionInfo)
        } catch (e: Throwable) {
            Result.Error(IOException("Error logging in", e))
        }
    }
}
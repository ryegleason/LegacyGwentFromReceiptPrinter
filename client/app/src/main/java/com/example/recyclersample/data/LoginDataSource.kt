package com.example.recyclersample.data

import com.example.recyclersample.data.model.ConnectionInfo
import java.io.DataInputStream
import java.io.DataOutputStream
import java.io.IOException
import java.net.Socket

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

        var clientSocket: Socket? = null

        return try {
            // TODO: handle loggedInUser authentication
            clientSocket = Socket(ip, serverPort)
            val connectionInfo = ConnectionInfo(clientSocket, DataInputStream(clientSocket.getInputStream()), DataOutputStream(clientSocket.getOutputStream()), java.util.UUID.randomUUID())
            Result.Success(connectionInfo)
        } catch (e: Throwable) {
            try {
                clientSocket?.close()
            } catch (ex: IOException) {
                ex.printStackTrace()
            }
            Result.Error(IOException("Error logging in", e))
        }
    }

    fun logout(connectionInfo: ConnectionInfo) {
        connectionInfo.dataInputStream.close()
        connectionInfo.dataOutputStream.close()
        connectionInfo.socket.close()
    }
}
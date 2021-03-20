package com.example.recyclersample.data.model

import java.io.DataInputStream
import java.io.DataOutputStream
import java.net.Socket
import java.util.*

/**
 * Data class that captures user information for logged in users retrieved from LoginRepository
 */
data class ConnectionInfo(
    val socket: Socket,
    val dataInputStream: DataInputStream,
    val dataOutputStream: DataOutputStream,
    val uuid: UUID
)
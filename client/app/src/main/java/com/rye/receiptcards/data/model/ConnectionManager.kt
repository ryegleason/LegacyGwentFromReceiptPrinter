package com.rye.receiptcards.data.model

import android.accounts.NetworkErrorException
import com.google.protobuf.InvalidProtocolBufferException
import org.zeromq.SocketType
import org.zeromq.ZContext
import org.zeromq.ZMQ.Poller
import org.zeromq.ZMQ.Socket
import java.lang.Exception
import com.rye.receiptcards.data.Result
import com.rye.receiptcards.data.UUIDToProtoUUID
import com.rye.receiptcards.proto.Reqrep
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.Closeable
import java.util.*

const val REQUEST_RETRIES = 3
const val REQUEST_TIMEOUT: Long = 5000

/**
 * Maintains connection to server
 */
//class ConnectionInfo(private val address: String) : Closeable {

private val ctx: ZContext = ZContext()
private var socket: Socket = ctx.createSocket(SocketType.REQ)!!
private val poller: Poller = ctx.createPoller(1)
private val uuid = UUID.randomUUID()

private lateinit var address: String

suspend fun connect(ipAddress: String) {
    ctx.destroySocket(socket)
    socket = ctx.createSocket(SocketType.REQ)
    address = "tcp://$ipAddress"
    withContext(Dispatchers.IO) {
        socket.connect(address)
        poller.register(socket, Poller.POLLIN)
    }
}

suspend fun request(messageBuilder: Reqrep.Req.Builder) : Result<Reqrep.Rep> {
    messageBuilder.userUuid = UUIDToProtoUUID(uuid)
    val request = messageBuilder.build().toByteArray()

    val reply = withContext(Dispatchers.IO) {

        socket.send(request)

        var retriesLeft: Int = REQUEST_RETRIES
        while (retriesLeft > 0 && !Thread.currentThread().isInterrupted) {
            //  We send a request, then we work to get a reply
            while (true) {
                //  Poll socket for a reply, with timeout
                val rc = poller.poll(REQUEST_TIMEOUT)
                if (rc == -1) break //  Interrupted

                //  Here we process a server reply and exit our loop if the
                //  reply is valid. If we didn't a reply we close the client
                //  socket and resend the request. We try a number of times
                //  before finally abandoning:
                if (poller.pollin(0)) {
                    return@withContext socket.recv()
                }

                if (--retriesLeft == 0) {
                    println("E: server seems to be offline, abandoning\n")
                    break
                } else {
                    println("W: no response from server, retrying\n")
                    //  Old socket is confused; close it and open a new one
                    poller.unregister(socket)
                    ctx.destroySocket(socket)
                    println("I: reconnecting to server\n")
                    socket = ctx.createSocket(SocketType.REQ)
                    socket.connect(address)
                    poller.register(socket, Poller.POLLIN)
                    //  Send request again, on new socket
                    socket.send(request)
                }
            }
        }
        null
    }

    if (reply != null){
        return try {
            Result.Success(Reqrep.Rep.parseFrom(reply))
        } catch (e: InvalidProtocolBufferException) {
            Result.Error(e)
        }
    }
    return Result.Error(NetworkErrorException("Connection failed"))
}

fun close() {
    poller.close()
    ctx.destroy()
}
//}
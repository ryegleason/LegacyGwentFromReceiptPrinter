package com.rye.receiptcards.data.model

import android.accounts.NetworkErrorException
import org.zeromq.SocketType
import org.zeromq.ZContext
import org.zeromq.ZMQ.Poller
import org.zeromq.ZMQ.Socket
import java.lang.Exception
import com.rye.receiptcards.data.Result
import com.rye.receiptcards.data.UUIDToProtoUUID
import com.rye.receiptcards.proto.Reqrep
import java.io.Closeable
import java.util.*


/**
 * Maintains connection to server
 */
class ConnectionInfo(private val address: String) : Closeable {

    companion object {
        const val REQUEST_RETRIES = 3
        const val REQUEST_TIMEOUT: Long = 2500
    }

    private val ctx: ZContext = ZContext()
    private var socket: Socket = ctx.createSocket(SocketType.REQ)!!
    private val poller: Poller = ctx.createPoller(1)
    private val uuid = UUID.randomUUID()

    init {
        socket.connect("tcp://$address")
        poller.register(socket, Poller.POLLIN)
    }

    fun request(messageBuilder: Reqrep.Req.Builder) : Result<Reqrep.Rep> {
        messageBuilder.userUuid = UUIDToProtoUUID(uuid)
        val request = messageBuilder.build().toByteArray()
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
                    val reply = socket.recv()
                    try {
                        return Result.Success(Reqrep.Rep.parseFrom(reply))
                    } catch (e: Exception) {
                        println("Malformed message, parsing error:")
                        e.printStackTrace()
                    }
                }

                if (--retriesLeft == 0) {
                    println("E: server seems to be offline, abandoning\n")
                    break
                } else {
                    println("W: bad/no response from server, retrying\n")
                    //  Old socket is confused; close it and open a new one
                    poller.unregister(socket)
                    ctx.destroySocket(socket)
                    println("I: reconnecting to server\n")
                    socket = ctx.createSocket(SocketType.REQ)
                    socket.connect("tcp://$address")
                    poller.register(socket, Poller.POLLIN)
                    //  Send request again, on new socket
                    socket.send(request)
                }
            }
        }

        return Result.Error(NetworkErrorException("Server offline"))
    }

    override fun close() {
        poller.close()
        ctx.destroy()
    }
}
package com.rye.receiptcards.data

import com.rye.receiptcards.proto.Reqrep
import java.util.*

fun protoUUIDToUUID(uuid: Reqrep.UUID): UUID {
    return UUID(uuid.first64, uuid.second64)
}

fun UUIDToProtoUUID(uuid: UUID): Reqrep.UUID {
    val builder = Reqrep.UUID.newBuilder()
    builder.first64 = uuid.mostSignificantBits
    builder.second64 = uuid.leastSignificantBits
    return builder.build()
}
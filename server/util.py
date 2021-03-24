from uuid import UUID

from proto.protobuf import reqrep_pb2


def proto_UUID_to_UUID(proto_UUID: reqrep_pb2.UUID) -> UUID:
    return UUID(int=(proto_UUID.first64 << 64) + proto_UUID.second64)


def UUID_to_proto_UUID(uuid: UUID) -> UUID:
    proto = reqrep_pb2.UUID()
    proto.first64 = uuid.int >> 64
    proto.second64 = uuid.int & 0xFFFFFFFFFFFFFFFF
    return proto
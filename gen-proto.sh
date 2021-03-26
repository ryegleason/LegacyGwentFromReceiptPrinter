#!/bin/bash
protoc --python_out=server/proto/ --java_out=client/app/src/main/java/ protobuf/reqrep.proto
# Copyright 2020 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python AsyncIO implementation of the GRPC helloworld.Greeter client."""

import asyncio
import logging

import grpc
import helloworld_pb2
import helloworld_pb2_grpc

async def success(stub):
    response = await stub.SayHello(helloworld_pb2.HelloRequest(name="you"))
    print("Greeter client received: " + response.message)

async def actual_error(stub):
    try:
        response = await stub.SayHello(helloworld_pb2.HelloRequest(name="abort"))
        print("Greeter client received: " + response.message)
    except grpc.RpcError as e:
        print(e.debug_error_string())

async def arity_error(stub):
    try:
        response = await stub.SayHello(helloworld_pb2.HelloRequest(name="abort_with_trailing_metadata"))
        print("Greeter client received: " + response.message)
    except grpc.RpcError as e:
        print(e.debug_error_string())

async def run() -> None:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        await success(stub)
        await actual_error(stub)
        await arity_error(stub)


if __name__ == "__main__":
    logging.basicConfig()
    asyncio.run(run())

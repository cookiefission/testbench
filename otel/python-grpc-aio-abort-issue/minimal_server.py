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
"""
The Python AsyncIO implementation of the GRPC helloworld.Greeter server.
Adapted to demonstrate an issue with the opentelemetry python grpc aio implementation
Minimal to only have buggy case
"""

import asyncio
import logging

import grpc
import helloworld_pb2
import helloworld_pb2_grpc


class Greeter(helloworld_pb2_grpc.GreeterServicer):
    async def SayHello(
        self,
        request: helloworld_pb2.HelloRequest,
        context: grpc.aio.ServicerContext,
    ) -> helloworld_pb2.HelloReply:
        metadata = (
            ("this", "should"),
            ("work", "nicely")
        )
        await context.abort(code=grpc.StatusCode.ABORTED, details="This is the actual error message", trailing_metadata=metadata)


async def serve() -> None:
    server = grpc.aio.server()
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())

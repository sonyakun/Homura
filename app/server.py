import asyncio
import hashlib
import json
import os
import random
import string
import struct
import time
import uuid

import aiohttp
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import ciphers, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers import algorithms, modes

from .utils import Utils


class Server:
    @classmethod
    async def serverLoop(
        cls, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        # varint
        buffer = b""
        while True:
            r = await reader.read(1)
            buffer += r
            if not r[0] & 128:
                break
        size = Utils.decodeVarInt(buffer)
        response = await reader.read(size)

        # get packet id
        received = b""
        position = 0
        for r in response:
            received += bytes([r])
            position += 1
            if not r & 128:
                break
        packet_id = Utils.decodeVarInt(received)
        if packet_id != 0:
            writer.close()
            return

        # get protocol version
        received = b""
        for r in response[position:]:
            received += bytes([r])
            position += 1
            if not r & 128:
                break
        protocolVersion = Utils.decodeVarInt(received)

        # get address and port
        received = b""
        for r in response[position:]:
            received += bytes([r])
            position += 1
            if not r & 128:
                break
        size = Utils.decodeVarInt(received)
        address = response[position : position + size].decode("utf-8")
        position += size
        port = struct.unpack(">H", response[position : position + 2])[0]
        position += 2
        received = b""
        for r in response[position:]:
            received += bytes([r])
            position += 1
            if not r & 128:
                break
        nextState = Utils.decodeVarInt(received)
        if nextState != 1 and nextState != 2:
            writer.close()
            return

        if nextState == 1:
            await cls.sendServerDetails(
                reader, writer, protocolVersion, address, port, nextState
            )

    @classmethod
    async def sendServerDetails(
        cls,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        protocolVersion: int,
        address: str,
        port: int,
        nextState: int,
    ):
        response = b""
        while True:
            r = await reader.read(1)
            response += r
            if not r[0] & 128:
                break
        size = Utils.decodeVarInt(response)
        response = await reader.read(size)
        if response != b"\x00":
            writer.close()
            return
        data = json.dumps(
            {
                "version": {"name": "1.12.2", "protocol": protocolVersion},
                "players": {"max": 1, "online": 0},
                "description": {"text": "Hello"},
            }
        ).encode()
        data = b"\x00" + Utils.encodeVarInt(len(data)) + data
        writer.write(Utils.encodeVarInt(len(data)) + data)
        pos = 0
        response = b""
        while True:
            r = await reader.read(1)
            response += r
            pos += 1
            if not r[0] & 128:
                break
        size = Utils.decodeVarInt(response)
        response = await reader.read(size)
        if response[0] != 1:
            writer.close()
            return
        data = response
        data = Utils.encodeVarInt(len(data)) + data
        writer.write(data)
        await writer.drain()
        writer.close()

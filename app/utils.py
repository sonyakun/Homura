import struct
import zlib


class Utils:
    @classmethod
    def encodeVarInt(cls, num):
        res = b""
        while num:
            b = num & 127
            num = num >> 7
            if num != 0:
                b |= 128
            res += bytes([b])
        return res

    @classmethod
    def decodeVarInt(cls, data):
        val = 0
        shift = 0
        for d in data:
            val |= (d & 127) << shift
            if not (d & 128):
                break
            shift += 7
        return val

    @classmethod
    def packVarInt(cls, number, max_bits=32):
        """
        Packs a varint.
        """

        number_min = -1 << (max_bits - 1)
        number_max = +1 << (max_bits - 1)
        if not (number_min <= number < number_max):
            raise ValueError(
                f"varint does not fit in range: {number_min:d} <= {number:d} < {number_max:d}"
            )

        if number < 0:
            number += 1 << 32

        out = b""
        for i in range(10):
            b = number & 0x7F
            number >>= 7
            out += struct.pack("B", b | (0x80 if number > 0 else 0))
            if number == 0:
                break
        return out

    @classmethod
    def packPacket(cls, data: bytes, compression_threshold: int = -1):
        """
        Packs a packet frame. This method handles length-prefixing and
        compression.
        """

        if compression_threshold >= 0:
            # Compress data and prepend uncompressed data length
            if len(data) >= compression_threshold:
                data = cls.packVarInt(len(data)) + zlib.compress(data)
            else:
                data = cls.packVarInt(0) + data

        # Prepend packet length
        return cls.packVarInt(len(data), max_bits=32) + data

    @classmethod
    def packString(cls, text: str):
        """
        Pack a varint-prefixed utf8 string.
        """

        text = text.encode("utf-8")
        return cls.packVarInt(len(text), max_bits=16) + text

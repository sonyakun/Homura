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

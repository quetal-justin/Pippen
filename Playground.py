import sys

file = sys.argv[1] # get file path
# (fileName, extName) = filePath.rsplit('.', maxsplit=1)

contents = ""

# ---------------------------------------------------------------------------------
# A. Chunks 
# 
# - Factor Pattern for object creation
# ---------------------------------------------------------------------------------
class Chunk:

    # Factory Pattern 
    @staticmethod
    def create(hexChunkType):
        creator = get_creator(hexChunkType)
        return creator()
    
    # def extractChunkData(self):

def get_creator(hexChunkType):
    if hexChunkType == '49484452': # IHDR Chunk
        return IdhrChunk
    elif hexChunkType == '504C5445': # PLTE Chunk
        return PlteChunk
    elif hexChunkType == '49444154': # IDAT Chunk(s)
        return IdatChunk
    elif hexChunkType == '49454E44': # IEND Chunk
        return IendChunk
    else:
        raise ValueError(hexChunkType)

class IdhrChunk(Chunk):
    def __init__(self):
        self._element = None
        print(type(self))

class PlteChunk(Chunk):
    def __init__(self):
        self._element = None
        print(type(self))

class IdatChunk(Chunk):
    def __init__(self):
        self._element = None
        print(type(self))

class IendChunk(Chunk):
    def __init__(self):
        self._element = None
        print(type(self))

# ---------------------------------------------------------------------------------
# Y. Bits
# ---------------------------------------------------------------------------------
# assume it is a hex value
def get_bit(target, n, bitRange=4):
    if (
        (target is not None) and (n in range(0,bitRange)) and (type(target) == str) and 
        (target.isdigit() or (target.upper() >= 'A' and target.upper() <= 'F'))
    ):
        return (1) if (int(target, 16) & (1 << n) > 0) else (0)
    else:
        return None

# ---------------------------------------------------------------------------------
# Z. Main
# ---------------------------------------------------------------------------------

# 1 byte = 8 bits = 2 * 4 bits = 2 * 1 hex digit = 2 hex digits 
with open(file, "rb") as f:
    hexLine = "".join([line.hex() for line in f.readlines()])  # convert bytes to hex (no need to strip line: each singel byte matters when parsing PNG format)
    
    print(hexLine)
    # print(getBit(hexLine[0], 3))

# print(globals()['ChunkCreator'])

plteChunk = Chunk.create('504C5445')

idhrChunk = Chunk.create('49484452')
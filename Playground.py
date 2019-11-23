import sys

file = sys.argv[1] # get file path
# (fileName, extName) = filePath.rsplit('.', maxsplit=1)

contents = ""

# ---------------------------------------------------------------------------------
# A. Data Stream
#
# - to store all chunks in the image. 
# ---------------------------------------------------------------------------------
class DataStrem:

    def __init__(self):
        self._idhrChunk = None
        self._plteChunk = None
        self._idatChunk = None
        self._iendChunk = None
        pass

    def set_idhr_chunk(self, idhrChunk):
        self._idhrChunk = idhrChunk

    def set_plte_chunk(self, plteChunk):
        self._plteChunk = plteChunk

    def set_idat_chunk(self, idatChunk):
        self._idatChunk = idatChunk

    def set_iend_chunk(self, iendChunk):
        self._iendChunk = iendChunk

# ---------------------------------------------------------------------------------
# X. Chunk
# 
# - Factor Pattern for object creation
# - if not having __init__(self) in subclass, super class's __init__(self) is called
# - reference: Understanding Class Inheritance in Python 3
#   https://www.digitalocean.com/community/tutorials/understanding-class-inheritance-in-python-3
# ---------------------------------------------------------------------------------
class Chunk:

    def __init__(self):
        self._length = None         # 4-bytes; unsigned int; for _chunkData; valid values: 0 ~ 2^(31) - 1
        self._chunkType = None      # 4-bytes (8 hex characters); hex string values
        self._chunkData = None      # _length-bytes; dictionary or None
        self._crc = None            # 4-bytes (8 hex characters); hex string values; for _chunkType and _chunkData
        pass

    # Factory Pattern 
    @staticmethod
    def create(chunkType):
        creator = _get_creator(chunkType)
        return creator()

    # - this is called when child class has no overriding, i.e. no data field.
    # - None is returned
    # - length = data length
    def extract_data(self, length, hexChunkData):
        return None 

    # --- accessors ---
    def get_length(self):
        return self._length

    def get_type(self):
        return self._chunkType

    def get_data(self):
        return self._chunkData

    def get_crc(self):
        return self._crc

    # --- mutators ---
    def set_length(self, length):
        self._length = length
    
    def set_type(self, chunkType):
        self._chunkType = chunkType

    def set_data(self, chunkData):
        self._chunkData = chunkData

    def set_crc(self, crc):
        self._crc = crc

# used by Chunk class
def _get_creator(chunkType):
    if chunkType == '49484452' or chunkType == 'IHDR' or chunkType == 'ihdr': # IHDR Chunk
        return IdhrChunk
    elif chunkType == '504C5445' or chunkType == 'PLTE' or chunkType == 'plte': # PLTE Chunk
        return PlteChunk
    elif chunkType == '49444154' or chunkType == 'IDAT' or chunkType == 'idat': # IDAT Chunk(s)
        return IdatChunk
    elif chunkType == '49454E44' or chunkType == 'IEND' or chunkType == 'iend': # IEND Chunk
        return IendChunk
    else:
        raise ValueError(chunkType)

class IdhrChunk(Chunk):
    
    # override
    def extract_data(self, length, hexChunkData):
        data = {
            'width': None,              # 4-bytes; unsigned int; 0 is invalid
            'height': None,             # 4-bytes; unsigned int; 0 is invalid
            'bitDepth': None,           # 1-byte; int; number of bits per sample; valid values = 1,2,4,8,16; not all values allowed for all colour types.
            'colourType': None,         # 1-byte; int; PNG image type; valid values = 0,2,3,4,6
            'compressionMethod': None,  # 1-byte; int; method to compress the image data; (#)valid value = 0(#); 
            'filterMethod': None,       # 1-byte; int; preprocessing method applied before compresson; (#)valid value = 0(#); 
            'interlaceMethod': None     # 1-byte; int; transmission order of the image data before compresson; valid value = 0 (no interlace) or 1 (Adam7 interlace).
        }

        assert (data['width'] is None), "Not None!!"
        assert (data['height'] is None), "Not None!!"
        assert (data['bitDepth'] is None), "Not None!!"
        assert (data['colourType'] is None), "Not None!!"
        assert (data['compressionMethod'] is None), "Not None!!"
        assert (data['filterMethod'] is None), "Not None!!"
        assert (data['interlaceMethod'] is None), "Not None!!"

        # data length must be 26 in IHDR
        if len(hexChunkData) == length * 2:
            data['width'] = int(hexChunkData[0:8], 16)
            data['height'] = int(hexChunkData[8:16], 16)
            data['bitDepth'] = int(hexChunkData[16:18], 16)
            data['colourType'] = int(hexChunkData[18:20], 16)
            data['compressionMethod'] = int(hexChunkData[20:22], 16)
            data['filterMethod'] = int(hexChunkData[22:24], 16)
            data['interlaceMethod'] = int(hexChunkData[24:26], 16)
            return data
        else:
            raise ValueError(len(hexChunkData))

class PlteChunk(Chunk):
    
    # override
    def extract_data(self, length, hexChunkData):
        pass

class IdatChunk(Chunk):

    # override
    def extract_data(self, length, hexChunkData):
        pass

# no chunk data, i.e. no need to extract data
class IendChunk(Chunk):
    pass

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
    hexLine = "".join([line.hex() for line in f.readlines()[0:20]]).upper()  # convert bytes to hex (no need to strip line: each singel byte matters when parsing PNG format)
    
    if hexLine[0:16] == "89504E470D0A1A0A": # png must begin with this eight bytes
        chunkStartIdx = 16
        while chunkStartIdx != len(hexLine):
            print(chunkStartIdx)
            
            # parse chunks
            length = int(hexLine[chunkStartIdx : chunkStartIdx+8], 16)                  # get Length
            hexChunkType = hexLine[chunkStartIdx+8 : chunkStartIdx+16]                  # get Chunk Type
            hexChunkData = hexLine[chunkStartIdx+16 : chunkStartIdx+16+length*2]        # get Chunk Data (note: length -> bytes => need *2)
            hexCrc = hexLine[chunkStartIdx+16+length*2 : chunkStartIdx+16+length*2+8]   # get CRC
            assert (length * 2 == len(hexChunkData)), "Inconsistent Data: hex should have a double of length than byte!!"
            assert (len(hexLine[chunkStartIdx : chunkStartIdx+8]) + len(hexChunkType) + len(hexChunkData) + len(hexCrc) == chunkStartIdx+length*2+8), "Inconsistent Data!"
            
            # create new Chunk of corresponding type
            chunk = Chunk.create(hexChunkType)
            assert (chunk.get_length() is None), "Wrong Value!!"
            assert (chunk.get_type() is None), "Wrong Value!!"
            assert (chunk.get_data() is None), "Wrong Value!!"
            assert (chunk.get_crc() is None), "Wrong Value!!"
            
            # extract Chunk Data based on its type (polymorphism)
            chunkData = chunk.extract_data(length, hexChunkData)
            print(chunkData)

            # store information into Chunk object
            chunk.set_length(length)
            chunk.set_type(hexChunkType)
            chunk.set_data(chunkData)
            chunk.set_crc(hexCrc)
            assert (chunk.get_length() == length), "Wrong Value!!"
            assert (chunk.get_type() == hexChunkType), "Wrong Value!!"
            assert (chunk.get_data() == chunkData), "Wrong Value!!"
            assert (chunk.get_crc() == hexCrc), "Wrong Value!!"

            # update chunk starting index (i.e. the counter)
            chunkStartIdx += 16 + length + 8
            
    else:
        raise ValueError(hexLine[0:16])

    print(hexLine)
    # print(getBit(hexLine[0], 3))

# print(globals()['ChunkCreator'])

plteChunk = Chunk.create('504C5445')
print(plteChunk.get_length())

iendChunk = Chunk.create('49454E44')
print(iendChunk.extract_data(1,'E3'))
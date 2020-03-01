# SCI 2000 - Project Report
# Topic: Topic 4 - Image Compression
# Name: Justin M. C. Choi & Mike Winkler
# Date: Dec/03/2019 (Tue) 

## How to run?

> python3 Playground.py <png_image_path>

## Goal

Our goal in this project is to convert an PNG image into a PPM image.

## Steps

Step 1 - Format PNG Datastream

PNG Datastream can be splitted into chunks together with a signature at the beginning. In general, a chunk consists of four fields: Length, Type, Data, and CRC (Cyclic Redundancy Code). Length gives the number of bytes in the Data field, instead of the number of bytes in the whole chunk. Type indicates what the chunk is used for. Data stores information corresponding to the chunk type. CRC is used for detecting errors.

Although there are 16 chunk types available in total, only three of them must be in a PNG datastream. They are IDHR, IDAT, and IEND. IDHR chunk stores basic information about the PNG image, such as width, height, and bit depth (the maximum pixel value). IDAT chunk stores the compressed image data. IEND chunk is just a chunk indicating the end of the PNG datastream, so it stores no data inside. While IDHR chunk and IEND chunk must appear only once, one or more IDAT chunks can be in the PNG datastream. When there are multiple IDAT chunks, we need to concatenate the data field of all IDAT chunks to get the compressed image data in "zlib" format. 

Step 2 - Decompression (Zlib)

"zlib" datastream is compressed by using deflate/inflate compression with a sliding window of at most 32728 bytes (2^48 bits). Deflate/inflate compression uses two lossless data compression algorithms: LZ77 and Huffman coding. While LZ77 compresses data by replacing repeated occurrences of data with a pair of length-distance numbers, Huffman coding encodes data based on the frequency it appears (the more frequent the data appear, the shorter the encoding results will be). In our project, we import a library to achieve this due to time constraints.

Step 3-5 - Reconstruction (Un-filter), Deserialization, and Un-Interlacing

After the "zlib" datastream is decompressed, we get a bunch of filtered scanlines, i.e. a filtered row of pixels. Each filtered scanline begins with a filter type (which is NOT the same as the filter method in IDHR block), followed by a sequence of pixels. There are five filter types: None (0), Sub (1), Up (2), Average (3), and Paeth (4). Each of them corresponds to a linear operation. In order to reconstruct the filtered scanline, the opposite function should be applied. The result will be a bunch of scanlines, and they can be deserialized.

The last step is to undo the interlacing step, if there is one. When interlace method in IDHR chunk is equal to one, Adam 7 is used. In Adam 7, each pixel will be mapped to a distinct pass based on its position in the Adam 7's 8-by-8 pattern. If the image is over 8-by-8, then it will replicate the same pattern to the exceeding parts.  

Although we don't have time to achieve these steps 3, 4, and 5, we understand more about why PNG does things in this specific way. For example, in many cases, the difference in between two adjacent pixels is small. If this characteristic is applied together with LZ77 and the Huffman code compression algorithm, spaces for storing the image can be greatly reduced. This is a motivation of having the fitering process.

Also, interlacing is important because it allows a blurred image to be shown while loading, instead of forcing users to wait until all pixels of the image is shown.

## Result

We rebuild the shape of Pippen (the penguin picture) successfully. 

## Description

- Justin is responsible for code design and code implementation. 

- Mike is responsible for the presentation.

## References

- Portable Network Graphics (PNG) Specification (Second Edition) 
  https://www.w3.org/TR/2003/REC-PNG-20031110/#8Interlace

- ZLIB Compressed Data Format Specification
  https://www.ietf.org/rfc/rfc1950.txt

- DEFLATE Compressed Data Format Specification version 1.3
  https://tools.ietf.org/html/rfc1951

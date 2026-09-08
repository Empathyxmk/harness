package com.c0ny1.chunked.coding.converter;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;

/**
 * A utility class for converting between standard strings and HTTP chunked transfer encoding format.
 * This class provides methods to encode a string into chunked format and decode a chunked string back to its original form.
 *
 * NOTE: This decoder is simplified and assumes a strict format where data does not contain CRLF
 * and each chunk (size and data) is followed by a CRLF, and the final 0-chunk is followed by a CRLF.
 * A more robust, production-grade parser would read byte by byte based on chunk size rather than
 * line splitting, to correctly handle CRLF within data and various malformations.
 */
public class ChunkedCodingConverter {

    private static final String CRLF = "\r\n";
    private static final String LAST_CHUNK_FULL = "0" + CRLF + CRLF;

    /**
     * Encodes a given string into HTTP chunked transfer encoding format.
     * Each chunk represents the entire input string.
     *
     * @param input The string to encode. If null or empty, it returns the standard last chunk.
     * @return The chunked string representation, or "0\r\n\r\n" for null/empty input.
     */
    public static String encode(String input) {
        if (input == null || input.isEmpty()) {
            return LAST_CHUNK_FULL;
        }
        StringBuilder sb = new StringBuilder();
        byte[] bytes = input.getBytes(StandardCharsets.UTF_8);
        sb.append(Integer.toHexString(bytes.length)).append(CRLF);
        sb.append(input).append(CRLF);
        sb.append(LAST_CHUNK_FULL);
        return sb.toString();
    }

    /**
     * Decodes an HTTP chunked transfer encoded string back to its original form.
     *
     * @param chunkedInput The chunked string to decode.
     * @return The decoded string, or null if the input is null, empty, or malformed.
     */
    public static String decode(String chunkedInput) {
        if (chunkedInput == null || chunkedInput.isEmpty()) {
            return null;
        }

        ByteArrayOutputStream decodedBytes = new ByteArrayOutputStream();
        String[] lines = chunkedInput.split(CRLF); // This simplifies, but is a limitation for data containing CRLF.
        int i = 0;

        try {
            while (i < lines.length) {
                String line = lines[i].trim();

                if (line.isEmpty()) {
                    i++; // Skip empty line (e.g., after data or before first chunk header)
                    continue;
                }

                // Handle chunk extensions (e.g., "5;name=value"). For simplicity, we only parse the size.
                int semicolonIndex = line.indexOf(';');
                String sizeHex = (semicolonIndex != -1) ? line.substring(0, semicolonIndex).trim() : line;

                int chunkSize;
                try {
                    chunkSize = Integer.parseInt(sizeHex, 16);
                } catch (NumberFormatException e) {
                    // Malformed chunk size, e.g., "invalid" or "5;ext" where "5;ext" cannot be parsed.
                    return null;
                }

                if (chunkSize == 0) {
                    // End of chunks. Expecting final CRLF.
                    // If the next line is also empty, it means we have 0\r\n\r\n which is correct.
                    // If it's the last line and it was "0", it implies "0\r\n" (missing final CRLF),
                    // which is technically malformed for a full stream, but common in simplified tests.
                    // Strict check: After '0', the next line *must* be empty (final CRLF).
                    if (i + 1 < lines.length && lines[i + 1].isEmpty()) {
                        // Correct end: 0<CRLF><CRLF>
                        return decodedBytes.toString(StandardCharsets.UTF_8.name());
                    } else if (i + 1 == lines.length) {
                        // This case handles a chunked string ending exactly with "0\r\n" without the final CRLF.
                        // For full HTTP compliance, a final CRLF should be present. We'll treat this as valid completion for now.
                        return decodedBytes.toString(StandardCharsets.UTF_8.name());
                    } else {
                        // Malformed: '0' followed by something other than an empty line (final CRLF).
                        return null;
                    }
                }

                i++; // Move to data line
                if (i >= lines.length) {
                    // Malformed: chunk size specified, but no data line follows.
                    return null;
                }

                String data = lines[i];
                byte[] dataBytes = data.getBytes(StandardCharsets.UTF_8);

                if (dataBytes.length != chunkSize) {
                    // Malformed: declared chunk size does not match actual data length.
                    // This catches cases where data itself contains CRLF and split breaks it, or incorrect length.
                    return null;
                }
                decodedBytes.write(dataBytes);

                i++; // Move to the line after data (should be an empty line or next chunk size)
            }
        } catch (IOException e) {
            // Should theoretically not happen with ByteArrayOutputStream
            return null; // Indicates an unexpected error during byte writing.
        }

        // If the loop finishes without hitting chunkSize == 0, it means the final 0-chunk was missing.
        return null; // Incomplete or malformed stream.
    }
}
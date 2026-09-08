package com.backblaze.erasure;

import org.junit.Test;
import static org.junit.Assert.*;

public class ReedSolomonPublicTest {
    @Test
    public void testEncodeDecodeWithOtherData() {
        ReedSolomon rs = ReedSolomon.create(4, 3); // different parameters than the likely default
        byte[][] shards = new byte[7][10];
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 10; j++) {
                shards[i][j] = (byte) ((i + 1) * (j + 3));
            }
        }
        rs.encodeParity(shards, 0, 10);

        // Simulate missing any 3 data
        shards[1] = new byte[10];
        shards[5] = new byte[10];
        shards[6] = new byte[10];
        boolean[] shardPresent = {true, false, true, true, true, false, false};

        rs.decodeMissing(shards, shardPresent, 0, 10);

        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 10; j++) {
                byte expected = (byte) ((i + 1) * (j + 3));
                assertEquals(expected, shards[i][j]);
            }
        }
    }
}
package com.backblaze.erasure;

import org.junit.Test;
import static org.junit.Assert.*;

import java.util.Arrays;

public class FecPublicTest {
    @Test
    public void testFecDecodeOtherData() {
        int dataShards = 5;
        int parityShards = 2;
        Fec fec = new Fec(dataShards, parityShards);

        byte[][] matrix = new byte[dataShards + parityShards][32];
        // fill with new input pattern
        for (int i = 0; i < dataShards; i++) {
            Arrays.fill(matrix[i], (byte) (i + 10));
        }
        fec.encode(matrix, 0, 32);

        // lose different shards (simulate erasure)
        boolean[] mark = new boolean[dataShards + parityShards];
        Arrays.fill(mark, true);
        mark[2] = false;  // lose shard 2
        mark[4] = false;  // lose shard 4
        mark[6] = false;  // lose one parity

        byte[][] recovered = new byte[dataShards][32];
        System.arraycopy(matrix, 0, recovered, 0, dataShards);
        fec.decode(recovered, mark, 32);

        // Check that lost data shards are all (10+idx)
        assertEquals(12, recovered[2][0]);
        assertEquals(14, recovered[4][0]);
    }
}
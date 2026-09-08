package com.example.public_tests;

import com.example.haishoku.haillow.Haillow;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicHaillowTest {

    @Test
    public void testTupleToHexPublic() {
        String hex = Haillow.tupleToHex(new int[]{12, 210, 111});
        assertEquals("#0cd26f", hex);
    }

    @Test
    public void testHexToTuplePublic() {
        int[] tuple = Haillow.hexToTuple("#123456");
        assertArrayEquals(new int[]{18, 52, 86}, tuple);
    }
}
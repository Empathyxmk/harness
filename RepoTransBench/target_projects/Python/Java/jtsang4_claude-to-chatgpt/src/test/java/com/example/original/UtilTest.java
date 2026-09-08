package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import org.mockito.MockedStatic;
import org.mockito.Mockito;

public class UtilTest {

    @Test
    public void testNumTokensFromStringBasic() {
        try (MockedStatic<TiktokenEncoding> mocked = Mockito.mockStatic(TiktokenEncoding.class)) {
            mocked.when(() -> TiktokenEncoding.getEncoding("cl100k_base"))
                    .thenReturn(new DummyEncoding(new int[]{1, 2, 3}));
            int tokens = UtilMock.numTokensFromString("abc");
            assertEquals(3, tokens);
        }
    }

    @Test
    public void testNumTokensFromStringEmpty() {
        try (MockedStatic<TiktokenEncoding> mocked = Mockito.mockStatic(TiktokenEncoding.class)) {
            mocked.when(() -> TiktokenEncoding.getEncoding("cl100k_base"))
                    .thenReturn(new DummyEncoding(new int[]{}));
            int tokens = UtilMock.numTokensFromString("");
            assertEquals(0, tokens);
        }
    }

    // Dummy encoding/mock
    public static class DummyEncoding {
        private int[] vals;

        public DummyEncoding(int[] vals) { this.vals = vals; }
        public int[] encode(String input) { return vals; }
    }
}

class TiktokenEncoding {
    public static UtilTest.DummyEncoding getEncoding(String name) { return null; }
}

class UtilMock {
    // Replaces util.num_tokens_from_string
    public static int numTokensFromString(String s) {
        UtilTest.DummyEncoding encoding = TiktokenEncoding.getEncoding("cl100k_base");
        int[] encoded = encoding.encode(s);
        return encoded.length;
    }
}
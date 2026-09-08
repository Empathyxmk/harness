package com.example.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import org.mockito.MockedStatic;
import org.mockito.Mockito;

public class PublicUtilTest {
    @Test
    public void testPublicNumTokensFromStringNonempty() {
        try (MockedStatic<PublicTiktokenEncoding> mocked = Mockito.mockStatic(PublicTiktokenEncoding.class)) {
            mocked.when(() -> PublicTiktokenEncoding.getEncoding("cl100k_base"))
                    .thenReturn(new DummyPublicEncoding(new int[]{4,5,6,7,8}));
            int tokens = PublicUtilMock.numTokensFromString("hello");
            assertEquals(5, tokens);
        }
    }

    @Test
    public void testPublicNumTokensFromStringEmpty() {
        try (MockedStatic<PublicTiktokenEncoding> mocked = Mockito.mockStatic(PublicTiktokenEncoding.class)) {
            mocked.when(() -> PublicTiktokenEncoding.getEncoding("cl100k_base"))
                    .thenReturn(new DummyPublicEncoding(new int[]{}));
            int tokens = PublicUtilMock.numTokensFromString("");
            assertEquals(0, tokens);
        }
    }
    public static class DummyPublicEncoding {
        private int[] data;
        public DummyPublicEncoding(int[] data) { this.data = data; }
        public int[] encode(String input) { return data; }
    }
}
class PublicTiktokenEncoding {
    public static PublicUtilTest.DummyPublicEncoding getEncoding(String name) { return null; }
}
class PublicUtilMock {
    public static int numTokensFromString(String s) {
        PublicUtilTest.DummyPublicEncoding encoding = PublicTiktokenEncoding.getEncoding("cl100k_base");
        int[] encoded = encoding.encode(s);
        return encoded.length;
    }
}
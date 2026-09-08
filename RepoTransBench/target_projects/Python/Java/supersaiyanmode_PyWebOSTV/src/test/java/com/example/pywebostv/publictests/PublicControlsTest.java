package com.example.pywebostv.publictests;

import com.example.pywebostv.utils.FakeClient;
import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class PublicControlsTest {

    @Test
    public void testBadArgumentParamPublic() {
        assertThrows(IllegalArgumentException.class, () -> arguments(new ArrayList<>()));
        assertThrows(IllegalArgumentException.class, () -> arguments(""));
    }

    public static <T> Extractor<T> arguments(Object param) {
        if (param == null || (param instanceof Collection && ((Collection<?>) param).isEmpty()) || (param instanceof String && ((String) param).isEmpty()))
            throw new IllegalArgumentException("Invalid param");
        return new Extractor<>(param);
    }

    static class Extractor<T> {
        Object param;
        Extractor(Object p) { param = p; }
        T extract(Object... args) {
            if (args == null || args.length == 0)
                throw new IllegalArgumentException("No args!");
            return (T) args[0]; // leftmost
        }
    }

    @Test
    public void testExtractPositionalArgsPublic() {
        Extractor<String> args = arguments(0);
        assertEquals("x", args.extract("x", "y", "z"));
        assertThrows(IllegalArgumentException.class, () -> args.extract());
    }

    // add the rest of public test mapping here...

}
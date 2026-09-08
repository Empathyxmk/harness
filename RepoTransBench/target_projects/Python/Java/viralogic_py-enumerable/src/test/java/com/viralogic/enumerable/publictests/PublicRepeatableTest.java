package com.viralogic.enumerable.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class PublicRepeatableTest {

    @Test
    void testRepeatableIterablePublic() {
        List<Integer> src = Arrays.asList(11, 22, 33);
        List<Integer> again = new ArrayList<>(src);
        List<Integer> twice = new ArrayList<>(src);
        assertEquals(Arrays.asList(11, 22, 33), again);
        assertEquals(Arrays.asList(11, 22, 33), twice);
    }
}
package com.gregmalcolm.pythonkoans.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import org.mockito.Mockito;

interface PubSampleDependency {
    int calculate(int x, int y);
}

class PublicMockTest {

    @Test
    void testMockingDependency() {
        PubSampleDependency dep = Mockito.mock(PubSampleDependency.class);
        Mockito.when(dep.calculate(3, 7)).thenReturn(10);

        assertEquals(10, dep.calculate(3, 7));
        Mockito.verify(dep).calculate(3, 7);
    }
}
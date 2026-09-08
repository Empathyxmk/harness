package com.gregmalcolm.pythonkoans.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import org.mockito.Mockito;

interface PubSampleDependencyExtra {
    int multiply(int x, int y);
}

class PublicMockExtraTest {

    @Test
    void testMockingDependencyMultiply() {
        PubSampleDependencyExtra dep = Mockito.mock(PubSampleDependencyExtra.class);
        Mockito.when(dep.multiply(4, 6)).thenReturn(24);

        assertEquals(24, dep.multiply(4, 6));
        Mockito.verify(dep).multiply(4, 6);
    }
}
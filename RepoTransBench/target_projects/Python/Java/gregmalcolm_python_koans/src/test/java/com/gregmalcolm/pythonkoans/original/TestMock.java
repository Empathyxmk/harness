package com.gregmalcolm.pythonkoans.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import org.mockito.Mockito;

interface SampleDependency {
    int calculate(int x, int y);
}

class TestMock {

    @Test
    void testMockingDependency() {
        // Simulates mock usage in Python, test_mock.py
        SampleDependency dep = Mockito.mock(SampleDependency.class);
        Mockito.when(dep.calculate(2, 3)).thenReturn(5);

        assertEquals(5, dep.calculate(2, 3));
        Mockito.verify(dep).calculate(2, 3);
    }
}
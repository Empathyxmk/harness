package com.aiforever.gigachat.publicapi;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class Usage {
    int used;
    int quota;

    public Usage(int used, int quota) {
        this.used = used;
        this.quota = quota;
    }

    double usageRatio() {
        return quota > 0 ? (double) used / quota : 0.0;
    }
}

public class PublicUsageTest {

    @Test
    void testUsageRatio() {
        Usage u = new Usage(50, 120);
        assertEquals(50.0 / 120.0, u.usageRatio());
    }

    @Test
    void testZeroQuota() {
        Usage u = new Usage(50, 0);
        assertEquals(0.0, u.usageRatio());
    }
}
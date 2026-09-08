package com.plattysoft.leonids;

import org.junit.Test;

import static org.junit.Assert.*;

// Public test: Verify time progression in ParticleSystem
public class ParticleSystemDummyPublicTest {

    @Test
    public void testUpdateTimeProgressionPublic() {
        ParticleSystem ps = new ParticleSystem(null, 10, null, 3000);
        long startTime = 1000L;
        ps.mCurrentTime = startTime;
        ps.update(startTime + 300);
        assertEquals(1300L, ps.mCurrentTime);
    }
}
package com.plattysoft.leonids;

import org.junit.Test;

import static org.junit.Assert.*;

// Public test: different properties for a Particle
public class ParticlePublicTest {

    @Test
    public void testInitialValuesAreSetPublic() {
        Particle p = new Particle();
        p.mCurrentX = 15f;
        p.mCurrentY = 25f;
        assertEquals(15f, p.mCurrentX, 0.01);
        assertEquals(25f, p.mCurrentY, 0.01);
    }
}
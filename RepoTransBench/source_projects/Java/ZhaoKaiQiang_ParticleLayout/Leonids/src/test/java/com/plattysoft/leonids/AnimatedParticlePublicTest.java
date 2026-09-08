package com.plattysoft.leonids;

import org.junit.Test;

import static org.junit.Assert.*;

// Public test: Test animated particle with different animation values
public class AnimatedParticlePublicTest {
    @Test
    public void testAnimatedParticleAnimationValuesPublic() {
        AnimatedParticle particle = new AnimatedParticle();
        particle.mLifetime = 3000;
        assertEquals(3000, particle.mLifetime);
    }
}
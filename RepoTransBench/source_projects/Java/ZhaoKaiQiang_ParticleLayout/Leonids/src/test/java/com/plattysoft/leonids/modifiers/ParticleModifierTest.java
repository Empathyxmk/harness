package com.plattysoft.leonids.modifiers;

import com.plattysoft.leonids.Particle;
import org.junit.Test;

public class ParticleModifierTest {
    @Test
    public void testApplyNoop() {
        Particle p = new Particle();
        ParticleModifier modifier = (particle, miliseconds) -> {};
        modifier.apply(p, 10L);
    }
}
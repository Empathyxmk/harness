package com.plattysoft.leonids.modifiers;

import com.plattysoft.leonids.Particle;

import org.junit.Test;

import static org.junit.Assert.*;

// Public test: create a dummy modifier and invoke modify with different data
public class ParticleModifierPublicTest {

    @Test
    public void testModifyPublic() {
        ParticleModifier m = new ParticleModifier() {
            @Override
            public void apply(Particle particle, long miliseconds) {
                // Set new test value
                particle.mCurrentY = 44f;
            }
        };
        Particle p = new Particle();
        m.apply(p, 100);
        assertEquals(44f, p.mCurrentY, 0.001);
    }

}
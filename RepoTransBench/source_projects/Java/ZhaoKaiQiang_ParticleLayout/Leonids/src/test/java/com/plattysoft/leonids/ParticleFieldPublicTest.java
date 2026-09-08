package com.plattysoft.leonids;

import android.content.Context;
import android.view.View;

import org.junit.Test;

import java.util.ArrayList;

import static org.junit.Assert.*;

// Public test: Test setting particles with new test values.
public class ParticleFieldPublicTest {

    @Test
    public void testSetParticlesPublic() {
        Context ctx = null;
        ParticleField field = new ParticleField(ctx);
        ArrayList<Particle> particles = new ArrayList<>();
        Particle p = new Particle();
        particles.add(p);
        field.setParticles(particles);
        assertNotNull(field);
        assertEquals(1, particles.size());
    }
}
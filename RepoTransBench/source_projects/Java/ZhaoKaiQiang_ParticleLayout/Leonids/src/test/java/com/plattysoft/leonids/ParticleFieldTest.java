package com.plattysoft.leonids;

import android.content.Context;
import android.graphics.Canvas;
import android.util.AttributeSet;

import org.junit.Before;
import org.junit.Test;

import java.util.ArrayList;

import static org.mockito.Mockito.*;

public class ParticleFieldTest {

    private Context mockContext;
    private AttributeSet mockAttrs;
    private Canvas mockCanvas;

    @Before
    public void setUp() {
        mockContext = mock(Context.class);
        mockAttrs = mock(AttributeSet.class);
        mockCanvas = mock(Canvas.class);
    }

    @Test
    public void testConstructors() {
        ParticleField pf1 = new ParticleField(mockContext);
        ParticleField pf2 = new ParticleField(mockContext, mockAttrs);
        ParticleField pf3 = new ParticleField(mockContext, mockAttrs, 0);
    }

    @Test
    public void testSetParticlesAndOnDraw() {
        ParticleField pf = new ParticleField(mockContext);
        Particle particle1 = mock(Particle.class);
        Particle particle2 = mock(Particle.class);
        ArrayList<Particle> particles = new ArrayList<>();
        particles.add(particle1);
        particles.add(particle2);
        pf.setParticles(particles);
        pf.onDraw(mockCanvas);
        verify(particle1, atLeastOnce()).draw(any(Canvas.class));
        verify(particle2, atLeastOnce()).draw(any(Canvas.class));
    }

}
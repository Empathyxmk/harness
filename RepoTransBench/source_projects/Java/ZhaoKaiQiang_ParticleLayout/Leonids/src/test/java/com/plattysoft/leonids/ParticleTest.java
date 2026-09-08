package com.plattysoft.leonids;

import android.graphics.Bitmap;
import android.graphics.Canvas;

import com.plattysoft.leonids.modifiers.ParticleModifier;

import org.junit.Before;
import org.junit.Test;
import org.mockito.ArgumentCaptor;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class ParticleTest {

    private Bitmap mockBitmap;
    private Canvas mockCanvas;
    private ParticleModifier mockModifier;
    private Particle particle;

    @Before
    public void setUp() {
        mockBitmap = mock(Bitmap.class);
        mockCanvas = mock(Canvas.class);
        mockModifier = mock(ParticleModifier.class);
        particle = new Particle(mockBitmap);
        particle.activate(0, new ArrayList<ParticleModifier>(Collections.singletonList(mockModifier)));
    }

    @Test
    public void testInitDefaults() {
        particle.init();
        assertEquals(1f, particle.mScale, 0.001f);
        assertEquals(255, particle.mAlpha);
    }

    @Test
    public void testConfigureSetsFields() {
        when(mockBitmap.getWidth()).thenReturn(10);
        when(mockBitmap.getHeight()).thenReturn(20);
        particle.configure(1000, 100f, 200f);
        // Should center particle coordinates
        assertEquals(95f, particle.mInitialX, 0.001f);
        assertEquals(190f, particle.mInitialY, 0.001f);
        assertEquals(95f, particle.mCurrentX, 0.001f);
        assertEquals(190f, particle.mCurrentY, 0.001f);
    }

    @Test
    public void testUpdateReturnsFalseWhenExpired() {
        when(mockBitmap.getWidth()).thenReturn(10);
        when(mockBitmap.getHeight()).thenReturn(20);
        particle.configure(100, 5, 5);
        boolean active = particle.update(200);
        assertFalse(active);
    }

    @Test
    public void testUpdateMovesParticleAndCallsModifier() {
        when(mockBitmap.getWidth()).thenReturn(10);
        when(mockBitmap.getHeight()).thenReturn(10);
        particle.activate(50, Arrays.asList(mockModifier));
        particle.configure(1000, 20f, 22f);
        particle.mSpeedX = 2f;
        particle.mSpeedY = 3f;
        particle.mRotationSpeed = 30f;
        boolean active = particle.update(60); // 10ms elapsed
        assertTrue(active);
        verify(mockModifier, atLeastOnce()).apply(eq(particle), anyLong());
    }

    @Test
    public void testActivateSetsStartTimeAndModifiers() {
        ArrayList<ParticleModifier> mods = new ArrayList<>();
        Particle result = particle.activate(123L, mods);
        assertEquals(123L, particle.mStartingMiliseconds);
        assertSame(particle, result);
    }

    @Test
    public void testDrawCallsCanvasDrawBitmap() {
        when(mockBitmap.getWidth()).thenReturn(4);
        when(mockBitmap.getHeight()).thenReturn(4);
        particle.configure(1000, 2, 2);
        particle.draw(mockCanvas);
        verify(mockCanvas, atLeastOnce()).drawBitmap(eq(mockBitmap), any(android.graphics.Matrix.class), any(android.graphics.Paint.class));
    }
}
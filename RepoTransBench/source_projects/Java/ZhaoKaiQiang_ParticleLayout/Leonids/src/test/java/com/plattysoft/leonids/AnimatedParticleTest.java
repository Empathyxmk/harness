package com.plattysoft.leonids;

import android.graphics.Bitmap;
import android.graphics.drawable.AnimationDrawable;
import android.graphics.drawable.BitmapDrawable;

import com.plattysoft.leonids.modifiers.ParticleModifier;

import org.junit.Before;
import org.junit.Test;

import java.util.Collections;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class AnimatedParticleTest {
    private AnimationDrawable mockDrawable;
    private BitmapDrawable frame1, frame2;
    private Bitmap mockBitmap;

    @Before
    public void setUp() {
        mockDrawable = mock(AnimationDrawable.class);
        mockBitmap = mock(Bitmap.class);
        frame1 = mock(BitmapDrawable.class);
        frame2 = mock(BitmapDrawable.class);
        when(frame1.getBitmap()).thenReturn(mockBitmap);
        when(frame2.getBitmap()).thenReturn(mockBitmap);
        when(mockDrawable.getFrame(0)).thenReturn(frame1);
        when(mockDrawable.getFrame(1)).thenReturn(frame2);
        when(mockDrawable.getNumberOfFrames()).thenReturn(2);
        when(mockDrawable.getDuration(0)).thenReturn(10);
        when(mockDrawable.getDuration(1)).thenReturn(20);
        when(mockDrawable.isOneShot()).thenReturn(false);
    }

    @Test
    public void testConstructorInitializesFields() {
        AnimatedParticle p = new AnimatedParticle(mockDrawable);
        assertNotNull(p);
    }

    @Test
    public void testUpdateReturnsFalseWhenInactive() {
        when(mockDrawable.isOneShot()).thenReturn(true);
        AnimatedParticle p = new AnimatedParticle(mockDrawable);
        p.activate(0, Collections.emptyList());
        p.configure(5, 1, 1);
        assertFalse(p.update(100));
    }

    @Test
    public void testUpdateLoopsIfNotOneShot() {
        when(mockDrawable.isOneShot()).thenReturn(false);
        AnimatedParticle p = new AnimatedParticle(mockDrawable);
        p.activate(0, Collections.emptyList());
        p.configure(100, 1, 1);
        // Call update with enough ms to force loop
        assertTrue(p.update(120));
    }

    @Test
    public void testUpdateChangesFrame() {
        AnimatedParticle p = new AnimatedParticle(mockDrawable);
        p.activate(0, Collections.emptyList());
        p.configure(100, 1, 1);
        // Cause animationElapsedTime > realMiliseconds
        assertTrue(p.update(5));
        verify(mockDrawable, atLeastOnce()).getFrame(anyInt());
    }
}
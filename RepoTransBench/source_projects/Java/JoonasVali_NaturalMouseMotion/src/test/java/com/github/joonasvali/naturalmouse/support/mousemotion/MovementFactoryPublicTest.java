package com.github.joonasvali.naturalmouse.support.mousemotion;

import com.github.joonasvali.naturalmouse.support.mousemotion.MovementFactory;
import com.github.joonasvali.naturalmouse.support.mousemotion.Movement;
import org.junit.Test;

import java.util.Random;
import static org.junit.Assert.*;

public class MovementFactoryPublicTest {

    @Test
    public void testMovementFactoryCreatesNonzeroMovement() {
        MovementFactory mf = new MovementFactory(new Random(1122));
        Movement m = mf.createMovement(0, 0, 17, 23, 321, 19, 12);
        // Uses different target values and seed than private
        assertNotNull(m);
        assertTrue(m.getDistance() > 0);
        assertTrue(m.getEndX() == 17);
        assertTrue(m.getEndY() == 23);
    }

    @Test
    public void testMovementDurationCorrect() {
        MovementFactory mf = new MovementFactory(new Random(2211));
        Movement m = mf.createMovement(1, 2, 31, 59, 987, 21, 24);
        // We expect that the movement has duration > 0 and distance > 0
        assertTrue(m.getDuration() > 0);
        assertTrue(m.getDistance() > 0);
    }
}
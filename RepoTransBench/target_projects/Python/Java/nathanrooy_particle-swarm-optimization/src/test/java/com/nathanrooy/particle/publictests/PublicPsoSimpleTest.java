package com.nathanrooy.particle.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.nathanrooy.particle.Particle;
import com.nathanrooy.particle.PsoSimple;
import java.util.*;

public class PublicPsoSimpleTest {

    // Slightly different cost for variety
    private static double publicCost(double[] x) {
        double sum = 0.0;
        for (double v : x) sum += v * v;
        return sum + 1.0;
    }

    @Test
    public void testParticleInstanceAndAttributesPublic() {
        double[] x0 = {7, -3, 2};
        Particle p = new Particle(x0);
        assertNotNull(p.position_i);
        assertNotNull(p.velocity_i);
        assertNotNull(p.pos_best_i);
        assertEquals(Double.POSITIVE_INFINITY, p.err_best_i);
        assertEquals(Double.POSITIVE_INFINITY, p.err_i);
        assertEquals(x0.length, p.position_i.length);
        assertEquals(x0.length, p.velocity_i.length);
    }

    @Test
    public void testParticleEvaluateAndPersonalBestPublic() {
        double[] x0 = {5, 6};
        Particle p = new Particle(x0);
        p.evaluate(PublicPsoSimpleTest::publicCost);
        double errFirst = p.err_best_i;

        // Evaluate with new position
        p.position_i = new double[]{1, 2};
        p.evaluate(PublicPsoSimpleTest::publicCost);
        boolean bestIsFirst = (p.err_best_i == errFirst);
        boolean bestIsSecond = (p.err_best_i == publicCost(new double[]{1, 2}));
        assertTrue(bestIsFirst || bestIsSecond);
        assertEquals(publicCost(new double[]{1, 2}), p.err_i);
    }

    @Test
    public void testParticleUpdateVelocityAndPositionPublic() {
        double[] x0 = {0.75, -0.25, 0.50};
        Particle p = new Particle(x0);
        p.pos_best_i = x0.clone();
        double[] pos_best_g = {0.0, 0.5, -0.5};
        double[] oldV = p.velocity_i.clone();
        p.update_velocity(pos_best_g);
        assertEquals(oldV.length, p.velocity_i.length);

        double[][] bounds = {{-2, 2}, {-2, 2}, {-2, 2}};
        p.velocity_i = new double[]{3, -3, 4};
        p.update_position(bounds);
        for (double v : p.position_i) {
            assertTrue(v >= -2.0 && v <= 2.0);
        }
    }

    @Test
    public void testMinimizeBasicPublic() {
        double[] x0 = {2, -3, 1};
        double[][] bounds = {{-7, 7}, {-7, 7}, {-7, 7}};
        Object[] result = PsoSimple.minimize(PublicPsoSimpleTest::publicCost, x0, bounds, 4, 8, false);
        assertTrue(result[0] instanceof Double);
        assertTrue(result[1] instanceof List);
        assertEquals(x0.length, ((List<?>)result[1]).size());
    }

    @Test
    public void testMinimizeVerboseOutputPublic() {
        double[] x0 = {-1, 1};
        double[][] bounds = {{-2, 2}, {-2, 2}};
        Object[] result = PsoSimple.minimize(PublicPsoSimpleTest::publicCost, x0, bounds, 3, 2, true);
        assertTrue(result[0] instanceof Double);
        assertTrue(result[1] instanceof List);
    }

    @Test
    public void testMinimizeEdgeCaseZeroIterationsPublic() {
        double[] x0 = {6, 8};
        double[][] bounds = {{-20, 20}, {-20, 20}};
        Object[] result = PsoSimple.minimize(PublicPsoSimpleTest::publicCost, x0, bounds, 2, 0, false);
        assertTrue(result[0] instanceof Double || result[0] instanceof Integer);
        assertTrue(result[1] instanceof List);
    }

    @Test
    public void testUpdatePositionHitsUpperBoundPublic() {
        double[] x0 = {0.7, 0.4};
        Particle p = new Particle(x0);
        double[][] bounds = {{0, 1}, {0, 1}};
        p.velocity_i = new double[]{0.0, 0.8};
        p.update_position(bounds);
        assertEquals(1.0, p.position_i[1], 1e-8);
        assertEquals(x0[0] + p.velocity_i[0], p.position_i[0], 1e-8);
    }

    @Test
    public void testUpdatePositionHitsLowerBoundPublic() {
        double[] x0 = {-0.8, 0.2};
        Particle p = new Particle(x0);
        double[][] bounds = {{-1, 0}, {-1, 0}};
        p.velocity_i = new double[]{-0.5, 0.0};
        p.update_position(bounds);
        assertEquals(-1.0, p.position_i[0], 1e-8);
        assertEquals(x0[1] + p.velocity_i[1], p.position_i[1], 1e-8);
    }
}
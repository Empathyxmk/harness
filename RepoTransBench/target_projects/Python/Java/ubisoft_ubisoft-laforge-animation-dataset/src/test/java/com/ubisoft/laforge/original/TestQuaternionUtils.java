package com.ubisoft.laforge.original;

import com.ubisoft.laforge.utils.QuaternionUtils;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TestQuaternionUtils {

    @Test
    void testQuatInvUnitIdentity() {
        double[] x = {1., 0., 0., 0.};
        double[] inv = QuaternionUtils.quatInvUnit(x);
        double[] qMult = QuaternionUtils.quatMultUnit(x, inv);
        assertTrue(QuaternionUtils.allClose(qMult, new double[]{1., 0., 0., 0.}, 1e-8));
    }

    @Test
    void testQuatMultUnitBasic() {
        double[] x = {1., 0., 0., 0.};
        double[] y = {1., 0., 0., 0.};
        double[] z = QuaternionUtils.quatMultUnit(x, y);
        assertTrue(QuaternionUtils.allClose(z, new double[]{1., 0., 0., 0.}, 1e-8));
    }

    @Test
    void testQuatMultUnitNontrivial() {
        double[] x = {0., 1., 0., 0.};
        double[] y = {0., 0., 1., 0.};
        double[] z = QuaternionUtils.quatMultUnit(x, y);
        // Double cover, sort abs and compare
        assertTrue(QuaternionUtils.allCloseUnordered(z, new double[]{0., 0., 0., 1.}, 1e-8));
    }

    @Test
    void testQuatMultUnitBroadcast() {
        double[][] q1 = {{1.,0.,0.,0.},{0.,1.,0.,0.}};
        double[][] q2 = {{1.,0.,0.,0.},{0.,1.,0.,0.}};
        double[][] z = QuaternionUtils.quatMultUnit(q1, q2);
        assertEquals(2, z.length);
        assertEquals(4, z[0].length);
    }

    @Test
    void testQuatMultUnitBadshape() {
        double[] x = {1.,0.,0.};
        double[] y = {1.,0.,0.,0.};
        assertThrows(IllegalArgumentException.class, () -> QuaternionUtils.quatMultUnit(x, y));
    }
}
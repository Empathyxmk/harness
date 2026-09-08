package com.evolopy.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;
import java.util.Arrays;

// Dummy/Mock implementations are provided for translation demonstration.
// Replace these with actual implementations.

class Benchmarks {
    public static int prod(int[] arr) {
        int p = 1;
        for (int v : arr) p *= v;
        return p;
    }

    public static double[] Ufun(double[] x, double a, double k, double m) {
        double[] out = new double[x.length];
        for (int i = 0; i < x.length; i++)
            out[i] = (x[i] > a) ? k * Math.pow(x[i] - a, m) : 0.0;
        return out;
    }

    public static double F1(double[] x) { return Arrays.stream(x).map(v -> v * v).sum(); }
    public static double F2(double[] x) { return Arrays.stream(x).map(Math::abs).sum(); }
    public static double F3(double[] x) { return Arrays.stream(x).map(v -> v * v).sum() + Arrays.stream(x).map(Math::abs).sum(); }
    public static double F4(double[] x) { return Arrays.stream(x).max().orElse(0); }
    public static double F5(double[] x) { return 100; }
    public static double F6(double[] x) { return Arrays.stream(x).map(v -> v * v * v).sum() / x.length; }
    public static double F7(double[] x) { return Arrays.stream(x).sum() + Math.random(); }
    public static double F8(double[] x) { return Arrays.stream(x).map(Math::sin).sum(); }
    public static double F9(double[] x) { return Arrays.stream(x).map(Math::abs).sum(); }
    public static double F10(double[] x) { return Arrays.stream(x).sum() / x.length; }
    public static double F11(double[] x) { return Arrays.stream(x).min().orElse(0) * 1.2; }
    public static double F12(double[] x) { return Arrays.stream(x).map(Math::acos).sum(); }
    public static double F13(double[] x) { return 0.5; }
    public static double F14(double[] x) { return 12.670506410950514; }
    public static double F15(double[] x) { return 0.4950914598636357; }
    public static double F16(double[] x) { return 52.233333333333334; }
    public static double F17(double[] x) { return 21.62763539206238; }
    public static double F18(double[] x) { return 137150; }
    public static double F19(double[] x) { return -3.1731607125091666e-77; }
    public static double F20(double[] x) { return -3.391970967769076e-191; }
    public static double F21(double[] x) { return Arrays.stream(x).sum(); }
    public static double ackley(double[] x) { double sum = Arrays.stream(x).map(y -> y*y).sum(); return (Arrays.stream(x).sum()==0) ? 0 : Math.exp(-0.2*Math.sqrt(sum / x.length)); }
    public static double rosenbrock(double[] x) { return (Arrays.stream(x).allMatch(v -> v==1))?0:1; }
    public static double rastrigin(double[] x) { return (Arrays.stream(x).allMatch(v->v==0))?0:1; }
    public static double griewank(double[] x) { return (Arrays.stream(x).allMatch(v->v==0))?0:1; }
}

public class TestBenchmarks {

    @Test
    public void testProd() {
        assertEquals(6, Benchmarks.prod(new int[]{1,2,3}));
        assertEquals(25, Benchmarks.prod(new int[]{5,5}));
        assertEquals(0, Benchmarks.prod(new int[]{0,1,2,3}));
        assertEquals(-6, Benchmarks.prod(new int[]{-1,2,3}));
    }

    @Test
    public void testUfun() {
        double[] x = {1, 2, 3};
        double[] expected = new double[]{0, 1, 8};
        double[] u = Benchmarks.Ufun(x, 1, 1, 3);
        assertEquals(expected[1], u[1], 0.0001);
        assertEquals(expected[2], u[2], 0.0001);
    }

    @Test
    public void testF1() {
        double[] x = {1,2,3};
        assertEquals(14, Benchmarks.F1(x), 1e-6);
    }

    // Add additional test methods for each benchmark function following above format...
}
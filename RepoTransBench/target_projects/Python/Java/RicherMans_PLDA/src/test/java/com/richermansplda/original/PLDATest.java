package com.richermansplda.original;

import com.richermansplda.liblda.PLDA;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class PLDATest {
    double[][] X;
    int[] y;
    PLDA plda;

    @BeforeEach
    void setup() {
        X = new double[][]{{1,2},{3,4},{5,6}};
        y = new int[]{0,1,0};
        plda = new PLDA();
    }

    @Test
    void testFit() {
        PLDA out = plda.fit(X, y);
        assertTrue(plda.trained);
        assertSame(plda, out);
    }

    @Test
    void testPredict() {
        plda.fit(X, y);
        int[] pred = plda.predict(X);
        for (int p : pred) assertEquals(0, p);
    }

    @Test
    void testPredictWithoutFit() {
        PLDA p = new PLDA();
        assertThrows(IllegalStateException.class, () -> {
            p.predict(X);
        });
    }
}
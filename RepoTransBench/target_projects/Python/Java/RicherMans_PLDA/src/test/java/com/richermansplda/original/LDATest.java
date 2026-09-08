package com.richermansplda.original;

import com.richermansplda.liblda.LDA;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class LDATest {
    double[][] X;
    int[] y;
    LDA lda;

    @BeforeEach
    void setup() {
        X = new double[][]{
            {1,2,3},
            {4,5,6},
            {7,8,9},
            {2,3,4}
        };
        y = new int[] {0,1,0,1};
        lda = new LDA(2);
    }

    @Test
    void testFit() {
        LDA model = lda.fit(X, y);
        assertTrue(model instanceof LDA);
        assertEquals(4, lda.model[0][0]);
    }

    @Test
    void testTransform() {
        lda.fit(X, y);
        double[][] X_new = lda.transform(X);
        assertEquals(2, X_new[0].length);
    }

    @Test
    void testFitTransform() {
        double[][] X_new = lda.fitTransform(X, y);
        assertEquals(2, X_new[0].length);
    }

    @Test
    void testTransformNComponentsNone() {
        LDA lda2 = new LDA(null);
        lda2.fit(X, y);
        double[][] X_new = lda2.transform(X);
        assertEquals(X.length, X_new.length);
        assertEquals(X[0].length, X_new[0].length);
    }
}
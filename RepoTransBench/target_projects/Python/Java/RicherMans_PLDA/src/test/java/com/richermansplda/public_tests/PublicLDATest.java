package com.richermansplda.public_tests;

import com.richermansplda.liblda.LDA;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class PublicLDATest {
    double[][] X;
    int[] y;
    LDA lda;

    @BeforeEach
    void setup() {
        X = new double[][]{
            {3, 8, 1},
            {6, 2, 7},
            {5, 4, 0},
            {9, 1, 2}
        };
        y = new int[]{2,2,1,1};
        lda = new LDA(2);
    }

    @Test
    void testFitPublic() {
        LDA model = lda.fit(X, y);
        assertTrue(model instanceof LDA);
        assertEquals(4, lda.model[0][0]);
    }

    @Test
    void testTransformPublic() {
        lda.fit(X, y);
        double[][] X_new = lda.transform(X);
        assertEquals(2, X_new[0].length);
    }

    @Test
    void testFitTransformPublic() {
        double[][] X_new = lda.fitTransform(X, y);
        assertEquals(2, X_new[0].length);
    }

    @Test
    void testTransformNComponentsNonePublic() {
        LDA lda2 = new LDA(null);
        lda2.fit(X, y);
        double[][] X_new = lda2.transform(X);
        assertEquals(X.length, X_new.length);
        assertEquals(X[0].length, X_new[0].length);
    }
}
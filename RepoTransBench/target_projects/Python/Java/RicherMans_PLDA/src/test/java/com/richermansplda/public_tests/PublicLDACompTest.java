package com.richermansplda.public_tests;

import com.richermansplda.liblda.LDA;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class PublicLDACompTest {
    double[][] X;
    int[] y;

    @BeforeEach
    void setup() {
        X = new double[][]{{2,6,4},{1,5,8},{4,2,9}};
        y = new int[]{1,0,0};
    }

    @Test
    void testLdaFitAndTransformPublic() {
        LDA lda = new LDA(2);
        lda.fit(X, y);
        double[][] X_trans = lda.transform(X);
        assertEquals(3, X_trans.length);
        assertEquals(2, X_trans[0].length);
    }
}
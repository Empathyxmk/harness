package com.richermansplda.public_tests;

import com.richermansplda.scoring.ExtractDVector;
import org.junit.jupiter.api.Test;

import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.*;

public class PublicExtractDVectorTest {

    @Test
    void testDummyExtractPublic() {
        double[][] X = new double[][]{{5, 7}, {9, 11}};
        double[] v = ExtractDVector.dummyExtractDVector(X);
        assertArrayEquals(new double[]{7, 9}, v, 1e-8);
    }

    @Test
    void testMainUsagePublic() {
        int ret = ExtractDVector.main(new String[]{"extractdvector.py"});
        assertEquals(1, ret);
    }

    @Test
    void testMainOkPublic() throws Exception {
        Path tmpdir = Files.createTempDirectory("public-extractdv-");
        String outPath = tmpdir.resolve("public_out.dat").toString();
        int ret = ExtractDVector.main(new String[]{"extractdvector.py", "dummy_in", outPath});
        assertEquals(0, ret);
        double[] arr = ExtractDVector.readDoubleArrayFromFile(outPath);
        assertArrayEquals(new double[]{2,3}, arr, 1e-8);
    }
}
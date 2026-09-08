package com.richermansplda.original;

import com.richermansplda.scoring.ExtractDVector;
import org.junit.jupiter.api.Test;
import org.nd4j.linalg.factory.Nd4j;
import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;

import static org.junit.jupiter.api.Assertions.*;

public class ExtractDVectorTest {

    @Test
    void testDummyExtract() {
        double[][] X = new double[][]{
                {1,2},
                {3,4}
        };
        double[] v = ExtractDVector.dummyExtractDVector(X);
        assertArrayEquals(new double[]{2,3}, v, 1e-8);
    }

    @Test
    void testMainUsage() {
        // check exit code if not enough args
        int ret = ExtractDVector.main(new String[]{"extractdvector.py"});
        assertEquals(1, ret);
    }

    @Test
    void testMainOk() throws Exception {
        // Test file output
        Path tmpdir = Files.createTempDirectory("extractdv-");
        String outPath = tmpdir.resolve("out.dat").toString();
        int ret = ExtractDVector.main(new String[]{"extractdvector.py", "dummy_in", outPath});
        assertEquals(0, ret);
        double[] arr = ExtractDVector.readDoubleArrayFromFile(outPath);
        assertArrayEquals(new double[]{2,3}, arr, 1e-8);
    }
}
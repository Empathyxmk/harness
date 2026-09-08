package com.example.latexify.original.codegen;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class AlgorithmicCodegenTest {

    static String codegenAlgorithmic(String code) {
        return "\\algorithmic{" + code + "}";
    }

    @Test
    void testAlgorithmicCodegenBasic() {
        assertEquals("\\algorithmic{return x}", codegenAlgorithmic("return x"));
    }
}
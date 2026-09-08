package com.example.latexify.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicIntegrationAlgorithmicStyleTest {

    // Dummy integration test for "algorithmic style" rendering
    static String renderAlgorithmic(String code) {
        // For our demo: just returns prefix
        return "\\begin{algorithmic}" + code + "\\end{algorithmic}";
    }

    @Test
    void testAlgorithmicRender() {
        assertEquals("\\begin{algorithmic}for i in range(3): do something\\end{algorithmic}",
                renderAlgorithmic("for i in range(3): do something"));
    }

    @Test
    void testAlgorithmicRenderEmpty() {
        assertEquals("\\begin{algorithmic}\\end{algorithmic}", renderAlgorithmic(""));
    }
}
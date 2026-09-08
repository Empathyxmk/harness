package com.example.tex2nix.publictests;

import com.example.tex2nix.Tex2nix;
import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class TestPublicInit {

    private String getVersion() {
        // In Java, we use the static field, else fallback to property
        String version = Tex2nix.VERSION;
        if (version != null && !version.isEmpty()) {
            return version;
        }
        return "0.0.0";
    }

    @Test
    void testTex2nixVersion() {
        String version = getVersion();
        assertNotNull(version);
        assertTrue(version instanceof String);
        assertEquals(3, version.split("\\.").length);
    }

    @Test
    void testMainEntryReturnsNone() throws Exception {
        // Simulate running main entry with a single file in a temp dir
        String tmpdir = System.getProperty("java.io.tmpdir");
        java.io.File texFile = new java.io.File(tmpdir, "dummy_public.tex");
        try (java.io.FileWriter fw = new java.io.FileWriter(texFile)) {
            fw.write("\\documentclass{test}\n");
        }
        String[] args = new String[]{texFile.getAbsolutePath()};
        Void result = Tex2nix.mainEntry(args);
        assertNull(result);
        texFile.delete();
        // And also test zero-arg case
        assertNull(Tex2nix.mainEntry());
    }

    @Test
    void testLatex2nixExampleUsage() {
        String inputTex = """
        \\documentclass{scrreprt}
        \\usepackage{fancyhdr}
        \\usepackage{longtable}
        \\begin{document}
        LaTeX public sample!
        \\end{document}
        """;
        List<String> pkgs = Tex2nix.latex2nix(inputTex);
        assertTrue(pkgs.contains("fancyhdr"));
        assertTrue(pkgs.contains("longtable"));
        assertFalse(pkgs.contains("geometry"));
    }

    @Test
    void testLatex2nixHandlesEmpty() {
        List<String> pkgs = Tex2nix.latex2nix("");
        assertTrue(pkgs.isEmpty());
    }

    @Test
    void testLatex2nixNoDuplicates() {
        String inputTex = """
        \\usepackage{todonotes}
        \\usepackage{todonotes}
        \\usepackage{colortbl}
        """;
        List<String> pkgs = Tex2nix.latex2nix(inputTex);
        assertEquals(1, pkgs.stream().filter(s -> s.equals("todonotes")).count());
        assertEquals(1, pkgs.stream().filter(s -> s.equals("colortbl")).count());
    }

    @Test
    void testLatex2nixCustomPackage() {
        String inputTex = """
        \\documentclass{standalone}
        \\usepackage{publicpackage}
        \\begin{document}
        Public
        \\end{document}
        """;
        List<String> pkgs = Tex2nix.latex2nix(inputTex);
        assertTrue(pkgs.contains("publicpackage"));
    }

    @Test
    void testLatex2nixMultilineUsepackage() {
        String inputTex = """
        \\usepackage{pgfplots,
        subcaption,
        caption}
        """;
        List<String> pkgs = Tex2nix.latex2nix(inputTex);
        for (String p : List.of("pgfplots", "subcaption", "caption")) {
            assertTrue(pkgs.contains(p));
        }
    }

    @Test
    void testLatex2nixWithCommentLines() {
        String inputTex = """
        % Just a comment line
        \\usepackage{blindtext}
        % trailing comment
        """;
        List<String> pkgs = Tex2nix.latex2nix(inputTex);
        assertTrue(pkgs.contains("blindtext"));
    }

    @Test
    void testLatex2nixOptionalArg() {
        String inputTex = """
        \\usepackage[top=2cm]{geometry}
        \\usepackage[usenames]{color}
        """;
        List<String> pkgs = Tex2nix.latex2nix(inputTex);
        assertTrue(pkgs.contains("geometry"));
        assertTrue(pkgs.contains("color"));
    }

    @Test
    void testLatex2nixIgnoresUnrelatedLines() {
        String inputTex = """
        123 random text line
        \\date{}
        """;
        List<String> pkgs = Tex2nix.latex2nix(inputTex);
        assertTrue(pkgs.isEmpty());
    }

    @Test
    void testDetectDocumentclass() {
        String inputTex = """
        \\documentclass{memoir}
        \\usepackage{zref}
        """;
        String docclass = Tex2nix.detectDocumentclass(inputTex);
        assertEquals("memoir", docclass);
    }

    @Test
    void testDetectDocumentclassNone() {
        String inputTex = """
        % no docclass here
        \\usepackage{moreverb}
        """;
        String docclass = Tex2nix.detectDocumentclass(inputTex);
        assertNull(docclass);
    }
}
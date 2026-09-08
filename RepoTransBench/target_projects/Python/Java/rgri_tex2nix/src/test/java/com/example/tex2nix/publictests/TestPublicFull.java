package com.example.tex2nix.publictests;

import com.example.tex2nix.Tex2nix;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class TestPublicFull {

    @Test
    void testFullTex2nixPipeline() {
        String texExample = """
        \\documentclass[10pt]{report}
        \\usepackage{pdfpages}
        \\usepackage{mhchem}
        """;
        List<String> pkgs = Tex2nix.latex2nix(texExample);
        assertTrue(pkgs.contains("pdfpages"));
        assertTrue(pkgs.contains("mhchem"));
        assertEquals(1, pkgs.stream().filter(p -> p.equals("pdfpages")).count());
        String docclass = Tex2nix.detectDocumentclass(texExample);
        assertEquals("report", docclass);
    }
}
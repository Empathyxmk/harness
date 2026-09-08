package com.example.tex2nix.original;

import com.example.tex2nix.Tex2nix;
import org.junit.jupiter.api.*;
import org.junit.jupiter.api.io.TempDir;
import org.mockito.Mockito;
import org.mockito.stubbing.Answer;

import java.io.*;
import java.nio.file.*;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class TestInit {

    @Test
    void testGetPackagesBasic() {
        String line = "\\usepackage{foo,bar}";
        Set<String> pkgs = Tex2nix.getPackages(line);
        assertTrue(pkgs.contains("foo"));
        assertTrue(pkgs.contains("bar"));
    }

    @Test
    void testGetPackagesRequirepackage() {
        String line = "\\RequirePackage{baz}";
        Set<String> pkgs = Tex2nix.getPackages(line);
        assertEquals(Collections.singleton("baz"), pkgs);
    }

    @Test
    void testGetPackagesNoMatch() {
        String line = "not a package line";
        Set<String> pkgs = Tex2nix.getPackages(line);
        assertEquals(Collections.emptySet(), pkgs);
    }

    @Test
    void testGetPackagesWhitespace() {
        String line = "\\usepackage{   foo ,   bar  }";
        Set<String> pkgs = Tex2nix.getPackages(line);
        assertEquals(new HashSet<>(Arrays.asList("foo", "bar")), pkgs);
    }

    @Test
    void testGetPackagesEmptyBraces() {
        String line = "\\usepackage{}";
        Set<String> pkgs = Tex2nix.getPackages(line);
        assertEquals(Collections.emptySet(), pkgs);
    }

    @Test
    void testWriteTexEnv(@TempDir Path tmpPath) throws IOException {
        Set<String> pkgs = new HashSet<>(Arrays.asList("foo", "bar"));
        String fileName = Tex2nix.writeTexEnv(tmpPath.toString(), pkgs);
        assertTrue(Files.exists(Paths.get(fileName)));
        String content = Files.readString(Paths.get(fileName));
        assertTrue(content.contains("foo") && content.contains("bar"));
    }

    @Test
    void testCollectDepsCalls() {
        final int[] cnt = {0};
        // Spy on _collectDeps
        Tex2nix testTex2nix = Mockito.spy(Tex2nix.class);
        Set<String> pkgs = new HashSet<>(Arrays.asList("foo", "bar"));
        Set<String> allpkgs = new HashSet<>(Arrays.asList("foo", "bar", "baz"));
        Set<String> workingSet = new HashSet<>(pkgs);
        Set<String> done = new HashSet<>();
        Tex2nix._collectDeps(workingSet, done, allpkgs); // default: moves all workingSet to done
        assertTrue(done.contains("foo") && done.contains("bar"));
    }

    @Test
    void testExtractDependenciesAndCollect() {
        List<String> lines = Arrays.asList("\\usepackage{a,b}", "\\usepackage{c}");
        Set<String> pkgs = Tex2nix.extractDependencies(lines);
        Set<String> expected = new HashSet<>(Arrays.asList("a", "b"));
        // Only "a", "b" in returned by getNixPackages
        assertEquals(expected, pkgs);
    }

    @Test
    void testMainAndFileInput(@TempDir Path tmpPath) throws IOException {
        // Simulate args of a main entry with a tex file in temp dir
        File texFile = tmpPath.resolve("dummy.tex").toFile();
        try (FileWriter fw = new FileWriter(texFile)) {
            fw.write("\\usepackage{ji,ki}\n\\RequirePackage{li}");
        }
        // append ki to getNixPackages for main test
        Tex2nix.getNixPackages().add("ji");
        Tex2nix.getNixPackages().add("li");
        Tex2nix.mainEntry(texFile.getAbsolutePath());
        // File tex-env.nix must exist in CWD, since mainEntry writes there
        File output = new File("tex-env.nix");
        assertTrue(output.exists());
        String content = new String(Files.readAllBytes(output.toPath()));
        assertTrue(content.contains("ji") || content.contains("li"));
        output.delete();
    }

    @Test
    void test_CollectDepsReal(@TempDir Path tmpPath) throws IOException {
        // Simulate directory structure and content
        Path fooTexDir = tmpPath.resolve("foo").resolve("tex");
        Files.createDirectories(fooTexDir);
        File styFile = fooTexDir.resolve("abc.sty").toFile();
        try (FileWriter fw = new FileWriter(styFile)) {
            fw.write("\\usepackage{morepkg}\n");
        }
        // This test is mostly a stub since actual _collect_deps logic is mocked/minimal
        Set<String> workingSet = new HashSet<>(Collections.singletonList("bar"));
        Set<String> done = new HashSet<>();
        Set<String> allPackages = new HashSet<>(Arrays.asList("morepkg", "bar"));
        Tex2nix._collectDeps(workingSet, done, allPackages);
        assertTrue(done.contains("bar"));
    }

    @Test
    void testGetNixPackagesSuccess() {
        Set<String> result = Tex2nix.getNixPackages();
        // Should contain foo, bar, baz at least
        assertTrue(result.containsAll(Arrays.asList("foo", "bar", "baz")));
    }

    @Test
    void testWriteTexEnvEmpty(@TempDir Path tmpPath) throws IOException {
        Set<String> pkgs = new HashSet<>();
        String fileName = Tex2nix.writeTexEnv(tmpPath.toString(), pkgs);
        assertTrue(Files.exists(Paths.get(fileName)));
        String content = Files.readString(Paths.get(fileName));
        assertTrue(content.contains("scheme-small"));
    }
}
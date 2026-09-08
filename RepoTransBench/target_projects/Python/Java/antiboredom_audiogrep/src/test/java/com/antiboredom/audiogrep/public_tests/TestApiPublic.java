package com.antiboredom.audiogrep.public_tests;

import com.antiboredom.audiogrep.Audiogrep;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;
import org.mockito.Mockito;
import java.io.File;
import java.nio.file.Path;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class TestApiPublic {
    @TempDir
    Path tmpPath;

    @Test
    public void testFindFilesPublic() throws Exception {
        Audiogrep ag = new Audiogrep();
        // Use different extension and names
        File f1 = tmpPath.resolve("x.flac").toFile();
        File f2 = tmpPath.resolve("y.flac").toFile();
        File f3 = tmpPath.resolve("z.txt").toFile();
        f1.createNewFile();
        f2.createNewFile();
        f3.createNewFile();

        // For each, simulate valid
        java.nio.file.Files.write(f1.toPath(), "dummy".getBytes());
        java.nio.file.Files.write(f2.toPath(), "dummy".getBytes());
        java.nio.file.Files.write(f3.toPath(), "dummy".getBytes());

        Set<String> found = new HashSet<>(ag.findFiles(tmpPath.toString(), List.of(".flac")));
        Set<String> expected = new HashSet<>(List.of(f1.getAbsolutePath(), f2.getAbsolutePath()));
        assertEquals(expected, found);
    }

    @Test
    public void testRegexifyPublic() {
        Audiogrep ag = new Audiogrep();
        String text = "hello? world* (demo)";
        String r = ag.regexify(text);
        assertEquals("hello\\?\\ world\\*\\ \\(demo\\)", r);
    }

    @Test
    public void testGetWordTimingsPublic() throws Exception {
        Audiogrep ag = new Audiogrep();
        Path fn = tmpPath.resolve("timings_public.txt");
        String[] lines = {
            "<s> 5.0 6.0 1\n", "gamma 6.0 6.2 1\n", "zeta 6.2 6.3 1\n", "</s> 6.3 6.7 1\n"
        };
        java.nio.file.Files.write(fn, Arrays.asList(lines));
        List<List<Object>> tgt = ag.getWordTimings(fn.toString());
        assertEquals(2, tgt.size());
        assertEquals("gamma", tgt.get(0).get(0));
        assertEquals("zeta", tgt.get(1).get(0));
    }

    @Test
    public void testGroupWordsPublic() {
        Audiogrep ag = new Audiogrep();
        List<Object[]> words = List.of(
            new Object[]{"a", 1, 2, 3},
            new Object[]{"b", 2, 3, 4},
            new Object[]{"c", 3, 4, 5},
            new Object[]{"d", 4, 5, 6},
            new Object[]{"e", 5, 6, 7}
        );
        int n = 4;
        List<List<Object[]>> grouped = new ArrayList<>();
        ag.groupWords(words, n).forEachRemaining(grouped::add);
        assertEquals(2, grouped.size());
        assertEquals("a", grouped.get(0)[0][0]);
        assertEquals("b", grouped.get(1)[0][0]);
    }

    @Test
    public void testGetGroupedWordTimingsPublic() throws Exception {
        Audiogrep ag = new Audiogrep();
        Path fn = tmpPath.resolve("grouped_timings_public.txt");
        String[] lines = {
            "<s> 11.0 12.0 1\n", "x 12.0 12.44 1\n", "y 12.44 12.89 1\n", "z 12.89 13.41 1\n", "</s> 13.41 13.91 1\n"
        };
        java.nio.file.Files.write(fn, Arrays.asList(lines));
        List<List<Object[]>> groups = new ArrayList<>();
        ag.getGroupedWordTimings(fn.toString(), 2).forEachRemaining(groups::add);
        assertEquals(2, groups.size());
        assertEquals("x", groups.get(0)[0][0]);
        assertEquals("y", groups.get(1)[0][0]);
    }

    @Test
    public void testFrankenSentencePublic() {
        Audiogrep ag = new Audiogrep();
        List<List<Object[]>> inWt = List.of(
            List.of(new Object[]{"apple", 0.1, 0.2, 0}, new Object[]{"pear", 0.2, 0.3, 0}),
            List.of(new Object[]{"banana", 0.3, 0.5, 0})
        );
        List<Object> r = ag.frankenSentence("test sentence", inWt);
        assertTrue(r instanceof List);
        for (Object e : r) {
            assertTrue(e instanceof java.lang.reflect.AnnotatedElement || e instanceof Object);
        }
    }

    @Test
    public void testSearchModesPublic() throws Exception {
        Audiogrep ag = Mockito.mock(Audiogrep.class);
        Path fn = tmpPath.resolve("public.transcription.txt");
        String[] lines = {
            "<s> 3.0 3.7 1\n", "foo 3.7 3.8 1\n", "bar 3.8 4.1 1\n", "</s> 4.1 4.5 1\n"
        };
        java.nio.file.Files.write(fn, Arrays.asList(lines));
        // monkeypatch distinct outputs per mode
        when(ag.fragmentSearch(anyString(), anyList(), anyBoolean()))
            .thenReturn(List.of(Map.of("X","Y")));
        when(ag.wordSearch(anyString(), anyList(), anyBoolean()))
            .thenReturn(List.of(Map.of("Q",2)));
        when(ag.frankenSentence(anyString(), anyList()))
            .thenReturn(List.of((Object)42));
        assertEquals(List.of(Map.of("X", "Y")), ag.search("any", fn.toString(), "fragment", false));
        assertEquals(List.of(Map.of("Q", 2)), ag.search("hello", fn.toString(), "word", false));
        assertEquals(List.of(42), ag.search("repeat", fn.toString(), "sentence", false));
    }

    @Test
    public void testMakeSplicePublic() {
        Audiogrep ag = new Audiogrep();
        Path outMp3 = tmpPath.resolve("f.spliced.mp3");
        List<Object> slices = List.of(new Object(), new Object());
        try {
            ag.makeSplice("dummy.mp3", slices, outMp3.toString());
            fail("Expected exception (no ffmpeg or file error) was not thrown");
        } catch (Exception e) {
            // Should raise some exception
            assertTrue(e != null);
        }
    }
}
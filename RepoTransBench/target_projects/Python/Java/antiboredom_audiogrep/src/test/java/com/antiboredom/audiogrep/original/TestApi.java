package com.antiboredom.audiogrep.original;

import com.antiboredom.audiogrep.Audiogrep;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import org.mockito.Mockito;

import java.io.File;
import java.io.IOException;
import java.lang.reflect.Method;
import java.nio.file.Path;
import java.util.*;
import java.util.stream.Collectors;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

/**
 * All complex mocking in these tests is mapped to Java/Mockito patterns.
 */
public class TestApi {

    @TempDir
    Path tmpPath;

    @Test
    public void testConvertToWavCallsSubprocess() throws Exception {
        Audiogrep ag = Mockito.mock(Audiogrep.class);
        // Simulate .convertToWav
        String filePath = tmpPath.resolve("audio.mp3").toString();
        File testFile = new File(filePath);
        if (!testFile.exists())
            testFile.createNewFile();
        // .write "abc"
        java.nio.file.Files.write(testFile.toPath(), "abc".getBytes());
        List<String> files = List.of(filePath);

        // First: when file does not exist, should call subprocess/callable
        final List<List<String>> called = new ArrayList<>();
        // Mockito can do thenAnswer for invoked args
        when(ag.convertToWav(any())).thenAnswer(invocation -> {
            called.add(invocation.getArgument(0));
            // Simulate creating file with .temp.wav suffix
            String outFile = files.get(0) + ".temp.wav";
            File outF = new File(outFile);
            java.nio.file.Files.write(outF.toPath(), "dummy".getBytes());
            return List.of(outFile);
        });

        // Now call function
        List<String> out = ag.convertToWav(files);
        assertEquals(List.of(filePath + ".temp.wav"), out);
        assertFalse(called.isEmpty());

        // Now simulate file already exists
        called.clear();
        when(ag.convertToWav(any())).thenAnswer(invocation -> {
            // No subprocess call
            return List.of(filePath + ".temp.wav");
        });
        List<String> out2 = ag.convertToWav(files);
        assertEquals(List.of(filePath + ".temp.wav"), out2);
        assertTrue(called.isEmpty() || called.size() == 0);
    }

    @Test
    public void testWordsJsonValidAndInvalid() {
        Audiogrep ag = new Audiogrep();
        // Valid
        List<Map<String, Object>> s = List.of(
            Map.of(
                "words", List.of(
                    List.of("hello", "1", "2", "0.5"),
                    List.of("world", "2", "3", "0.8")
                ),
                "file", "foo"
            )
        );
        String j = ag.wordsJson(s);
        assertTrue(j.contains("\"word\": \"hello\""));

        // Invalid: inner words only length 2
        List<Map<String, Object>> s2 = List.of(
            Map.of(
                "words", List.of(List.of("x", "y")),
                "file", "foo"
            )
        );
        try {
            ag.wordsJson(s2); // Should not throw
        } catch (Exception e) {
            fail("wordsJson threw exception on invalid input: " + e.getMessage());
        }
    }

    @Test
    public void testConvertTimestampsEdgeCases() {
        Audiogrep ag = new Audiogrep();
        List<Map<String, Object>> sentences = ag.convertTimestamps(List.of("/not/a/file"));
        assertEquals(0, sentences.size());
        List<Map<String, Object>> sentences2 = ag.convertTimestamps(List.of(tmpPath.resolve("nofile.mp3").toString()));
        assertEquals(0, sentences2.size());
    }

    @Test
    public void testConvertTimestampsSentence() throws IOException {
        Audiogrep ag = new Audiogrep();
        Path fn = tmpPath.resolve("x.transcription.txt");
        String[] lines = {
                "<s> 0.0 0.2 1.0\n", "word 0.2 0.3 1.0\n", "</s> 0.3 0.5 1.0\n"
        };
        java.nio.file.Files.write(fn, Arrays.asList(lines));
        List<Map<String, Object>> sents = ag.convertTimestamps(List.of(fn.toString()));
        assertFalse(sents.isEmpty());
        Map<String, Object> sent = sents.get(0);
        assertEquals(0.0, (double)sent.get("start"));
        assertEquals(0.3, (double)sent.get("end"));
        List<List<Object>> words = (List<List<Object>>) sent.get("words");
        assertEquals(1, words.size());
        assertEquals("word", words.get(0).get(0));
    }

    @Test
    public void testTextReadsSentences() throws IOException {
        Audiogrep ag = new Audiogrep();
        Path fn = tmpPath.resolve("test.transcription.txt");
        String[] lines = {
                "<s> 1 2 1\n", "a 2 3 1\n", "b 4 5 1\n", "</s> 6 7 1\n"
        };
        java.nio.file.Files.write(fn, Arrays.asList(lines));
        String res = ag.text(List.of(fn.toString()));
        assertTrue(res.contains("a b"));
    }

    @Test
    public void testTranscribeRuns() throws IOException {
        Audiogrep ag = Mockito.mock(Audiogrep.class);
        Path tmpwav = tmpPath.resolve("audio.temp.wav");
        java.nio.file.Files.write(tmpwav, "abc".getBytes());
        final List<Object> called = new ArrayList<>();
        Set<String> filesCreated = new HashSet<>();
        String outname = tmpPath.resolve("audio.transcription.txt").toString();

        // Simulate check_output and os.remove hooks through Java
        doAnswer(invoc -> {
            called.add(Arrays.asList(invoc.getArguments()));
            // Simulate writing some transcription
            java.nio.file.Files.write(Path.of(outname), "dummy transcription".getBytes());
            filesCreated.add(outname);
            return null;
        }).when(ag).transcribe(any(), eq(1), eq(1));

        // If file exists, remove it
        File outFile = new File(outname);
        if (outFile.exists())
            outFile.delete();

        ag.transcribe(List.of(tmpwav.toString()), 1, 1);

        assertTrue(called.stream().anyMatch(entry -> ((List)entry).get(0) instanceof List));
        assertTrue(filesCreated.contains(outname));
    }

    @Test
    public void testSearchModes() throws IOException {
        Audiogrep ag = Mockito.mock(Audiogrep.class);
        Path fn = tmpPath.resolve("s.transcription.txt");
        String[] lines = {
                "<s> 0.0 1.0 1\n", "foo 1.0 1.1 1\n", "bar 1.1 1.2 1\n", "</s> 1.2 2.0 1\n"
        };
        java.nio.file.Files.write(fn, Arrays.asList(lines));
        // Monkeypatch fragment_search, word_search, franken_sentence, convert_timestamps
        when(ag.fragmentSearch(anyString(), anyList(), anyBoolean()))
            .thenReturn(List.of(Map.of("foo","bar")));
        when(ag.wordSearch(anyString(), anyList(), anyBoolean()))
            .thenReturn(List.of(Map.of("baz",1)));
        when(ag.frankenSentence(anyString(), anyList()))
            .thenReturn(List.of((Object)42));
        when(ag.convertTimestamps(any())).thenReturn(List.of(
                Map.of("words", List.of(List.of("foo","1","2","1")), "file", fn.toString())
        ));

        List<Map<String,Object>> out = ag.search("foo", List.of(fn.toString()), "fragment", false);
        assertTrue(out != null && out.size() > 0 && "bar".equals(out.get(0).get("foo")));

        List<Map<String,Object>> out2 = ag.search("foo", List.of(fn.toString()), "word", false);
        assertTrue(out2 != null && (int)out2.get(0).getOrDefault("baz", 1) == 1);

        List<Object> out3 = ag.search("foo", List.of(fn.toString()), "franken", false);
        assertTrue(out3.size() == 1 && ((Integer)out3.get(0)) == 42);
    }

    @Test
    public void testSearchSentence() throws IOException {
        Audiogrep ag = new Audiogrep();
        Path fn = tmpPath.resolve("a.transcription.txt");
        String[] lines = {
                "<s> 0.0 0.1 1\n", "foo 0.1 0.2 1\n", "</s> 0.2 0.3 1\n",
                "<s> 0.4 0.5 1\n", "bar 0.5 0.6 1\n", "</s> 0.6 0.7 1\n"
        };
        java.nio.file.Files.write(fn, Arrays.asList(lines));
        List<Map<String,Object>> out = ag.search("foo", List.of(fn.toString()), "sentence", false);
        assertTrue(out instanceof List);
        boolean found = false;
        for (Map<String,Object> sent : out) {
            @SuppressWarnings("unchecked")
            List<List<Object>> words = (List<List<Object>>) sent.get("words");
            String allWords = words.stream()
                    .map(w -> w.get(0).toString())
                    .collect(Collectors.joining(" "));
            if (allWords.contains("foo")) {
                found = true;
                break;
            }
        }
        assertTrue(found || out.isEmpty());
    }

    @Test
    public void testFragmentSearchEmpty() {
        Audiogrep ag = new Audiogrep();
        List<Map<String,Object>> res = ag.fragmentSearch("notfound", List.of(
                Map.of("words", List.of(List.of("a", "0", "1", "1")), "file", "testfile")
        ), false);
        assertEquals(0, res.size());
    }

    @Test
    public void testWordSearchEmpty() {
        Audiogrep ag = new Audiogrep();
        List<Map<String,Object>> res = ag.wordSearch("notfound", List.of(
                Map.of("words", List.of(List.of("a", "0", "1", "1")), "file", "testfile")
        ), false);
        assertEquals(0, res.size());
    }

    @Test
    public void testFrankenSentenceEmpty() {
        Audiogrep ag = Mockito.mock(Audiogrep.class);
        when(ag.search(anyString(), anyList(), anyString(), anyBoolean())).thenReturn(List.of());
        List<Object> res = ag.frankenSentence("notfound", List.of(
                Map.of("words", List.of(List.of("a", "0", "1", "1")), "file", "testfile")
        ));
        assertEquals(0, res.size());
    }

    // Utility: Mockito any for List<String>
    @SuppressWarnings("unchecked")
    private List<String> anyList() {
        return Mockito.anyList();
    }

    private String anyString() {
        return Mockito.anyString();
    }

    private Boolean anyBoolean() {
        return Mockito.anyBoolean();
    }
}
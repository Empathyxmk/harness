package com.antiboredom.audiogrep.original;

import com.antiboredom.audiogrep.Audiogrep;
import org.junit.jupiter.api.Test;

import java.io.File;
import java.nio.file.Paths;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

public class TestAudiogrep {
    @Test
    public void testConvertTimestamps() {
        Audiogrep ag = new Audiogrep();
        // The file is expected to exist for testing, simulate its presence.
        String filename = Paths.get(System.getProperty("user.dir"), "src", "test", "resources", "data", "test.mp3").toString();

        // For actual test, the file should exist. This will fail if not provided or simulated.
        List<Map<String,Object>> sentences = ag.convertTimestamps(List.of(filename));
        // Simulate: sentences get parsed, words inner field is a list, etc.
        // Build union of all words.
        boolean foundFashion = false;
        for (Map<String,Object> sentence : sentences) {
            @SuppressWarnings("unchecked")
            List<List<Object>> words = (List<List<Object>>) sentence.get("words");
            for (List<Object> word : words) {
                if("fashion".equals(word.get(0).toString())) {
                    foundFashion = true;
                }
            }
        }
        assertTrue(foundFashion, "'fashion' not found in audio words");
        assertEquals(9, sentences.size());
    }
}
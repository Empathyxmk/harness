package edu.cmu.pocketsphinx;

import org.junit.Test;

import static org.junit.Assert.*;

public class SpeechRecognizerPublicTest {

    @Test
    public void testSpeechRecognizerInstancePublic() {
        SpeechRecognizer recognizer = new SpeechRecognizer();
        assertNotNull(recognizer);
    }

    // Public tests: we could add additional trivial assertions if possible, but
    // SpeechRecognizer usage is limited without Android context.
}
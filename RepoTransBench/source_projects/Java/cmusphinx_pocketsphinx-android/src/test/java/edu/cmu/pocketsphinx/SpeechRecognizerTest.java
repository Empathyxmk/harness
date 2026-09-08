package edu.cmu.pocketsphinx;

import org.junit.Test;

import static org.junit.Assert.*;

public class SpeechRecognizerTest {

    private static class DummyListener implements RecognitionListener {
        boolean ready = false;
        @Override public void onReadyForSpeech() { ready = true; }
        @Override public void onBeginningOfSpeech() {}
        @Override public void onEndOfSpeech() {}
        @Override public void onPartialResult(Hypothesis hypothesis) {}
        @Override public void onResult(Hypothesis hypothesis) {}
        @Override public void onError(Exception e) {}
        @Override public void onTimeout() {}
    }

    @Test
    public void testAddAndRemoveListener() {
        SpeechRecognizer recognizer = new SpeechRecognizer();
        DummyListener l = new DummyListener();
        recognizer.addListener(l);
        recognizer.removeListener(l);
        // Should not cause exceptions
    }

    @Test
    public void testStartListeningFiresReady() {
        SpeechRecognizer recognizer = new SpeechRecognizer();
        DummyListener l = new DummyListener();
        recognizer.addListener(l);
        recognizer.startListening("search");
        assertTrue(l.ready);
    }

    @Test
    public void testStopAndCancelNoErrors() {
        SpeechRecognizer recognizer = new SpeechRecognizer();
        recognizer.stop();
        recognizer.cancel();
        // Just for coverage, no state to assert
    }
}
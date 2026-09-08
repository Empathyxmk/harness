package edu.cmu.pocketsphinx;

import org.junit.Test;

import static org.junit.Assert.*;

public class RecognitionListenerPublicTest {

    private static class CallbackCounter implements RecognitionListener {

        public int ready, begin, end, partial, result, error, timeout;

        @Override public void onReadyForSpeech() { ready++; }
        @Override public void onBeginningOfSpeech() { begin++; }
        @Override public void onEndOfSpeech() { end++; }
        @Override public void onPartialResult(Hypothesis hypothesis) { partial++; }
        @Override public void onResult(Hypothesis hypothesis) { result++; }
        @Override public void onError(Exception e) { error++; }
        @Override public void onTimeout() { timeout++; }
    }

    @Test
    public void testListenerMethodsWithDifferentData() {
        CallbackCounter cc = new CallbackCounter();
        cc.onReadyForSpeech();
        cc.onReadyForSpeech(); // Call twice to differ from existing
        cc.onBeginningOfSpeech();
        cc.onPartialResult(new Hypothesis("different_partial", 100));
        cc.onEndOfSpeech();
        cc.onEndOfSpeech(); // Call twice to differ from existing
        cc.onResult(new Hypothesis("different_result", 99));
        cc.onResult(new Hypothesis("result_again", -5));
        cc.onError(new Exception("different_fail"));
        cc.onError(new Exception("another_fail"));
        cc.onTimeout();
        cc.onTimeout(); // Call twice to differ

        assertEquals(2, cc.ready);
        assertEquals(1, cc.begin);
        assertEquals(2, cc.end);
        assertEquals(1, cc.partial);
        assertEquals(2, cc.result);
        assertEquals(2, cc.error);
        assertEquals(2, cc.timeout);
    }
}
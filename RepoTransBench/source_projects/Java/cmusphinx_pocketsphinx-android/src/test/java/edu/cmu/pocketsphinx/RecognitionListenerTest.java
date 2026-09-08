package edu.cmu.pocketsphinx;

import org.junit.Test;

import static org.junit.Assert.*;

public class RecognitionListenerTest {

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
    public void testListenerMethods() {
        CallbackCounter cc = new CallbackCounter();
        cc.onReadyForSpeech();
        cc.onBeginningOfSpeech();
        cc.onEndOfSpeech();
        cc.onPartialResult(new Hypothesis("foo", 10));
        cc.onResult(new Hypothesis("bar", 9));
        cc.onError(new Exception("fail"));
        cc.onTimeout();
        assertEquals(1, cc.ready);
        assertEquals(1, cc.begin);
        assertEquals(1, cc.end);
        assertEquals(1, cc.partial);
        assertEquals(1, cc.result);
        assertEquals(1, cc.error);
        assertEquals(1, cc.timeout);
    }
}
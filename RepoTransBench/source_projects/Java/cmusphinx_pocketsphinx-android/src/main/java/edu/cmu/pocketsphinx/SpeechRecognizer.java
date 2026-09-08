package edu.cmu.pocketsphinx;

import java.util.ArrayList;
import java.util.List;

public class SpeechRecognizer {
    private final List<RecognitionListener> listeners = new ArrayList<>();

    public SpeechRecognizer() {}

    public void addListener(RecognitionListener l) {
        listeners.add(l);
    }

    public void removeListener(RecognitionListener l) {
        listeners.remove(l);
    }

    public void startListening(String search) {
        for (RecognitionListener l : listeners)
            l.onReadyForSpeech();
        // dummy operation
    }

    public void stop() {
        // dummy
    }
    public void cancel() {
        // dummy
    }
}
package edu.cmu.pocketsphinx;

public interface RecognitionListener {
    void onReadyForSpeech();
    void onBeginningOfSpeech();
    void onEndOfSpeech();
    void onPartialResult(Hypothesis hypothesis);
    void onResult(Hypothesis hypothesis);
    void onError(Exception e);
    void onTimeout();
}
package edu.cmu.pocketsphinx;

public class SpeechRecognizerSetup {

    private java.io.File acousticModel;
    private java.io.File dictionary;
    private java.io.File rawLogDir;

    public static SpeechRecognizerSetup defaultSetup() {
        return new SpeechRecognizerSetup();
    }

    public SpeechRecognizerSetup setAcousticModel(java.io.File f) {
        this.acousticModel = f;
        return this;
    }

    public SpeechRecognizerSetup setDictionary(java.io.File f) {
        this.dictionary = f;
        return this;
    }

    public SpeechRecognizerSetup setRawLogDir(java.io.File f) {
        this.rawLogDir = f;
        return this;
    }

    public SpeechRecognizer getRecognizer() {
        return new SpeechRecognizer();
    }
}
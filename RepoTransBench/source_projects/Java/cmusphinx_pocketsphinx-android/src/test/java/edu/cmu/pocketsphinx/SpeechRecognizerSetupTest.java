package edu.cmu.pocketsphinx;

import org.junit.Test;
import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class SpeechRecognizerSetupTest {

    @Test
    public void testDefaultSetup() {
        Assets assets = mock(Assets.class);
        SpeechRecognizerSetup setup = SpeechRecognizerSetup.defaultSetup();
        assertNotNull(setup);
    }

    @Test
    public void testGetRecognizerReturnsSpeechRecognizer() {
        SpeechRecognizerSetup setup = SpeechRecognizerSetup.defaultSetup();
        setup.setAcousticModel(new java.io.File("."));
        setup.setDictionary(new java.io.File("."));
        setup.setRawLogDir(new java.io.File("."));
        SpeechRecognizer recognizer = setup.getRecognizer();
        assertNotNull(recognizer);
    }

    @Test
    public void testSetKeyMethods() {
        SpeechRecognizerSetup setup = SpeechRecognizerSetup.defaultSetup();
        assertEquals(setup, setup.setAcousticModel(new java.io.File(".")));
        assertEquals(setup, setup.setDictionary(new java.io.File(".")));
        assertEquals(setup, setup.setRawLogDir(new java.io.File(".")));
    }
}
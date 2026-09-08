package edu.cmu.pocketsphinx;

import org.junit.Test;
import java.io.File;

import static org.junit.Assert.*;

public class SpeechRecognizerSetupPublicTest {

    @Test
    public void testDefaultSetupReturnsSetupInstancePublic() {
        SpeechRecognizerSetup setup = SpeechRecognizerSetup.defaultSetup();
        assertNotNull(setup);
    }

    @Test
    public void testSetupWithNonExistingFilesPublic() {
        SpeechRecognizerSetup setup = SpeechRecognizerSetup.defaultSetup();
        File acousticModel = new File("dummy_model_dir_public");
        File dictionary = new File("dummy_dict_file_public.dic");
        File logDir = new File("dummy_log_dir_public");

        assertSame(setup, setup.setAcousticModel(acousticModel));
        assertSame(setup, setup.setDictionary(dictionary));
        assertSame(setup, setup.setRawLogDir(logDir));
    }

    @Test
    public void testGetRecognizerReturnsInstancePublic() {
        SpeechRecognizerSetup setup = SpeechRecognizerSetup.defaultSetup();
        assertNotNull(setup.getRecognizer());
    }
}
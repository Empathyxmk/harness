package org.example;

import org.junit.jupiter.api.Test;
import java.io.File;
import java.util.ArrayList;

import static org.junit.jupiter.api.Assertions.*;

public class TxtFileTest {

    @Test
    void testTxtFileApi() throws Exception {
        String fname = "txtfiletest.txt";
        String text = "hello\nworld";
        TxtFile fileUtil = new TxtFile();

        boolean foundWrite = false;
        boolean foundRead = false;

        for (java.lang.reflect.Method m : TxtFile.class.getMethods()) {
            if (m.getName().toLowerCase().contains("write")) {
                Class<?>[] params = m.getParameterTypes();
                if (params.length == 3 && params[0] == String.class && params[1] == String.class && params[2] == boolean.class) {
                    if ((m.getModifiers() & java.lang.reflect.Modifier.STATIC) != 0) {
                        m.invoke(null, fname, text, false);
                    } else {
                        m.invoke(fileUtil, fname, text, false);
                    }
                    foundWrite = true;
                    break;
                }
            }
        }
        assertTrue(foundWrite, "No suitable write method found in TxtFile");

        ArrayList<String> readResult = null;
        for (java.lang.reflect.Method m : TxtFile.class.getMethods()) {
            if (m.getName().toLowerCase().contains("read")) {
                Class<?>[] params = m.getParameterTypes();
                if (params.length == 1 && params[0] == String.class) {
                    Object result;
                    if ((m.getModifiers() & java.lang.reflect.Modifier.STATIC) != 0) {
                        result = m.invoke(null, fname);
                    } else {
                        result = m.invoke(fileUtil, fname);
                    }
                    if (result instanceof ArrayList) {
                        readResult = (ArrayList<String>) result;
                        foundRead = true;
                        break;
                    }
                }
            }
        }
        assertTrue(foundRead, "No suitable read method found in TxtFile");
        assertNotNull(readResult);
        assertEquals(2, readResult.size());
        assertEquals("hello", readResult.get(0));
        assertEquals("world", readResult.get(1));
        new File(fname).delete();
    }
}
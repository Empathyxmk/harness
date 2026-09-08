package org.nibblesec.tools;

import org.junit.Test;

import java.io.*;

import static org.junit.Assert.*;

public class SerialKillerPublicTest {
    @Test
    public void testSerializationWithDifferentString() throws Exception {
        String testStr = "PublicTestingStringXYZ";
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(baos);
        oos.writeObject(testStr);
        oos.close();

        ByteArrayInputStream bais = new ByteArrayInputStream(baos.toByteArray());
        ObjectInputStream ois = new ObjectInputStream(bais);
        String result = (String) ois.readObject();
        ois.close();

        assertEquals(testStr, result);
        assertFalse(result.isEmpty());
        assertTrue(result.startsWith("Public"));
    }
}
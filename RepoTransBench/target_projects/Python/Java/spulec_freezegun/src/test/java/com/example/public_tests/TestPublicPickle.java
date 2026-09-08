package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.io.*;

public class TestPublicPickle {

    @Test
    public void testSerialization() throws IOException, ClassNotFoundException {
        String data = "serialized data";
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(out);
        oos.writeObject(data);
        oos.flush();
        ByteArrayInputStream in = new ByteArrayInputStream(out.toByteArray());
        ObjectInputStream ois = new ObjectInputStream(in);
        String read = (String) ois.readObject();
        assertEquals(data, read);
    }
}
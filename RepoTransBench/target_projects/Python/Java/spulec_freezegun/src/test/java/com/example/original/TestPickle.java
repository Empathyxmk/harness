package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.io.*;

public class TestPickle {

    @Test
    public void testSerializationAndDeserialization() throws IOException, ClassNotFoundException {
        // Test serializing and deserializing an object
        String original = "this is data";
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(outputStream);
        oos.writeObject(original);
        oos.flush();

        ByteArrayInputStream inputStream = new ByteArrayInputStream(outputStream.toByteArray());
        ObjectInputStream ois = new ObjectInputStream(inputStream);
        String deserialized = (String) ois.readObject();

        assertEquals(original, deserialized, "Deserialized object did not match original.");
    }
}
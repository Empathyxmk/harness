package to.lean.tools.gmail.importer;

import org.junit.Test;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;

import static org.junit.Assert.*;

public class IoProviderPublicTest {

    @Test
    public void testDifferentReadAllReturnsStream() throws IOException {
        String testString = "PublicTestContent123";
        InputStream input = new ByteArrayInputStream(testString.getBytes("UTF-8"));
        byte[] bytes = IoProvider.readAll(input);
        assertEquals(testString, new String(bytes, "UTF-8"));
    }
}
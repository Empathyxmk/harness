package ca.krasnay.sqlbuilder.orm;

import junit.framework.TestCase;
import java.util.LinkedHashMap;
import java.util.Map;

public class StringMapConverterPublicTest extends TestCase {

    public void testToFromStringPublic() {
        StringMapConverter conv = new StringMapConverter(";", "=");

        Map<String,String> orig = new LinkedHashMap<String,String>();
        orig.put("key1", "valueA");
        orig.put("keyB", "value2");
        assertEquals("key1=valueA;keyB=value2", conv.toString(orig));
        assertEquals(null, conv.toString(null));

        Map<String,String> expected = new LinkedHashMap<String,String>();
        expected.put("x", "y");
        expected.put("abc", "123");
        assertEquals(expected, conv.fromString("x=y;abc=123"));

        assertEquals(null, conv.fromString(null));
    }
}
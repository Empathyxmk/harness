package ca.krasnay.sqlbuilder.orm;

import junit.framework.TestCase;
import java.util.Arrays;

public class StringListConverterPublicTest extends TestCase {

    public void testListToStringPublic() {
        StringListConverter conv = new StringListConverter(",");
        assertEquals("hello,world,public", conv.toString(Arrays.asList("hello", "world", "public")));
        assertEquals(null, conv.toString(null));
    }

    public void testStringToListPublic() {
        StringListConverter conv = new StringListConverter(",");
        assertEquals(Arrays.asList("foo", "bar", "baz"), conv.fromString("foo,bar,baz"));
        assertEquals(null, conv.fromString(null));
    }
}
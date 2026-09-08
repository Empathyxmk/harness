package ca.krasnay.sqlbuilder.orm;

import junit.framework.TestCase;
import java.util.Arrays;

public class StringListFlattenerPublicTest extends TestCase {

    public void testFlattenPublic() {
        assertEquals("a|b|c", StringListFlattener.flatten(Arrays.asList("a", "b", "c"), "|"));
        assertEquals("", StringListFlattener.flatten(Arrays.asList(), "#"));
    }

    public void testUnflattenPublic() {
        assertEquals(Arrays.asList("x", "y"), StringListFlattener.unflatten("x|y", "|"));
        assertEquals(Arrays.asList(""), StringListFlattener.unflatten("", "|"));
    }
}
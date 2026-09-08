package ca.krasnay.sqlbuilder;

import junit.framework.TestCase;

public class UniqueStringGeneratorPublicTest extends TestCase {

    public void testGeneratorPublic() {
        UniqueStringGenerator g = new UniqueStringGenerator("xyz");
        assertEquals("xyz0", g.next());
        assertEquals("xyz1", g.next());
        assertEquals("xyz2", g.next());
    }
}
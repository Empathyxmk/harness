package ca.krasnay.sqlbuilder;

import junit.framework.TestCase;

public class SelectCreatorPublicTest extends TestCase {

    public void testAllocateParameterPublic() {
        SelectCreator sel = new SelectCreator();
        String p0 = sel.allocateParameter();
        String p1 = sel.allocateParameter();
        assertEquals("param0", p0);
        assertEquals("param1", p1);
    }
}
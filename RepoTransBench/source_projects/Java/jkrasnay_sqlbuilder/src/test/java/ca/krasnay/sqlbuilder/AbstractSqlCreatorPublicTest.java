package ca.krasnay.sqlbuilder;

import junit.framework.TestCase;

public class AbstractSqlCreatorPublicTest extends TestCase {

    public void testAllocateParameterPublic() {
        SelectCreator sc = new SelectCreator();
        assertEquals("param0", sc.allocateParameter());
        // skip one, check that next is param1, then param2, then param3 for new sequence
        sc.allocateParameter();
        assertEquals("param2", sc.allocateParameter());
    }
}
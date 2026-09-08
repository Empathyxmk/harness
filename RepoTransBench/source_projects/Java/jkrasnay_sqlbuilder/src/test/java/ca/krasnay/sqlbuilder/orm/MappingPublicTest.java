package ca.krasnay.sqlbuilder.orm;

import junit.framework.TestCase;
import java.util.Date;

public class MappingPublicTest extends TestCase {

    static public class Foo {
        @Column
        public int public_id;

        public String value;
    }

    public void testGetSetPublic() throws Exception {
        Mapping mapping = new Mapping(Foo.class);
        Foo foo = new Foo();
        mapping.getField("public_id").setInt(foo, 44);
        assertEquals(44, mapping.getField("public_id").getInt(foo));
    }
}
package ca.krasnay.sqlbuilder;

import junit.framework.TestCase;

public class InsertBuilderPublicTest extends TestCase {

    public void testAllPublic() {

        InsertBuilder builder;

        builder = new InsertBuilder("Product");
        assertEquals("insert into Product () values ()", builder.toString());

        builder.set("code", "'PX01'");
        assertEquals("insert into Product (code) values ('PX01')", builder.toString());

        builder.set("description", "'Widget'");
        assertEquals("insert into Product (code, description) values ('PX01', 'Widget')", builder.toString());

    }
}
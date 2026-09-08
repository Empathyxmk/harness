package ca.krasnay.sqlbuilder;

import junit.framework.TestCase;

public class DeleteBuilderPublicTest extends TestCase {

    public void testPublic() {
        DeleteBuilder builder = new DeleteBuilder("Product");
        assertEquals("delete from Product", builder.toString());

        builder.where("category = 'Electronics'");
        assertEquals("delete from Product where category = 'Electronics'", builder.toString());

        builder.where("price < 20");
        assertEquals("delete from Product where category = 'Electronics' and price < 20", builder.toString());
    }
}
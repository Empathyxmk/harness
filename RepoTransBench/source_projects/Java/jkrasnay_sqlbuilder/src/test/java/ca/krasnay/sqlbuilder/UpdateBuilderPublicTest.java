package ca.krasnay.sqlbuilder;

import junit.framework.TestCase;

public class UpdateBuilderPublicTest extends TestCase {

    public void testAllPublic() {

        UpdateBuilder builder = new UpdateBuilder("Product");
        builder.set("price", "19.99");
        assertEquals("update Product set price = 19.99", builder.toString());

        builder.set("name", "'Gadget'");
        assertEquals("update Product set price = 19.99, name = 'Gadget'", builder.toString());

        builder.where("id = 7");
        assertEquals("update Product set price = 19.99, name = 'Gadget' where id = 7", builder.toString());

        builder.where("category = 'Tools'");
        assertEquals("update Product set price = 19.99, name = 'Gadget' where id = 7 and category = 'Tools'", builder.toString());
    }
}
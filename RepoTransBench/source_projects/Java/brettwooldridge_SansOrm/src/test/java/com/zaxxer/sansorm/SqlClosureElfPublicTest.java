package com.zaxxer.sansorm;

import com.zaxxer.sansorm.internal.OrmWriter;
import org.junit.Test;

import java.lang.reflect.Field;

import static org.junit.Assert.*;

public class SqlClosureElfPublicTest {

    public static class SampleEntity {
        public int publicInt;
        public String publicString;
    }

    @Test
    public void testGetFieldValuePublic() throws Exception {
        // Different test data than original
        SampleEntity obj = new SampleEntity();
        obj.publicInt = 77;
        obj.publicString = "helloPublic";

        Field intField = SampleEntity.class.getField("publicInt");
        Field stringField = SampleEntity.class.getField("publicString");

        assertEquals(77, OrmWriter.getFieldValue(obj, intField));
        assertEquals("helloPublic", OrmWriter.getFieldValue(obj, stringField));
    }

    @Test
    public void testSetFieldValuePublic() throws Exception {
        SampleEntity obj = new SampleEntity();

        Field intField = SampleEntity.class.getField("publicInt");
        Field stringField = SampleEntity.class.getField("publicString");

        OrmWriter.setFieldValue(obj, intField, 51);
        OrmWriter.setFieldValue(obj, stringField, "worldPublic");

        assertEquals(51, obj.publicInt);
        assertEquals("worldPublic", obj.publicString);
    }
}
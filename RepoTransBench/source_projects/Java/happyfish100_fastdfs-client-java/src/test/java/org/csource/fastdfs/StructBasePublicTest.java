package org.csource.fastdfs;

import org.junit.BeforeClass;
import org.junit.Test;

import java.io.UnsupportedEncodingException;
import java.util.Date;

import static org.junit.Assert.*;

public class StructBasePublicTest {

    private static class DummyStruct extends StructBase {
        public String strVal;
        public long longVal;
        public int intVal;
        public int int32Val;
        public byte byteVal;
        public boolean boolVal;
        public Date dateVal;

        @Override
        public void setFields(byte[] bs, int offset) {
            FieldInfo field = new FieldInfo("test", 0, 4);
            this.strVal = stringValue(bs, offset, field);
            this.longVal = longValue(bs, offset, field);
            this.intVal = intValue(bs, offset, field);
            this.int32Val = int32Value(bs, offset, field);
            this.byteVal = byteValue(bs, offset, field);
            this.boolVal = booleanValue(bs, offset, field);
            this.dateVal = dateValue(bs, offset, field);
        }
    }

    @BeforeClass
    public static void setUpCharset() {
        try {
            org.csource.fastdfs.ClientGlobal.g_charset = "UTF-8";
        } catch (Throwable t) {}
    }

    @Test
    public void testStringValueDifferent() throws UnsupportedEncodingException {
        DummyStruct s = new DummyStruct();
        byte[] bs = "Public01\0\0".getBytes("UTF-8"); // different string and field size (8)
        StructBase.FieldInfo f = new StructBase.FieldInfo("str", 0, 8);
        String val = s.stringValue(bs, 0, f);
        assertEquals("Public01", val);
    }

    @Test
    public void testStringValueEncodingExceptionPublic() {
        DummyStruct s = new DummyStruct();
        StructBase.FieldInfo f = new StructBase.FieldInfo("str", 0, 1);
        // Set a definitely unsupported charset for the fallback test
        String origCharset = org.csource.fastdfs.ClientGlobal.g_charset;
        org.csource.fastdfs.ClientGlobal.g_charset = "unknown-charset";
        String val = s.stringValue(new byte[] {66}, 0, f);
        assertNull(val);
        org.csource.fastdfs.ClientGlobal.g_charset = origCharset;
    }

    @Test
    public void testOtherValueMethodsPublic() {
        DummyStruct s = new DummyStruct();
        byte[] bs = new byte[16];
        // set value for long and int using a different value
        bs[0] = 42;
        StructBase.FieldInfo f = new StructBase.FieldInfo("d", 0, 8);

        s.setFields(bs, 0);
        assertNotNull(s.strVal);
        assertNotNull(s.dateVal);
        assertTrue(s.byteVal == bs[0]);
    }
}
package org.csource.fastdfs;

import org.junit.BeforeClass;
import org.junit.Test;

import java.io.UnsupportedEncodingException;
import java.util.Date;

import static org.junit.Assert.*;

public class StructBaseTest {

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
        // ensure ClientGlobal.g_charset is set
        try {
            org.csource.fastdfs.ClientGlobal.g_charset = "UTF-8";
        } catch (Throwable t) {}
    }

    @Test
    public void testStringValueNormal() throws UnsupportedEncodingException {
        DummyStruct s = new DummyStruct();
        byte[] bs = "TestStr\0\0\0".getBytes("UTF-8");
        StructBase.FieldInfo f = new StructBase.FieldInfo("str", 0, 7);
        String val = s.stringValue(bs, 0, f);
        assertEquals("TestStr", val);
    }

    @Test
    public void testStringValueEncodingException() {
        DummyStruct s = new DummyStruct();
        StructBase.FieldInfo f = new StructBase.FieldInfo("str", 0, 1);
        // Will throw exception if charset is invalid, so let's set an invalid one and test null fallback
        String origCharset = org.csource.fastdfs.ClientGlobal.g_charset;
        org.csource.fastdfs.ClientGlobal.g_charset = "invalid-charset";
        String val = s.stringValue(new byte[] {65}, 0, f);
        assertNull(val);
        org.csource.fastdfs.ClientGlobal.g_charset = origCharset;
    }

    @Test
    public void testOtherValueMethods() {
        DummyStruct s = new DummyStruct();
        byte[] bs = new byte[16];
        // set value for long and int
        long valLong = 100L;
        int valInt = 42;
        // Use ProtoCommon to encode longs/ints. But just test conversion, not encoding logic itself
        bs[0] = 100;
        StructBase.FieldInfo f = new StructBase.FieldInfo("d", 0, 8);

        s.setFields(bs, 0);
        // Just basic asserts for coverage here
        assertNotNull(s.strVal);
        assertNotNull(s.dateVal);
        assertTrue(s.byteVal == bs[0]);
    }
}
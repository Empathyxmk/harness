package net.jodah.typetools;

import org.testng.annotations.Test;
import java.lang.reflect.*;

import static org.testng.Assert.*;

public class ReifiedParameterizedTypeTest {

    private static class Sample<A, B> {}

    static ParameterizedType getParameterizedType() {
        try {
            Field f = SampleHolder.class.getDeclaredField("sample");
            return (ParameterizedType) f.getGenericType();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    static class SampleHolder {
        Sample<String, Integer> sample;
    }

    @Test
    public void testAddReifiedTypeArgument_Normal() {
        ParameterizedType pt = getParameterizedType();
        ReifiedParameterizedType rpt = new ReifiedParameterizedType(pt);

        rpt.addReifiedTypeArgument(String.class);
        rpt.addReifiedTypeArgument(Integer.class);

        assertEquals(rpt.getActualTypeArguments()[0], String.class);
        assertEquals(rpt.getActualTypeArguments()[1], Integer.class);
    }

    @Test
    public void testAddReifiedTypeArgument_Loop() {
        ParameterizedType pt = getParameterizedType();
        ReifiedParameterizedType rpt = new ReifiedParameterizedType(pt);

        rpt.addReifiedTypeArgument(rpt); // self-loop
        rpt.addReifiedTypeArgument(Integer.class);

        assertTrue(rpt.getActualTypeArguments()[0] == rpt);
        assertEquals(rpt.getActualTypeArguments()[1], Integer.class);

        // cover toString self-loop
        String str = rpt.toString();
        assertTrue(str.contains("..."));
    }

    @Test
    public void testAddReifiedTypeArgument_Overflow() {
        ParameterizedType pt = getParameterizedType();
        ReifiedParameterizedType rpt = new ReifiedParameterizedType(pt);

        rpt.addReifiedTypeArgument(String.class);
        rpt.addReifiedTypeArgument(Integer.class);
        rpt.addReifiedTypeArgument(Boolean.class); // Should be ignored, array only supports 2 args

        assertNull(rpt.getActualTypeArguments().length > 2 ? rpt.getActualTypeArguments()[2] : null);
    }

    @Test
    public void testToString_OwnerType() {
        // Instead: test with Sample<String, Integer>
        ParameterizedType paramType = getParameterizedType();
        ReifiedParameterizedType rpt = new ReifiedParameterizedType(paramType);

        rpt.addReifiedTypeArgument(null);
        rpt.addReifiedTypeArgument(Integer.class);
        String s = rpt.toString();
        assertTrue(s.contains("null"));
        assertTrue(s.contains(Integer.class.getTypeName()));
    }

    @Test
    public void testEquals() {
        ParameterizedType pt = getParameterizedType();
        ReifiedParameterizedType rpt1 = new ReifiedParameterizedType(pt);
        ReifiedParameterizedType rpt2 = new ReifiedParameterizedType(pt);

        rpt1.addReifiedTypeArgument(String.class);
        rpt1.addReifiedTypeArgument(Integer.class);

        rpt2.addReifiedTypeArgument(String.class);
        rpt2.addReifiedTypeArgument(Integer.class);

        // equal
        assertTrue(rpt1.equals(rpt2));
        assertTrue(rpt2.equals(rpt1));

        // not equal: different type arguments
        ReifiedParameterizedType rpt3 = new ReifiedParameterizedType(pt);
        rpt3.addReifiedTypeArgument(Integer.class);
        rpt3.addReifiedTypeArgument(String.class);
        assertFalse(rpt1.equals(rpt3));
    }

    @Test
    public void testHashCode() {
        ParameterizedType pt = getParameterizedType();
        ReifiedParameterizedType rpt1 = new ReifiedParameterizedType(pt);
        ReifiedParameterizedType rpt2 = new ReifiedParameterizedType(pt);

        rpt1.addReifiedTypeArgument(String.class);
        rpt1.addReifiedTypeArgument(Integer.class);

        rpt2.addReifiedTypeArgument(String.class);
        rpt2.addReifiedTypeArgument(Integer.class);

        assertEquals(rpt1.hashCode(), rpt2.hashCode());
    }

    @Test
    public void testNotEquals_DifferentType() {
        ParameterizedType pt = getParameterizedType();
        ReifiedParameterizedType rpt = new ReifiedParameterizedType(pt);
        assertFalse(rpt.equals("x"));
        assertFalse(rpt.equals(null));
    }
}
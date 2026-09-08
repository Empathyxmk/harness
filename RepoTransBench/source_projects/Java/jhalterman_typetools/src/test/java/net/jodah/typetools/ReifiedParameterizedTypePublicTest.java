package net.jodah.typetools;

import org.testng.annotations.Test;
import java.lang.reflect.*;

import static org.testng.Assert.*;

public class ReifiedParameterizedTypePublicTest {

    private static class PublicSample<X, Y> {}

    static ParameterizedType getParameterizedType() {
        try {
            Field f = PublicSampleHolder.class.getDeclaredField("sample");
            return (ParameterizedType) f.getGenericType();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    static class PublicSampleHolder {
        PublicSample<Double, Character> sample;
    }

    @Test
    public void testAddReifiedTypeArgument_Normal() {
        ParameterizedType pt = getParameterizedType();
        ReifiedParameterizedType rpt = new ReifiedParameterizedType(pt);

        rpt.addReifiedTypeArgument(Double.class);
        rpt.addReifiedTypeArgument(Character.class);

        assertEquals(rpt.getActualTypeArguments()[0], Double.class);
        assertEquals(rpt.getActualTypeArguments()[1], Character.class);
    }

    @Test
    public void testAddReifiedTypeArgument_Loop() {
        ParameterizedType pt = getParameterizedType();
        ReifiedParameterizedType rpt = new ReifiedParameterizedType(pt);

        rpt.addReifiedTypeArgument(rpt); // self-loop
        rpt.addReifiedTypeArgument(Character.class);

        assertTrue(rpt.getActualTypeArguments()[0] == rpt);
        assertEquals(rpt.getActualTypeArguments()[1], Character.class);

        // cover toString self-loop
        String str = rpt.toString();
        assertTrue(str.contains("..."));
    }

    @Test
    public void testAddReifiedTypeArgument_Overflow() {
        ParameterizedType pt = getParameterizedType();
        ReifiedParameterizedType rpt = new ReifiedParameterizedType(pt);

        rpt.addReifiedTypeArgument(Double.class);
        rpt.addReifiedTypeArgument(Character.class);
        rpt.addReifiedTypeArgument(Float.class); // Should be ignored, array only supports 2 args

        assertNull(rpt.getActualTypeArguments().length > 2 ? rpt.getActualTypeArguments()[2] : null);
    }

    @Test
    public void testToString_OwnerType() {
        ParameterizedType paramType = getParameterizedType();
        ReifiedParameterizedType rpt = new ReifiedParameterizedType(paramType);

        rpt.addReifiedTypeArgument(null);
        rpt.addReifiedTypeArgument(Character.class);
        String s = rpt.toString();
        assertTrue(s.contains("null"));
        assertTrue(s.contains(Character.class.getTypeName()));
    }

    @Test
    public void testEquals() {
        ParameterizedType pt = getParameterizedType();
        ReifiedParameterizedType rpt1 = new ReifiedParameterizedType(pt);
        ReifiedParameterizedType rpt2 = new ReifiedParameterizedType(pt);

        rpt1.addReifiedTypeArgument(Double.class);
        rpt1.addReifiedTypeArgument(Character.class);

        rpt2.addReifiedTypeArgument(Double.class);
        rpt2.addReifiedTypeArgument(Character.class);

        // equal
        assertTrue(rpt1.equals(rpt2));
        assertTrue(rpt2.equals(rpt1));

        // not equal: different type arguments
        ReifiedParameterizedType rpt3 = new ReifiedParameterizedType(pt);
        rpt3.addReifiedTypeArgument(Character.class);
        rpt3.addReifiedTypeArgument(Double.class);
        assertFalse(rpt1.equals(rpt3));
    }

    @Test
    public void testHashCode() {
        ParameterizedType pt = getParameterizedType();
        ReifiedParameterizedType rpt1 = new ReifiedParameterizedType(pt);
        ReifiedParameterizedType rpt2 = new ReifiedParameterizedType(pt);

        rpt1.addReifiedTypeArgument(Double.class);
        rpt1.addReifiedTypeArgument(Character.class);

        rpt2.addReifiedTypeArgument(Double.class);
        rpt2.addReifiedTypeArgument(Character.class);

        assertEquals(rpt1.hashCode(), rpt2.hashCode());
    }

    @Test
    public void testNotEquals_DifferentType() {
        ParameterizedType pt = getParameterizedType();
        ReifiedParameterizedType rpt = new ReifiedParameterizedType(pt);
        assertFalse(rpt.equals("public"));
        assertFalse(rpt.equals(null));
    }
}
package org.codejargon.feather;

import org.junit.Test;

import javax.inject.Named;
import java.lang.annotation.Annotation;

import static org.junit.Assert.*;

public class KeyTest {
    static class Q1 implements Annotation {
        @Override
        public Class<? extends Annotation> annotationType() {
            return Q1.class;
        }
    }

    @Test
    public void keyEqualitySameType() {
        Key<String> k1 = Key.of(String.class);
        Key<String> k2 = Key.of(String.class);
        assertEquals(k1, k2);
        assertEquals(k1.hashCode(), k2.hashCode());
    }

    @Test
    public void keyInequalityType() {
        Key<String> k1 = Key.of(String.class);
        Key<Integer> k2 = Key.of(Integer.class);
        assertNotEquals(k1, k2);
    }

    @Test
    public void keyWithQualifierAnnotation() {
        Key<String> k1 = Key.of(String.class, Q1.class);
        assertEquals(Q1.class, k1.qualifier);
        assertNull(k1.name);
        assertEquals("java.lang.String@Q1", k1.toString());
    }

    @Test
    public void keyWithNamed() {
        Key<String> k1 = Key.of(String.class, "name");
        assertEquals(Named.class, k1.qualifier);
        assertEquals("name", k1.name);
        assertEquals("java.lang.String@\"name\"", k1.toString());
    }

    @Test
    public void keyWithQualifierObject() {
        Q1 q1 = new Q1();
        Key<String> k = Key.of(String.class, (Annotation) q1); // Q1 object, not Named
        assertEquals(Q1.class, k.qualifier);
        assertNull(k.name);
    }

    @Test
    public void keyWithNamedQualifierObject() {
        Named n = new Named() {
            @Override public String value() {return "foo";}
            @Override public Class<? extends Annotation> annotationType() {return Named.class;}
        };
        Key<String> k = Key.of(String.class, n);
        assertEquals(Named.class, k.qualifier);
        assertEquals("foo", k.name);
    }

    @Test
    public void equalsAndHashCodeNullQualifierName() {
        Key<String> k1 = Key.of(String.class);
        Key<String> k2 = Key.of(String.class);
        assertTrue(k1.equals(k2));
        assertEquals(k1.hashCode(), k2.hashCode());
    }

    @Test
    public void notEqualsIfQualifierDiffers() {
        Key<String> k1 = Key.of(String.class);
        Key<String> k2 = Key.of(String.class, Q1.class);
        assertNotEquals(k1, k2);
    }

    @Test
    public void notEqualsIfNameDiffers() {
        Key<String> k1 = Key.of(String.class, "name1");
        Key<String> k2 = Key.of(String.class, "name2");
        assertNotEquals(k1, k2);
    }
}
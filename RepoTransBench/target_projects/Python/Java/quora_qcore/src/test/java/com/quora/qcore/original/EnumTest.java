package com.quora.qcore.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;
import java.util.stream.Collectors;
import java.io.*;
import com.quora.qcore.QCoreAsserts.*;

@SuppressWarnings("unchecked")
public class EnumTest {
    // Minimalistic Enum/Flags/IntEnum for test (real implementation should match Python)
    static class EnumBase<T> implements Serializable {
        final String name;
        final int value;
        EnumBase(String name, int value) { this.name = name; this.value = value; }
        public String getName() { return name; }
        public int getValue() { return value; }
        public String toString() { return name; }
        public boolean equals(Object o) { return o instanceof EnumBase && ((EnumBase<?>)o).value == value && ((EnumBase<?>)o).getClass().equals(this.getClass()); }
        public int hashCode() { return Integer.hashCode(value) + getClass().hashCode(); }
    }
    static class Gender extends EnumBase<Gender> {
        static final Gender UNDEFINED = new Gender("undefined", 0);
        static final Gender MALE = new Gender("male", 1);
        static final Gender FEMALE = new Gender("female", 2);
        static final List<Gender> MEMBERS = List.of(UNDEFINED, MALE, FEMALE);
        Gender(String name, int value) { super(name, value); }
        static Gender parse(String name) {
            for (Gender g : MEMBERS)
                if (g.name.equals(name)) return g;
            throw new IllegalArgumentException();
        }
        Gender opposite() {
            if (this == UNDEFINED) return UNDEFINED;
            if (this == MALE) return FEMALE;
            if (this == FEMALE) return MALE;
            return null;
        }
    }

    @Test
    public void testGenderProps() {
        assertEquals(Gender.UNDEFINED, Gender.parse("undefined"));
        assertEquals(Gender.MALE, Gender.parse("male"));
        assertEquals(Gender.FEMALE, Gender.parse("female"));
        assertEquals(Gender.UNDEFINED, Gender.UNDEFINED.opposite());
        assertEquals(Gender.FEMALE, Gender.MALE.opposite());
        assertEquals(Gender.MALE, Gender.FEMALE.opposite());
        assertEquals(Gender.UNDEFINED.value, 0);
        assertEquals(Gender.MALE.value, 1);
        assertEquals(Gender.FEMALE.value, 2);
        assertEquals("male", Gender.MALE.toString());
    }

    @Test
    public void testEnumValueEquality() {
        Gender g1 = Gender.MALE, g2 = Gender.MALE, g3 = Gender.FEMALE;
        assertEquals(g1, g2);
        assertNotEquals(g1, g3);
    }

    static class XyFlags extends EnumBase<XyFlags> {
        static final XyFlags X = new XyFlags("x", 1);
        static final XyFlags Y = new XyFlags("y", 4);
        static final XyFlags XY = new XyFlags("xy", 5);
        static final List<XyFlags> MEMBERS = List.of(X, Y, XY);

        XyFlags(String name, int value) { super(name, value);}
    }

    @Test
    public void testFlagsSim() {
        assertEquals(XyFlags.X.value | XyFlags.Y.value, XyFlags.XY.value);
    }

    // Pickle simulation: Java Serialization
    private <T extends Serializable> T serDeser(T in) throws IOException, ClassNotFoundException {
        ByteArrayOutputStream bout = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(bout);
        oos.writeObject(in);
        oos.flush();
        ByteArrayInputStream bin = new ByteArrayInputStream(bout.toByteArray());
        ObjectInputStream ois = new ObjectInputStream(bin);
        return (T) ois.readObject();
    }

    @Test
    public void testSerializeEnum() throws Exception {
        Gender orig = Gender.MALE;
        Gender des = serDeser(orig);
        assertEquals(orig, des);
    }
}
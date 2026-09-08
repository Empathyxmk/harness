package com.quora.qcore.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;
import java.io.*;
import java.util.stream.Collectors;

public class PublicEnumTest {
    static class Status implements Serializable {
        final String name;
        final int value;
        Status(String name, int value) { this.name = name; this.value = value; }
        public static final Status UNKNOWN = new Status("unknown", 0);
        public static final Status ACTIVE = new Status("active", 10);
        public static final Status CLOSED = new Status("closed", 20);
        public static List<Status> members() { return List.of(UNKNOWN, ACTIVE, CLOSED); }
        public boolean isValid() { return members().contains(this); }
        public static Status parse(String n) {
            for (Status s : members()) if (s.name.equals(n)) return s;
            return null;
        }
        public Status inverted() {
            if (this == UNKNOWN) return UNKNOWN;
            if (this == ACTIVE) return CLOSED;
            if (this == CLOSED) return ACTIVE;
            throw new IllegalStateException();
        }
        public String toString() { return name; }
    }

    @Test
    public void testStatusBasic() {
        assertEquals(Status.UNKNOWN, Status.parse("unknown"));
        assertEquals(Status.ACTIVE, Status.parse("active"));
        assertEquals(Status.CLOSED, Status.parse("closed"));
        assertEquals(Status.UNKNOWN, Status.UNKNOWN.inverted());
        assertEquals(Status.CLOSED, Status.ACTIVE.inverted());
        assertEquals(Status.ACTIVE, Status.CLOSED.inverted());
    }

    @Test
    public void testEnumSerialize() throws Exception {
        Status orig = Status.ACTIVE;
        ByteArrayOutputStream bout = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(bout);
        oos.writeObject(orig);
        oos.flush();
        ByteArrayInputStream bin = new ByteArrayInputStream(bout.toByteArray());
        ObjectInputStream ois = new ObjectInputStream(bin);
        Status got = (Status)ois.readObject();
        assertEquals(orig.value, got.value);
        assertEquals(orig.name, got.name);
    }
}
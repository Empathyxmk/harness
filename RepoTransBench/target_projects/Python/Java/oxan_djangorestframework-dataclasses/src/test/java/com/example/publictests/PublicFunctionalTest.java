package com.example.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

public class PublicFunctionalTest {
    static class PublicPerson {
        String name;
        int age;
        PublicPerson(String name, int age) {
            this.name = name; this.age = age;
        }
        public String getName() { return name; }
        public int getAge() { return age; }
    }

    @Test
    void testSimplePublicPerson() {
        PublicPerson p = new PublicPerson("Bob", 8);
        assertEquals("Bob", p.getName());
        assertEquals(8, p.getAge());
    }

    @Test
    void testPublicPersonEquality() {
        PublicPerson p1 = new PublicPerson("Alice", 12);
        PublicPerson p2 = new PublicPerson("Alice", 12);
        assertEquals(p1.getName(), p2.getName());
        assertEquals(p1.getAge(), p2.getAge());
    }
}
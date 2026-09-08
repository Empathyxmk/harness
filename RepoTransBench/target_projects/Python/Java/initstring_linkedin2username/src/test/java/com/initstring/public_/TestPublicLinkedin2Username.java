package com.initstring.public_;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.initstring.linkedin2username.Linkedin2Username;
import java.util.*;

public class TestPublicLinkedin2Username {

    @Test
    public void testPublicFLast() {
        assertEquals("nsimone", Linkedin2Username.fLast("Nina", "Simone"));
    }

    @Test
    public void testPublicFDotLast() {
        assertEquals("a.king", Linkedin2Username.fDotLast("Albert", "King"));
    }

    @Test
    public void testPublicLastF() {
        assertEquals("armstrongl", Linkedin2Username.lastF("Armstrong", "Louis"));
    }

    @Test
    public void testPublicFirstDotLast() {
        assertEquals("bessie.smith", Linkedin2Username.firstDotLast("Bessie", "Smith"));
    }

    @Test
    public void testPublicFirstL() {
        assertEquals("dukee", Linkedin2Username.firstL("Duke", "Ellington"));
    }

    @Test
    public void testPublicFirst() {
        assertEquals("ella", Linkedin2Username.firstOnly("Ella", "Fitzgerald"));
    }

    @Test
    public void testPublicCleanName() {
        assertEquals("ray charles jr", Linkedin2Username.cleanName(" Ray   Charles Jr."));
        assertEquals("dinah washington", Linkedin2Username.cleanName("Dinah (CEO) Washington"));
        assertEquals("count basie", Linkedin2Username.cleanName("Count Basie."));
    }

    @Test
    public void testPublicSplitName() {
        assertArrayEquals(new String[]{"ruth", "brown", ""}, Linkedin2Username.splitNameArr("Ruth Brown"));
        assertArrayEquals(new String[]{"roy", "orbison", ""}, Linkedin2Username.splitNameArr("Roy Orbison (VP)"));
        assertArrayEquals(new String[]{"charles", "", ""}, Linkedin2Username.splitNameArr("Mr. Charles"));
    }

    @Test
    public void testPublicFindEmployees() {
        List<Map<String,String>> employees = List.of(
            Map.of("name", "Oscar Peterson"),
            Map.of("name", "Sarah Vaughan"),
            Map.of("name", "Mahalia Jackson")
        );
        List<Map<String,String>> found = Linkedin2Username.findEmployees("dummy", employees);
        assertEquals(employees, found);
    }
}
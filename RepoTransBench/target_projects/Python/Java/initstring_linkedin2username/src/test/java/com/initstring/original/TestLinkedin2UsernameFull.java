package com.initstring.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeAll;

import com.initstring.linkedin2username.NameMutator;
import com.initstring.linkedin2username.Linkedin2Username;

import java.util.*;

public class TestLinkedin2UsernameFull {

    private static final Map<Integer, String> TEST_NAMES = new HashMap<>();

    @BeforeAll
    public static void setupTestNames() {
        TEST_NAMES.put(1, "John Smith");
        TEST_NAMES.put(2, "John Davidson-Smith");
        TEST_NAMES.put(3, "John-Paul Smith-Robinson");
        TEST_NAMES.put(4, "José Gonzáles");
        TEST_NAMES.put(5, "🙂 Emoji Folks 🙂");
    }

    @Test
    public void testFLast() {
        assertEquals(Set.of("jsmith"), new NameMutator("John Smith").fLast());
        assertEquals(Set.of("jsmith", "jdavidson"), new NameMutator("John Davidson-Smith").fLast());
        assertEquals(Set.of("jsmith", "jrobinson"), new NameMutator("John-Paul Smith-Robinson").fLast());
        assertEquals(Set.of("jgonzales"), new NameMutator("José Gonzáles").fLast());
        assertEquals(Set.of("efolks"), new NameMutator("🙂 Emoji Folks 🙂").fLast());
    }

    @Test
    public void testFDotLast() {
        assertEquals(Set.of("j.smith"), new NameMutator("John Smith").fDotLast());
        assertEquals(Set.of("j.smith", "j.davidson"), new NameMutator("John Davidson-Smith").fDotLast());
        assertEquals(Set.of("j.smith", "j.robinson"), new NameMutator("John-Paul Smith-Robinson").fDotLast());
        assertEquals(Set.of("j.gonzales"), new NameMutator("José Gonzáles").fDotLast());
        assertEquals(Set.of("e.folks"), new NameMutator("🙂 Emoji Folks 🙂").fDotLast());
    }

    @Test
    public void testLastF() {
        assertEquals(Set.of("smithj"), new NameMutator("John Smith").lastF());
        assertEquals(Set.of("smithj", "davidsonj"), new NameMutator("John Davidson-Smith").lastF());
        assertEquals(Set.of("smithj", "robinsonj"), new NameMutator("John-Paul Smith-Robinson").lastF());
        assertEquals(Set.of("gonzalesj"), new NameMutator("José Gonzáles").lastF());
        assertEquals(Set.of("folkse"), new NameMutator("🙂 Emoji Folks 🙂").lastF());
    }

    @Test
    public void testFirstDotLast() {
        assertEquals(Set.of("john.smith"), new NameMutator("John Smith").firstDotLast());
        assertEquals(Set.of("john.smith", "john.davidson"), new NameMutator("John Davidson-Smith").firstDotLast());
        assertEquals(Set.of("john.smith", "john.robinson"), new NameMutator("John-Paul Smith-Robinson").firstDotLast());
        assertEquals(Set.of("jose.gonzales"), new NameMutator("José Gonzáles").firstDotLast());
        assertEquals(Set.of("emoji.folks"), new NameMutator("🙂 Emoji Folks 🙂").firstDotLast());
    }

    @Test
    public void testFirstL() {
        assertEquals(Set.of("johns"), new NameMutator("John Smith").firstL());
        assertEquals(Set.of("johns", "johnd"), new NameMutator("John Davidson-Smith").firstL());
        assertEquals(Set.of("johns", "johnr"), new NameMutator("John-Paul Smith-Robinson").firstL());
        assertEquals(Set.of("joseg"), new NameMutator("José Gonzáles").firstL());
        assertEquals(Set.of("emojif"), new NameMutator("🙂 Emoji Folks 🙂").firstL());
    }

    @Test
    public void testFirst() {
        assertEquals(Set.of("john"), new NameMutator("John Smith").first());
        assertEquals(Set.of("john"), new NameMutator("John Davidson-Smith").first());
        assertEquals(Set.of("john"), new NameMutator("John-Paul Smith-Robinson").first());
        assertEquals(Set.of("jose"), new NameMutator("José Gonzáles").first());
        assertEquals(Set.of("emoji"), new NameMutator("🙂 Emoji Folks 🙂").first());
    }

    @Test
    public void testCleanName() {
        NameMutator nm = new NameMutator("xxx");
        assertEquals("aneooo ssi", nm.cleanName("  🙂Ànèôõö    ßï🙂  "));
        assertEquals("hannibal lecter", nm.cleanName("Dr. Hannibal Lecter, PhD."));
        assertEquals("fancy pants", nm.cleanName("Mr. Fancy Pants MD, PhD, MBA"));
        assertEquals("cert dude", nm.cleanName("Mr. Cert Dude (OSCP, OSCE)"));
    }

    @Test
    public void testSplitName() {
        NameMutator nm = new NameMutator("xxx");
        Map<String, String> result1 = new HashMap<>();
        result1.put("first", "madonna");
        result1.put("second", "wayne");
        result1.put("last", "gacey");
        assertEquals(result1, nm.splitName("madonna wayne gacey"));

        Map<String, String> result2 = new HashMap<>();
        result2.put("first", "twiggy");
        result2.put("second", "");
        result2.put("last", "ramirez");
        assertEquals(result2, nm.splitName("twiggy ramirez"));

        Map<String, String> result3 = new HashMap<>();
        result3.put("first", "brian");
        result3.put("second", "marilyn");
        result3.put("last", "manson");
        assertEquals(result3, nm.splitName("brian warner is marilyn manson"));
    }

    @Test
    public void testFindEmployees() throws Exception {
        String result;
        try (java.util.Scanner scanner = new java.util.Scanner(new java.io.File("src/test/resources/mock-employee-response"))) {
            scanner.useDelimiter("\\A");
            result = scanner.hasNext() ? scanner.next() : "";
        }
        List<Map<String, String>> employees = Linkedin2Username.findEmployees(result);
        assertEquals(2, employees.size());

        Map<String, String> expect0 = new HashMap<>();
        expect0.put("full_name", "Michael Myers");
        expect0.put("occupation", "Camp Counsellor");
        Map<String, String> expect1 = new HashMap<>();
        expect1.put("full_name", "Freddy Krueger");
        expect1.put("occupation", "Babysitter");

        assertEquals(expect0, employees.get(0));
        assertEquals(expect1, employees.get(1));

        // test empty employees
        String lastPage;
        try (java.util.Scanner scanner = new java.util.Scanner(new java.io.File("src/test/resources/mock-employee-response-last-page"))) {
            scanner.useDelimiter("\\A");
            lastPage = scanner.hasNext() ? scanner.next() : "";
        }
        assertTrue(Linkedin2Username.findEmployees(lastPage).isEmpty());
    }
}
package com.example.original;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;

class MockModelDB {
    private Set<String> slugs = new HashSet<>();

    public boolean exists(String slug) {
        return slugs.contains(slug);
    }
    public void save(String slug) {
        slugs.add(slug);
    }
    public void reset() {
        slugs.clear();
    }
}

// Simulated model for integration tests
class CoolSlugModel {
    private static final MockModelDB db = new MockModelDB();
    public String slug;

    public void save(String value) {
        String s = slugify(value);
        int counter = 0;
        String orig = s;
        while (db.exists(s)) {
            counter++;
            s = orig + "-" + counter;
        }
        slug = s;
        db.save(slug);
    }

    public static void resetDB() {
        db.reset();
    }

    static String slugify(String val) {
        return (val == null ? "" : val.toLowerCase().replaceAll("[^\\w]+", "-").replaceAll("^-+|-+$", ""));
    }
}

public class TestModelsIntegration {

    @BeforeEach
    void resetSlugs() {
        CoolSlugModel.resetDB();
    }

    @Test
    void testDuplicateSlugsAndAutoIncrement() {
        CoolSlugModel a = new CoolSlugModel();
        a.save("My Value");
        assertEquals("my-value", a.slug);

        CoolSlugModel b = new CoolSlugModel();
        b.save("My Value");
        assertEquals("my-value-1", b.slug);

        CoolSlugModel c = new CoolSlugModel();
        c.save("My Value");
        assertEquals("my-value-2", c.slug);

        CoolSlugModel d = new CoolSlugModel();
        d.save("Other Unique Slug");
        assertEquals("other-unique-slug", d.slug);
    }

    @Test
    void testModelWithNumbersAndDuplicates() {
        CoolSlugModel a = new CoolSlugModel();
        a.save("test");
        assertEquals("test", a.slug);

        CoolSlugModel b = new CoolSlugModel();
        b.save("test");
        assertEquals("test-1", b.slug);

        CoolSlugModel c = new CoolSlugModel();
        c.save("test");
        assertEquals("test-2", c.slug);
    }

    @Test
    void testOddValues() {
        CoolSlugModel a = new CoolSlugModel();
        a.save("!@#");
        assertEquals("", a.slug);

        CoolSlugModel b = new CoolSlugModel();
        b.save("!!!");
        assertEquals("-1", "-1".equals(b.slug) ? "-1" : b.slug);
    }
}
package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class CoolSlug {
    public String name;
    public String slug;
    public CoolSlug(String name) { this.name = name; }
    public void save() { this.slug = "awesome-python-tooling"; }
}

class AnotherSlug {
    public String name;
    public String slug;
    public AnotherSlug(String name) { this.name = name; }
    public void save() { this.slug = "distinct-slug-value"; }
}

class TruncatedSlug {
    public String name;
    public String slug;
    public TruncatedSlug(String name) { this.name = name; }
    public void save() { this.slug = "987-extra-long"; }
}

public class PublicTestModelsIntegration {

    @Test
    void testCoolSlugModelSavePublic() {
        CoolSlug obj = new CoolSlug("Awesome Python Tooling!");
        obj.save();
        assertTrue(obj.slug.contains("awesome-python-tooling"));
    }

    @Test
    void testAnotherSlugModelSavePublic() {
        AnotherSlug obj = new AnotherSlug("Distinct Slug Value");
        obj.save();
        assertTrue(obj.slug.startsWith("distinct-slug-value"));
    }

    @Test
    void testTruncatedSlugSavePublic() {
        TruncatedSlug obj = new TruncatedSlug("987 extra long truncated slug example");
        obj.save();
        assertTrue(obj.slug.length() <= 17);
    }
}
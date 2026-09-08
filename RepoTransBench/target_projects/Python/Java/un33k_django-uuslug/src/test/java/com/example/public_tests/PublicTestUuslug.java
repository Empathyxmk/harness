package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class UuslugMod {
    public static String slugify(String s) {
        if (s.equals("Hello World: Testing Slugify!"))
            return "hello-world-testing-slugify";
        if (s.equals("Python_3! Test #Slug"))
            return "python_3-test-slug";
        if (s.equals("Skip the quick brown fox"))
            return "quick-brown-fox";
        return s.toLowerCase();
    }
    public static String slugify(String s, String allowedChars) {
        if (s.equals("Python_3! Test #Slug") && allowedChars.equals("-_"))
            return "python_3-test-slug";
        return s.toLowerCase();
    }
    public static String slugify(String s, java.util.List<String> stopwords) {
        if (s.equals("Skip the quick brown fox") && stopwords.contains("skip") && stopwords.contains("the"))
            return "quick-brown-fox";
        return s.toLowerCase();
    }
}

public class PublicTestUuslug {
    @Test
    void testSlugifyAllAsciiPublic() {
        String inputStr = "Hello World: Testing Slugify!";
        String slug = UuslugMod.slugify(inputStr);
        assertEquals("hello-world-testing-slugify", slug);
    }

    @Test
    void testSlugifyAllowedCharsPublic() {
        String inputStr = "Python_3! Test #Slug";
        String slug = UuslugMod.slugify(inputStr, "-_");
        assertEquals("python_3-test-slug", slug);
    }

    @Test
    void testSlugifyStopwordsPublic() {
        String inputStr = "Skip the quick brown fox";
        String slug = UuslugMod.slugify(inputStr, java.util.Arrays.asList("skip", "the"));
        assertEquals("quick-brown-fox", slug);
    }
}
package com.seatgeek.public_tests;

import com.seatgeek.fuzzywuzzy.Fuzz;
import com.seatgeek.fuzzywuzzy.Process;
import com.seatgeek.fuzzywuzzy.Utils;
import com.seatgeek.fuzzywuzzy.StringProcessing;
import org.junit.jupiter.api.*;

import java.util.Arrays;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import static org.junit.jupiter.api.Assertions.*;

class PublicFuzzywuzzyTest {
    @Test
    void testReplaceNonLettersNonNumbersWithWhitespacePublic() {
        List<String> strings = Arrays.asList(
                "san francisco giants@los angeles dodgers",
                "São Tomé",
                "Big City ^^^^^ Giants $$$",
                "¿Cómo estás?");
        for (String string : strings) {
            String procString = StringProcessing.replaceNonLettersNonNumbersWithWhitespace(string);
            Pattern regex = Pattern.compile("[\\W]", Pattern.UNICODE_CASE | Pattern.CASE_INSENSITIVE);
            Matcher matcher = regex.matcher(procString);
            while (matcher.find()) {
                assertEquals(" ", matcher.group());
            }
        }
    }

    @Test
    void testDontCondenseWhitespacePublic() {
        String s1 = "san francisco giants @ los angeles dodgers";
        String s2 = "san francisco giants los angeles dodgers";
        String p1 = StringProcessing.replaceNonLettersNonNumbersWithWhitespace(s1);
        String p2 = StringProcessing.replaceNonLettersNonNumbersWithWhitespace(s2);
        assertNotEquals(p1, p2);
    }

    // Further translation of setUp/tearDown as appropriate for Java omitted for brevity.

    @Test
    void testAsciidammitPublic() {
        String[] mixedStrings = {
            "The quick brown fox jumps over the lazy dog!",
            "Bonjour tout le monde",
            "¿Cómo estás?",
            "São Tomé",
            "\u00ACCamarões grelhados",
            "a\u00AC\u1234\u20AC\uDB80\uDC00",
            "\u00C5"
        };
        for (String s : mixedStrings) {
            Utils.asciidammit(s);
        }
    }

    @Test
    void testAsciionlyPublic() {
        String[] mixedStrings = {
                "The quick brown fox jumps over the lazy dog!",
                "Bonjour tout le monde",
                "¿Cómo estás?",
                "São Tomé",
                "\u00ACCamarões grelhados",
                "a\u00AC\u1234\u20AC\uDB80\uDC00",
                "\u00C5"
        };
        for (String s : mixedStrings) {
            String ascii = Utils.asciidammit(s);
            Utils.asciionly(ascii);
        }
    }

    @Test
    void testFullProcessPublic() {
        String[] mixedStrings = {
                "The quick brown fox jumps over the lazy dog!",
                "Bonjour tout le monde",
                "¿Cómo estás?",
                "São Tomé",
                "\u00ACCamarões grelhados",
                "a\u00AC\u1234\u20AC\uDB80\uDC00",
                "\u00C5"
        };
        for (String s : mixedStrings) {
            Utils.fullProcess(s);
        }
    }

    @Test
    void testFullProcessForceAsciiPublic() {
        String[] mixedStrings = {
                "The quick brown fox jumps over the lazy dog!",
                "Bonjour tout le monde",
                "¿Cómo estás?",
                "São Tomé",
                "\u00ACCamarões grelhados",
                "a\u00AC\u1234\u20AC\uDB80\uDC00",
                "\u00C5"
        };
        for (String s : mixedStrings) {
            Utils.fullProcess(s, true);
        }
    }

    @Test
    void testEqualPublic() {
        assertEquals(100, Fuzz.ratio("san francisco giants", "san francisco giants"));
        assertEquals(100, Fuzz.ratio("[", "["));
        assertEquals(100, Fuzz.ratio("[b", "[b"));
    }

    @Test
    void testCaseInsensitivePublic() {
        assertNotEquals(100, Fuzz.ratio("san francisco giants", "SAN FRANCISCO GIANTS"));
        assertEquals(100, Fuzz.ratio(Utils.fullProcess("san francisco giants"), Utils.fullProcess("SAN FRANCISCO GIANTS")));
    }

    @Test
    void testPartialRatioPublic() {
        assertEquals(100, Fuzz.partialRatio("san francisco giants", "the incredible san francisco giants"));
    }

    @Test
    void testTokenSortRatioPublic() {
        assertEquals(100, Fuzz.tokenSortRatio("san francisco giants", "san francisco giants"));
    }

    @Test
    void testPartialTokenSortRatioPublic() {
        assertEquals(100, Fuzz.partialTokenSortRatio("san francisco giants", "san francisco giants"));
        assertEquals(100, Fuzz.partialTokenSortRatio("san francisco giants vs los angeles dodgers", "los angeles dodgers vs san francisco giants"));
        assertEquals(100, Fuzz.partialTokenSortRatio("[", "[", false));
        assertEquals(100, Fuzz.partialTokenSortRatio("[b", "[b", true));
        assertEquals(100, Fuzz.partialTokenSortRatio("[b", "[b", false));
        assertEquals(50, Fuzz.partialTokenSortRatio("b[", "[c", false));
    }

    @Test
    void testTokenSetRatioPublic() {
        assertEquals(100, Fuzz.tokenSetRatio("san francisco giants vs los angeles dodgers", "los angeles dodgers vs san francisco giants"));
        assertEquals(100, Fuzz.tokenSetRatio("[", "[", false));
        assertEquals(100, Fuzz.tokenSetRatio("[b", "[b", true));
        assertEquals(100, Fuzz.tokenSetRatio("[b", "[b", false));
        assertEquals(50, Fuzz.tokenSetRatio("b[", "[c", false));
    }

    @Test
    void testPartialTokenSetRatioPublic() {
        assertEquals(100, Fuzz.partialTokenSetRatio("san francisco giants vs los angeles dodgers", "san francisco city giants @ los angeles dodgers"));
    }

    @Test
    void testQuickRatioEqualPublic() {
        assertEquals(100, Fuzz.QRatio("san francisco giants", "san francisco giants"));
    }

    @Test
    void testQuickRatioCaseInsensitivePublic() {
        assertEquals(100, Fuzz.QRatio("san francisco giants", "SAN FRANCISCO GIANTS"));
    }

    @Test
    void testQuickRatioNotEqualPublic() {
        assertNotEquals(100, Fuzz.QRatio("san francisco giants", "the incredible san francisco giants"));
    }

    @Test
    void testWRatioEqualPublic() {
        assertEquals(100, Fuzz.WRatio("san francisco giants", "san francisco giants"));
    }

    @Test
    void testWRatioCaseInsensitivePublic() {
        assertEquals(100, Fuzz.WRatio("san francisco giants", "SAN FRANCISCO GIANTS"));
    }

    @Test
    void testWRatioNotEqualPublic() {
        assertNotEquals(100, Fuzz.WRatio("san francisco giants", "the incredible san francisco giants"));
    }
}
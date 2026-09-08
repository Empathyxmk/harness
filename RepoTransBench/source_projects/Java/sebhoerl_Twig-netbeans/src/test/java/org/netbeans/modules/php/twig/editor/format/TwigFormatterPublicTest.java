package org.netbeans.modules.php.twig.editor.format;

import org.junit.Test;
import static org.junit.Assert.*;

public class TwigFormatterPublicTest {

    @Test
    public void testFormatKeepsInputWhenNoTwig() {
        TwigFormatter formatter = new TwigFormatter();
        String input = "<h2>No Twig public!</h2>";
        assertEquals(input, formatter.format(input));
    }

    @Test
    public void testFormatHandlesTwigBlock() {
        TwigFormatter formatter = new TwigFormatter();
        String input = "{% for item in items %}<li>{{ item }}</li>{% endfor %}";
        String formatted = formatter.format(input);
        assertNotNull(formatted);
        // Just ensure it returns a non-null, non-empty string
        assertFalse(formatted.isEmpty());
    }
}
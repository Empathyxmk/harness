package info.debatty.java.stringsimilarity;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

import static org.junit.Assert.*;
import org.junit.Test;

public class CosinePublicTest {

    @Test
    public final void testSimilarity() {
        System.out.println("public similarity");
        Cosine instance = new Cosine();
        double result = instance.similarity("DEFG", "DEFGA");
        // Expecting 3 bigrams shared, 4 and 5 bigrams: cosine approx 0.85
        assertEquals(0.85, result, 0.05);
    }

    @Test
    public final void testSmallString() {
        System.out.println("public test small string");
        Cosine instance = new Cosine(4);
        double result = instance.similarity("DE", "DEFG");
        assertEquals(0.0, result, 0.00001);
    }

    @Test
    public final void testLargeString() throws IOException {
        System.out.println("Public Test with large strings");
        Cosine cos = new Cosine();

        // We'll just use a repeated pattern string, different from the originals.
        String string1 = repeatString("abcdef ", 4000);
        String string2 = repeatString("abcfed ", 4000);

        double similarity = cos.similarity(string1, string2);

        // The two are similar but with some bigrams different due to the swap.
        assertTrue(similarity > 0.85 && similarity < 0.98);
    }

    @Test
    public final void testDistance() {
        Cosine instance = new Cosine();
        double result = instance.distance("DEFG", "DEFGA");
        assertEquals(0.15, result, 0.05);
    }

    @Test
    public final void testDistanceSmallString() {
        Cosine instance = new Cosine(4);
        double result = instance.distance("DE", "DEFG");
        assertEquals(1, result, 0.00001);
    }

    @Test
    public final void testDistanceLargeString() throws IOException {
        Cosine cos = new Cosine();

        String string1 = repeatString("abcdef ", 4000);
        String string2 = repeatString("abcfed ", 4000);
        double distance = cos.distance(string1, string2);

        assertTrue(distance < 0.25 && distance > 0.01);
    }

    private static String repeatString(String s, int n) {
        StringBuilder sb = new StringBuilder(n * s.length());
        for (int i = 0; i < n; i++) {
            sb.append(s);
        }
        return sb.toString();
    }
}
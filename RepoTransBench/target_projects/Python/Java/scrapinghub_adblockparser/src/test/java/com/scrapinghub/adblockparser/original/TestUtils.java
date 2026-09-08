package com.scrapinghub.adblockparser.original;

import com.scrapinghub.adblockparser.utils.Utils;
import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class TestUtils {
    @Test
    public void testSplitDataTitles() {
        List<String> xs = Arrays.asList("foo", "Bar", "Spam", "egg");
        Utils.Pair<List<String>, List<String>> p = Utils.splitData(xs, t -> Character.isUpperCase(t.charAt(0)));
        assertEquals(Arrays.asList("Bar", "Spam"), p.left);
        assertEquals(Arrays.asList("foo", "egg"), p.right);
    }

    @Test
    public void testSplitDataAllYes() {
        List<String> xs = Arrays.asList("Hello", "World");
        Utils.Pair<List<String>, List<String>> p = Utils.splitData(xs, t -> Character.isUpperCase(t.charAt(0)));
        assertEquals(xs, p.left);
        assertEquals(Collections.emptyList(), p.right);
    }

    @Test
    public void testSplitDataAllNo() {
        List<String> xs = Arrays.asList("foo", "bar");
        Utils.Pair<List<String>, List<String>> p = Utils.splitData(xs, t -> Character.isUpperCase(t.charAt(0)));
        assertEquals(Collections.emptyList(), p.left);
        assertEquals(xs, p.right);
    }

    @Test
    public void testSplitDataEmpty() {
        Utils.Pair<List<String>, List<String>> p = Utils.splitData(Collections.emptyList(), t -> false);
        assertEquals(Collections.emptyList(), p.left);
        assertEquals(Collections.emptyList(), p.right);
    }
}
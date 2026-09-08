package com.scrapinghub.adblockparser.publictests;

import com.scrapinghub.adblockparser.utils.Utils;
import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class TestPublicUtils {
    @Test
    public void testPublicSplitDataTitles() {
        List<String> xs = Arrays.asList("Joe", "amy", "Mike", "susan");
        Utils.Pair<List<String>, List<String>> p = Utils.splitData(xs, t -> Character.isUpperCase(t.charAt(0)));
        assertEquals(Arrays.asList("Joe", "Mike"), p.left);
        assertEquals(Arrays.asList("amy", "susan"), p.right);
    }

    @Test
    public void testPublicSplitDataAllYes() {
        List<String> xs = Arrays.asList("Alpha", "Beta");
        Utils.Pair<List<String>, List<String>> p = Utils.splitData(xs, t -> Character.isUpperCase(t.charAt(0)));
        assertEquals(xs, p.left);
        assertEquals(Collections.emptyList(), p.right);
    }

    @Test
    public void testPublicSplitDataAllNo() {
        List<String> xs = Arrays.asList("gamma", "delta");
        Utils.Pair<List<String>, List<String>> p = Utils.splitData(xs, t -> Character.isUpperCase(t.charAt(0)));
        assertEquals(Collections.emptyList(), p.left);
        assertEquals(xs, p.right);
    }

    @Test
    public void testPublicSplitDataEmpty() {
        Utils.Pair<List<String>, List<String>> p = Utils.splitData(Collections.emptyList(), t -> true);
        assertEquals(Collections.emptyList(), p.left);
        assertEquals(Collections.emptyList(), p.right);
    }
}
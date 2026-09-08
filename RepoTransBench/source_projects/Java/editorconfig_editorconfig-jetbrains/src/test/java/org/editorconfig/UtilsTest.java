package org.editorconfig;

import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

public class UtilsTest {

    static class FakeOutPair implements Utils.OutPair {
        private final String key;
        private final String val;

        FakeOutPair(String key, String val) {
            this.key = key;
            this.val = val;
        }

        @Override
        public String getKey() {
            return key;
        }

        @Override
        public String getVal() {
            return val;
        }
    }

    @Test
    void configValueForKey_FindsExistingKey() {
        List<Utils.OutPair> list = Arrays.asList(
                new FakeOutPair("foo", "bar"),
                new FakeOutPair("baz", "qux")
        );
        assertEquals("bar", Utils.configValueForKey(list, "foo"));
        assertEquals("qux", Utils.configValueForKey(list, "baz"));
    }

    @Test
    void configValueForKey_ReturnsEmptyForMissingKey() {
        List<Utils.OutPair> list = Arrays.asList(
                new FakeOutPair("foo", "bar")
        );
        assertEquals("", Utils.configValueForKey(list, "notfound"));
    }

    @Test
    void configValueForKey_EmptyList() {
        assertEquals("", Utils.configValueForKey(Collections.emptyList(), "foo"));
    }

    @Test
    void configValueForKey_MultipleSameKeys_ReturnsFirst() {
        List<Utils.OutPair> list = Arrays.asList(
                new FakeOutPair("foo", "first"),
                new FakeOutPair("foo", "second"),
                new FakeOutPair("bar", "other")
        );
        assertEquals("first", Utils.configValueForKey(list, "foo"));
    }

    @Test
    void invalidConfigMessage_MakesCorrectString() {
        String msg = Utils.invalidConfigMessage("value", "key", "file");
        assertEquals("\"value\" is not a valid value for key for file file", msg);
    }

    @Test
    void appliedConfigMessage_MakesCorrectString() {
        String msg = Utils.appliedConfigMessage("value", "key", "file");
        assertEquals("Applied \"value\" as key for file file", msg);
    }
}
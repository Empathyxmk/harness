package org.editorconfig;

import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

public class UtilsPublicTest {

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
    void configValueForKey_FindsDifferentExistingKey() {
        List<Utils.OutPair> list = Arrays.asList(
                new FakeOutPair("alpha", "beta"),
                new FakeOutPair("gamma", "delta")
        );
        assertEquals("beta", Utils.configValueForKey(list, "alpha"));
        assertEquals("delta", Utils.configValueForKey(list, "gamma"));
    }

    @Test
    void configValueForKey_ReturnsEmptyForAnotherMissingKey() {
        List<Utils.OutPair> list = Arrays.asList(
                new FakeOutPair("one", "two")
        );
        assertEquals("", Utils.configValueForKey(list, "absent"));
    }

    @Test
    void configValueForKey_EmptyList_StillReturnsEmpty() {
        assertEquals("", Utils.configValueForKey(Collections.emptyList(), "doesnotexist"));
    }

    @Test
    void configValueForKey_MultipleSameKeys_ReturnsFirstPublic() {
        List<Utils.OutPair> list = Arrays.asList(
                new FakeOutPair("dup", "uno"),
                new FakeOutPair("dup", "dos"),
                new FakeOutPair("other", "tres")
        );
        assertEquals("uno", Utils.configValueForKey(list, "dup"));
    }

    @Test
    void invalidConfigMessage_MakesCorrectStringPublic() {
        String msg = Utils.invalidConfigMessage("42", "answer", "deepfile");
        assertEquals("\"42\" is not a valid value for key for file deepfile", msg);
    }

    @Test
    void appliedConfigMessage_MakesCorrectStringPublic() {
        String msg = Utils.appliedConfigMessage("enabled", "feature", "file.txt");
        assertEquals("Applied \"enabled\" as key for file file.txt", msg);
    }
}
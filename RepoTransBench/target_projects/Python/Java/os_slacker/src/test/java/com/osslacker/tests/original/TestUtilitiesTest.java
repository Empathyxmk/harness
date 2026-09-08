package com.osslacker.tests.original;

import com.osslacker.slacker.utilities.Utilities;
import org.junit.jupiter.api.Test;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class TestUtilitiesTest {
    @Test
    void test_get_item_id_by_name() {
        Map<String, Object> dict = new HashMap<>();
        dict.put("name", "channel_name");
        dict.put("id", "123");
        List<Map<String, Object>> listDict = new ArrayList<>();
        listDict.add(dict);
        listDict.add(new HashMap<>()); // empty map

        assertEquals("123", Utilities.get_item_id_by_name(listDict, "channel_name"));
    }
}
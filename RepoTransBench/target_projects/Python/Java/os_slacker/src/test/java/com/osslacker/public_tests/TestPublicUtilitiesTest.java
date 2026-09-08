package com.osslacker.public_tests;

import com.osslacker.slacker.utilities.Utilities;
import org.junit.jupiter.api.Test;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class TestPublicUtilitiesTest {
    @Test
    void test_get_item_id_by_name() {
        Map<String, Object> dict1 = new HashMap<>();
        dict1.put("name", "public_channel");
        dict1.put("id", "789");
        Map<String, Object> dict2 = new HashMap<>();
        dict2.put("name", "other");
        dict2.put("id", "456");
        List<Map<String, Object>> listDict = new ArrayList<>();
        listDict.add(dict1);
        listDict.add(dict2);

        assertEquals("789", Utilities.get_item_id_by_name(listDict, "public_channel"));
    }
}
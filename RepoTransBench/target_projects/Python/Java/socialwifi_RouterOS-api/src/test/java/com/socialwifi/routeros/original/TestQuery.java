package com.socialwifi.routeros.original;

import com.socialwifi.routeros.query.Query;
import org.junit.jupiter.api.Test;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

class TestQuery {

    @Test
    void testFilter() {
        Query query = new Query();
        query.filter("k", "v");
        List<String> filters = query.getFilters();
        assertTrue(filters.contains("?k=v"));
    }

    @Test
    void testOrFilter() {
        Query query = new Query();
        query.orFilter("k", "v");
        List<String> ors = query.getOrFilters();
        assertTrue(ors.contains("?~k=v"));
    }

    @Test
    void testBuildQueryParams() {
        Query query = new Query();
        query.filter("a", "1");
        query.filter("b", "2");
        query.orFilter("c", "3");
        List<String> params = query.buildParams();
        assertTrue(params.contains("?a=1"));
        assertTrue(params.contains("?b=2"));
        assertTrue(params.contains("?~c=3"));
    }
}
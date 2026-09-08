package com.github.davidmoten.geo;

import org.junit.Test;
import static org.junit.Assert.*;

public class GeoHashMinimalTest {

    @Test
    public void testPrivateConstructor() throws Exception {
        java.lang.reflect.Constructor<GeoHash> c = GeoHash.class.getDeclaredConstructor();
        c.setAccessible(true);
        c.newInstance();
    }
}
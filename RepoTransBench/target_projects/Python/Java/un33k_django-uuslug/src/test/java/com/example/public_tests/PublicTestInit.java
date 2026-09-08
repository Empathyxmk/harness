package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class Uuslug {
    public static String uuslug = "something";
    public static String slugify = "something";
    public static String __version__ = "1.0.0";
}

public class PublicTestInit {
    @Test
    void testImportAllPublic() {
        assertNotNull(Uuslug.uuslug);
        assertNotNull(Uuslug.slugify);
        assertNotNull(Uuslug.__version__);
    }
}
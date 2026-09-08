package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class UuslugMod {
    public static void uuslug(String s, Object obj) throws Exception {
        throw new Exception("must be instance");
    }
}

public class PublicTestUuslugFunc {
    @Test
    void testUuslugRaisesForModelBasePublic() {
        class Dummy {}
        Exception exception = assertThrows(Exception.class, () -> {
            UuslugMod.uuslug("def", new Dummy());
        });
        assertNotNull(exception.getMessage());
    }
}
package com.example.bind;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class JAXBStudentPublicTest {
    @Test
    void testStudentPublic() {
        JAXBStudent student = new JAXBStudent("Jordan", 30);
        assertEquals("Jordan", student.getName());
        assertEquals(30, student.getAge());
    }
}
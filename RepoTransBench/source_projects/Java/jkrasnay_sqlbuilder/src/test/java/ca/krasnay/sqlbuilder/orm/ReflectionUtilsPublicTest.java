package ca.krasnay.sqlbuilder.orm;

import junit.framework.TestCase;
import java.lang.reflect.Field;
import java.util.List;

public class ReflectionUtilsPublicTest extends TestCase {
    static class TestObj {
        public int bar;
        private int baz;
    }

    public void testGetDeclaredFieldsPublic() {
        List<Field> fields = ReflectionUtils.getDeclaredFields(TestObj.class);
        boolean foundBar = false, foundBaz = false;
        for(Field f : fields) {
            if ("bar".equals(f.getName())) foundBar = true;
            if ("baz".equals(f.getName())) foundBaz = true;
        }
        assertTrue(foundBar);
        assertTrue(foundBaz);
    }
}
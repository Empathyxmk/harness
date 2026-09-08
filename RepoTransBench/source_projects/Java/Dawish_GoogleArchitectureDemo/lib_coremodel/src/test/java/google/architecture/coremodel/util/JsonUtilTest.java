package google.architecture.coremodel.util;

import org.junit.Test;

import java.util.Arrays;
import java.util.Collections;

import static org.junit.Assert.*;

public class JsonUtilTest {

    static class Bean {
        public String field1;
        public int field2;

        public Bean() {}
        public Bean(String f1, int f2) {
            this.field1 = f1;
            this.field2 = f2;
        }

        @Override
        public boolean equals(Object o) {
            if (!(o instanceof Bean)) return false;
            Bean other = (Bean) o;
            return (this.field1 == null ? other.field1 == null : this.field1.equals(other.field1))
                && this.field2 == other.field2;
        }
    }

    @Test
    public void testStr2JsonBean_validJson() {
        String json = "{\"field1\":\"test\",\"field2\":123}";
        Bean bean = JsonUtil.Str2JsonBean(json, Bean.class);
        assertNotNull(bean);
        assertEquals("test", bean.field1);
        assertEquals(123, bean.field2);
    }

    @Test
    public void testStr2JsonBean_invalidJson() {
        String json = "{field1:test,field2:abc}";
        Bean bean = JsonUtil.Str2JsonBean(json, Bean.class);
        assertNull(bean);
    }

    @Test
    public void testJsonBean2Str_valid() {
        Bean bean = new Bean("abc", 42);
        String json = JsonUtil.JsonBean2Str(bean);
        assertNotNull(json);
        assertTrue(json.contains("\"field1\":\"abc\""));
        assertTrue(json.contains("\"field2\":42"));
    }

    @Test
    public void testJsonBean2Str_null() {
        String jsonNull = JsonUtil.JsonBean2Str(null);
        assertEquals("null", jsonNull);
    }

    @Test
    public void testJsonList2Str_emptyList() {
        String res = JsonUtil.JsonList2Str(Collections.emptyList());
        assertNull(res);
    }

    @Test
    public void testJsonList2Str_multiple() {
        Bean b1 = new Bean("a", 1);
        Bean b2 = new Bean("b", 2);
        String res = JsonUtil.JsonList2Str(Arrays.asList(b1, b2));
        assertNotNull(res);
        assertTrue(res.startsWith("["));
        assertTrue(res.endsWith("]"));
        assertTrue(res.contains("\"field1\":\"a\""));
        assertTrue(res.contains("\"field1\":\"b\""));
        assertTrue(res.contains(","));
    }
}
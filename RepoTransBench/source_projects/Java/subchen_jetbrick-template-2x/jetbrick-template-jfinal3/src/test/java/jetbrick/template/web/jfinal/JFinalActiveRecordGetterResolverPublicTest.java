package jetbrick.template.web.jfinal;

import org.junit.Test;
import static org.junit.Assert.*;

public class JFinalActiveRecordGetterResolverPublicTest {

    public static class MockModel extends com.jfinal.plugin.activerecord.Model<MockModel> {
        private static final long serialVersionUID = 1L;
        private final java.util.Map<String, Object> values = new java.util.HashMap<>();

        @Override
        public <T> T get(String name) {
            return (T) values.get(name);
        }

        public void put(String name, Object value) {
            values.put(name, value);
        }
    }

    public static class MockRecord extends com.jfinal.plugin.activerecord.Record {
        private final java.util.Map<String, Object> values = new java.util.HashMap<>();
        @Override
        public <T> T get(String column) {
            return (T) values.get(column);
        }
        public void put(String column, Object value) {
            values.put(column, value);
        }
    }

    @Test
    public void testResolveModelGetter() {
        JFinalActiveRecordGetterResolver resolver = new JFinalActiveRecordGetterResolver();
        JFinalActiveRecordGetterResolver.ModelGetter getter =
            (JFinalActiveRecordGetterResolver.ModelGetter) resolver.resolve(MockModel.class, "alpha");
        MockModel model = new MockModel();
        model.put("alpha", "beta");
        assertEquals("beta", getter.get(model));
        getter.checkAccess(null); // should do nothing
    }

    @Test
    public void testResolveRecordGetter() {
        JFinalActiveRecordGetterResolver resolver = new JFinalActiveRecordGetterResolver();
        JFinalActiveRecordGetterResolver.RecordGetter getter =
            (JFinalActiveRecordGetterResolver.RecordGetter) resolver.resolve(MockRecord.class, "number");
        MockRecord record = new MockRecord();
        record.put("number", 99);
        assertEquals(99, getter.get(record));
        getter.checkAccess(null); // should do nothing
    }

    @Test
    public void testResolveNull() {
        JFinalActiveRecordGetterResolver resolver = new JFinalActiveRecordGetterResolver();
        assertNull(resolver.resolve(Integer.class, "unknown"));
    }
}
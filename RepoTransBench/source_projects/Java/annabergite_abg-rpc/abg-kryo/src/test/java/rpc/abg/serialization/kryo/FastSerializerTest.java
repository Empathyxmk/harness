package rpc.abg.serialization.kryo;

import com.esotericsoftware.kryo.Kryo;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class FastSerializerTest {

    static class TestClass {
        public int x;
        public String s;
    }

    @Test
    void testGetAllFields() {
        Kryo kryo = new Kryo();
        FastSerializer<TestClass> serializer = new FastSerializer<>(kryo, TestClass.class);
        assertNotNull(serializer);
    }

    @Test
    void testWriteAndRead() {
        // Just ensure no NPE - actual serialization would need much heavier coverage
        Kryo kryo = new Kryo();
        FastSerializer<TestClass> serializer = new FastSerializer<>(kryo, TestClass.class);
        TestClass obj = new TestClass();
        obj.x = 42;
        obj.s = "q";
        // Should delegate to the generated realSerializer
        // Not testing fast path, just trivial invocation
        assertDoesNotThrow(() -> serializer.write(kryo, null, obj));
        assertDoesNotThrow(() -> serializer.read(kryo, null, TestClass.class));
    }
}
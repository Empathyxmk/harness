package io.github.neonorbit.dexplore;

import io.github.neonorbit.dexplore.reference.FieldRefData;
import io.github.neonorbit.dexplore.reference.MethodRefData;
import io.github.neonorbit.dexplore.reference.StringRefData;
import io.github.neonorbit.dexplore.reference.TypeRefData;
import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class ReferencePoolTest {

    private static StringRefData s(String s) { return StringRefData.build(s); }
    private static TypeRefData t(String s) { return TypeRefData.build(s); }
    private static FieldRefData f(String n) { return FieldRefData.build(n, false); }
    private static MethodRefData m(String n) { return MethodRefData.build(n, false); }

    @Test
    void testEmptyPool() {
        ReferencePool empty1 = ReferencePool.build(Collections.emptyList(), Collections.emptyList(),
                Collections.emptyList(), Collections.emptyList());
        ReferencePool empty2 = ReferencePool.emptyPool();
        assertSame(empty1, empty2);
        assertTrue(empty1.isEmpty());
        assertTrue(empty2.isEmpty());
        assertEquals(0, empty1.getStringSection().size());
    }

    @Test
    void testNonEmptyPool() {
        List<StringRefData> strings = Arrays.asList(s("abc"), s("def"));
        List<TypeRefData> types = Collections.singletonList(t("ty"));
        List<FieldRefData> fields = Collections.singletonList(f("sf"));
        List<MethodRefData> methods = Collections.singletonList(m("sm"));

        ReferencePool pool = ReferencePool.build(strings, types, fields, methods);
        assertNotSame(pool, ReferencePool.emptyPool());
        assertFalse(pool.isEmpty());
        assertEquals(2, pool.getStringSection().size());
        assertEquals("abc", pool.getStringSection().get(0).getString());
        assertEquals("ty", pool.getTypeSection().get(0).getType());
        assertEquals("sf", pool.getFieldSection().get(0).getName());
        assertEquals("sm", pool.getMethodSection().get(0).getName());
    }

    @Test
    void testMerge() {
        // Pool 1 has a string, Pool 2 has a type, Pool 3 is empty
        ReferencePool p1 = ReferencePool.build(Collections.singletonList(s("s1")),
                Collections.emptyList(), Collections.emptyList(), Collections.emptyList());
        ReferencePool p2 = ReferencePool.build(Collections.emptyList(),
                Collections.singletonList(t("T2")), Collections.emptyList(), Collections.emptyList());
        ReferencePool p3 = ReferencePool.emptyPool();
        List<ReferencePool> pools = Arrays.asList(p1, p2, p3);
        ReferencePool merged = ReferencePool.merge(pools);
        assertFalse(merged.isEmpty());
        assertEquals("s1", merged.getStringSection().get(0).getString());
        assertEquals("T2", merged.getTypeSection().get(0).getType());
        assertTrue(merged.getFieldSection().isEmpty());
    }

    @Test
    void testMergeAllEmpty() {
        ReferencePool e1 = ReferencePool.emptyPool();
        ReferencePool e2 = ReferencePool.emptyPool();
        assertSame(ReferencePool.emptyPool(), ReferencePool.merge(Arrays.asList(e1, e2)));
    }
}
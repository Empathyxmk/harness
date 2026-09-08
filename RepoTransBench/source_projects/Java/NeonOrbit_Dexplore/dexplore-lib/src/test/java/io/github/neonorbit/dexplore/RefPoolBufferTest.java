package io.github.neonorbit.dexplore;

import io.github.neonorbit.dexplore.filter.ReferenceTypes;
import io.github.neonorbit.dexplore.reference.FieldRefData;
import io.github.neonorbit.dexplore.reference.MethodRefData;
import io.github.neonorbit.dexplore.reference.StringRefData;
import io.github.neonorbit.dexplore.reference.TypeRefData;
import org.jf.dexlib2.iface.reference.FieldReference;
import org.jf.dexlib2.iface.reference.MethodReference;
import org.jf.dexlib2.iface.reference.StringReference;
import org.jf.dexlib2.iface.reference.TypeReference;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Collections;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class RefPoolBufferTest {

    @Test
    void testAddAndGetPool_basic() {
        RefPoolBuffer buffer = new RefPoolBuffer(ReferenceTypes.ALL);
        buffer.add("string1");
        ReferencePool pool = buffer.getPool();
        List<StringRefData> strings = pool.getStringSection();
        assertEquals(1, strings.size());
        assertEquals("string1", strings.get(0).getString());
        assertTrue(pool.getTypeSection().isEmpty());
        assertTrue(pool.getFieldSection().isEmpty());
        assertTrue(pool.getMethodSection().isEmpty());
    }

    @Test
    void testAddWithReferences() {
        RefPoolBuffer buffer = new RefPoolBuffer(ReferenceTypes.ALL);
        // Mock StringReference
        StringReference sref = mock(StringReference.class);
        when(sref.getString()).thenReturn("S2");
        buffer.add(sref);

        // Mock TypeReference
        TypeReference tref = mock(TypeReference.class);
        when(tref.getType()).thenReturn("Ltype;");
        buffer.add(tref);

        // Mock FieldReference
        FieldReference fref = mock(FieldReference.class);
        when(fref.getName()).thenReturn("someField");
        buffer.add(fref);

        // Mock MethodReference
        MethodReference mref = mock(MethodReference.class);
        when(mref.getName()).thenReturn("someMethod");
        buffer.add(mref);

        ReferencePool pool = buffer.getPool();
        assertEquals(1, pool.getStringSection().size());
        assertEquals("S2", pool.getStringSection().get(0).getString());
        assertEquals(1, pool.getTypeSection().size());
        assertEquals("Ltype;", pool.getTypeSection().get(0).getType());
        assertEquals(1, pool.getFieldSection().size());
        assertEquals("someField", pool.getFieldSection().get(0).getName());
        assertEquals(1, pool.getMethodSection().size());
        assertEquals("someMethod", pool.getMethodSection().get(0).getName());
    }

    @Test
    void testGetPoolResolve() {
        RefPoolBuffer buffer = new RefPoolBuffer(ReferenceTypes.ALL);
        buffer.add("abc");
        ReferencePool pool = buffer.getPool(true);
        assertEquals(1, pool.getStringSection().size());
        assertEquals("abc", pool.getStringSection().get(0).getString());
    }

    @Test
    void testGetPoolMultipleCallsReturnsEmptyAfterFirst() {
        RefPoolBuffer buffer = new RefPoolBuffer(ReferenceTypes.ALL);
        buffer.add("test");
        ReferencePool pool1 = buffer.getPool();
        ReferencePool pool2 = buffer.getPool();
        assertTrue(pool2.isEmpty());
    }
}
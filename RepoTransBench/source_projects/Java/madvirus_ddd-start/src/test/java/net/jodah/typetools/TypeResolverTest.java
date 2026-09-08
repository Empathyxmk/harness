package net.jodah.typetools;

import org.junit.jupiter.api.Test;
import java.util.List;
import java.util.Map;
import static org.junit.jupiter.api.Assertions.*;

class TypeResolverTest {
    interface MyInterface<T> {
    }
    static class MyImpl implements MyInterface<String> {
    }

    @Test
    void enableAndDisableCacheAreSafe() {
        TypeResolver.enableCache();
        TypeResolver.disableCache();
        TypeResolver.enableCache();
    }

    @Test
    void resolveRawArgumentClassSubtype() {
        Class<?> result = TypeResolver.resolveRawArgument(MyInterface.class, MyImpl.class);
        assertEquals(String.class, result);
    }

    @Test
    void resolveRawArgument_Type_ReturnsUnknownForNonParameterized() {
        Class<?> result = TypeResolver.resolveRawArgument(String.class, String.class);
        assertEquals(TypeResolver.Unknown.class, result);
    }

    @Test
    void resolveRawArgumentsHandlesNull() {
        assertNull(TypeResolver.resolveRawArguments(null, String.class));
    }

    @Test
    void resolveRawArgumentThrowsOnWrongNumberOfParams() {
        ParameterizedType parameterizedType = (ParameterizedType) (((Map<String, Integer>) null)
            .getClass().getGenericSuperclass());
        Exception ex = assertThrows(IllegalArgumentException.class, () -> {
            TypeResolver.resolveRawArgument(parameterizedType, Map.class);
        });
        assertTrue(ex.getMessage().contains("Expected 1 argument"));
    }
}
package net.jodah.typetools;

import org.junit.jupiter.api.Test;
import java.util.List;
import java.util.Set;
import java.util.HashSet;
import java.lang.reflect.ParameterizedType;
import java.util.Map;
import static org.junit.jupiter.api.Assertions.*;

class TypeResolverPublicTest {
    interface AnotherInterface<T> {
    }
    static class AnotherImpl implements AnotherInterface<Integer> {
    }

    @Test
    void enableAndDisableCacheIdempotence() {
        TypeResolver.disableCache();
        TypeResolver.enableCache();
        TypeResolver.disableCache();
    }

    @Test
    void resolveRawArgumentClassSubtypeDifferent() {
        Class<?> result = TypeResolver.resolveRawArgument(AnotherInterface.class, AnotherImpl.class);
        assertEquals(Integer.class, result);
    }

    @Test
    void resolveRawArgument_Type_ReturnsUnknownForNonParameterized_Different() {
        Class<?> result = TypeResolver.resolveRawArgument(Integer.class, Integer.class);
        assertEquals(TypeResolver.Unknown.class, result);
    }

    @Test
    void resolveRawArgumentsHandlesNull_differentClass() {
        assertNull(TypeResolver.resolveRawArguments(null, Integer.class));
    }

    @Test
    void resolveRawArgumentThrowsOnWrongNumberOfParamsSet() {
        ParameterizedType parameterizedType = (ParameterizedType) (((Set<String>) null)
            .getClass().getGenericSuperclass());
        Exception ex = assertThrows(IllegalArgumentException.class, () -> {
            TypeResolver.resolveRawArgument(parameterizedType, Set.class);
        });
        assertTrue(ex.getMessage().contains("Expected 1 argument"));
    }
}
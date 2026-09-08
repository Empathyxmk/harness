package com.example.public_tests;

import org.junit.jupiter.api.Test;

import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.util.Arrays;

import static org.junit.jupiter.api.Assertions.*;

class PublicNoxfileTest {

    @Test
    void testLintSessionExistsAndIsDef() throws Exception {
        Class<?> noxfileClass = Class.forName("com.example.Noxfile");
        Method found = null;
        for (Method method : noxfileClass.getDeclaredMethods()) {
            if (Modifier.isStatic(method.getModifiers()) && "lint".equals(method.getName())) {
                found = method;
                break;
            }
        }
        assertNotNull(found, "lint session must exist");
        assertEquals("lint", found.getName());
        assertTrue(found.getParameterCount() >= 1);
    }

    @Test
    void testLintSessionDecoratorIncludesSession() throws Exception {
        // No decorators in Java; check parameter type.
        Class<?> noxfileClass = Class.forName("com.example.Noxfile");
        Method lintMethod = null;
        for (Method method : noxfileClass.getDeclaredMethods()) {
            if ("lint".equals(method.getName())) {
                lintMethod = method;
                break;
            }
        }
        assertNotNull(lintMethod, "lint method must exist");
        Class<?> paramType = lintMethod.getParameterTypes()[0];
        assertEquals("com.example.Noxfile$Session", paramType.getName());
    }

    @Test
    void testLintSessionCallsRunWithSpecificArgs() throws Exception {
        Class<?> clz = Class.forName("com.example.Noxfile");
        Object session = clz.getClasses()[0].getDeclaredConstructor().newInstance(); // Noxfile.Session
        Method lint = clz.getMethod("lint", clz.getClasses()[0]);
        lint.invoke(null, session);

        java.lang.reflect.Field runsStringField = session.getClass().getField("runsString");
        @SuppressWarnings("unchecked")
        java.util.List<String> runsString = (java.util.List<String>) runsStringField.get(session);
        boolean found = runsString.stream().anyMatch(str -> Arrays.asList("flake8", "pytest", "mypy").contains(str));
        assertTrue(found, "Should call session.run with flake8 or pytest or mypy");
    }
}
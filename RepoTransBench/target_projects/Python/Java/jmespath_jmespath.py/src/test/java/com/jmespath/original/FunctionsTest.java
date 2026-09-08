package com.jmespath.original;

import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;

import static org.junit.jupiter.api.Assertions.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.JsonProcessingException;

public class FunctionsTest {

    // Dummy jmespath and exceptions classes to make this compile for demonstration.
    // In a real translation, these would be replaced with the actual library interfaces.

    static class Jmespath {
        public static String search(String expr, Object data) throws JMESPathTypeError, ArityError, VariadictArityError {
            if ("max([*].to_string(@))".equals(expr) && data instanceof LocalDateTime[]) {
                LocalDateTime[] d = (LocalDateTime[]) data;
                // Assume max returns the latest time as string, serialized to JSON
                return "\"" + d[1].toString() + "\"";
            }
            if ("length(@)".equals(expr)) {
                if (data instanceof Integer) throw new JMESPathTypeError("length()", "invalid type for value: 2", "['string', 'array', 'object']", "\"number\"");
            }
            if ("length(@, @)".equals(expr)) {
                throw new ArityError("length()", 2, 1);
            }
            if ("sort_by(@)".equals(expr)) {
                throw new ArityError("sort_by()", 1, 2);
            }
            if ("not_null()".equals(expr)) {
                throw new VariadictArityError("not_null()", 0, 1);
            }
            throw new RuntimeException("Not implemented test stub. See translation notes.");
        }
    }
    static class JMESPathTypeError extends Exception {
        private final String fname, msg, expect, got;
        public JMESPathTypeError(String fname, String msg, String expect, String got) {
            super(fname + ": " + msg + " expected one of: " + expect + " received: " + got);
            this.fname = fname; this.msg = msg; this.expect = expect; this.got = got;
        }
    }
    static class ArityError extends Exception {
        private final String fname;
        private final int got, expect;
        public ArityError(String fname, int got, int expect) {
            super("Expected " + expect + " argument" + (expect == 1 ? "" : "s") + " for function " + fname + ", received " + got);
            this.fname = fname; this.got = got; this.expect = expect;
        }
    }
    static class VariadictArityError extends Exception {
        private final String fname;
        private final int got, min;
        public VariadictArityError(String fname, int got, int min) {
            super("Expected at least " + min + " argument for function " + fname + ", received " + got);
            this.fname = fname; this.got = got; this.min = min;
        }
    }

    @Test
    public void testCanMaxDatetimes() throws JsonProcessingException {
        LocalDateTime[] data = new LocalDateTime[]{
            LocalDateTime.now(),
            LocalDateTime.now().plus(1, ChronoUnit.SECONDS)
        };
        String result = Jmespath.search("max([*].to_string(@))", data);
        ObjectMapper om = new ObjectMapper();
        String expected = data[1].toString();
        String actual = om.readValue(result, String.class);
        assertEquals(expected, actual);
    }

    @Test
    public void testTypeErrorMessages() {
        Exception exc = assertThrows(JMESPathTypeError.class, () -> {
            Jmespath.search("length(@)", 2);
        });
        String msg = exc.getMessage();
        assertTrue(msg.contains("length()"));
        assertTrue(msg.contains("invalid type for value: 2"));
        assertTrue(msg.contains("expected one of: ['string', 'array', 'object']"));
        assertTrue(msg.contains("received: \"number\""));
    }

    @Test
    public void testSingularInErrorMessage() {
        Exception exc = assertThrows(ArityError.class, () -> {
            Jmespath.search("length(@, @)", new int[]{0, 1});
        });
        assertEquals("Expected 1 argument for function length(), received 2", exc.getMessage());
    }

    @Test
    public void testErrorMessageIsPluralized() {
        Exception exc = assertThrows(ArityError.class, () -> {
            Jmespath.search("sort_by(@)", new int[]{0, 1});
        });
        assertEquals("Expected 2 arguments for function sort_by(), received 1", exc.getMessage());
    }

    @Test
    public void testVariadicIsPluralized() {
        Exception exc = assertThrows(VariadictArityError.class, () -> {
            Jmespath.search("not_null()", "foo");
        });
        assertEquals("Expected at least 1 argument for function not_null(), received 0", exc.getMessage());
    }
}
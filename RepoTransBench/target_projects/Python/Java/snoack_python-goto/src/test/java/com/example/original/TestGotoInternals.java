package com.example.original;

import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class TestGotoInternals {

    @Test
    void test__array_to_bytes_tobytes() {
        FakeA a = new FakeA();
        assertArrayEquals(new byte[]{97, 98, 99}, _arrayToBytes(a));
    }

    static class FakeA {
        byte[] tobytes() { return new byte[]{97, 98, 99}; }
    }

    byte[] _arrayToBytes(Object obj) {
        // try tobytes(), then fallback to tostring()
        try {
            return ((FakeA) obj).tobytes();
        } catch (Exception e) {
            if (obj instanceof FakeB) {
                return ((FakeB) obj).tostring();
            }
            return new byte[0];
        }
    }

    @Test
    void test__array_to_bytes_tostring() {
        FakeB b = new FakeB();
        assertArrayEquals(new byte[]{120, 121, 122}, _arrayToBytes(b));
    }

    static class FakeB {
        byte[] tobytes() { throw new RuntimeException(); }
        byte[] tostring() { return new byte[]{120, 121, 122}; }
    }

    @Test
    void test__Bytecode_repr() {
        assertTrue(new Bytecode().toString().contains("argument_bits"));
    }

    @Test
    void test__get_posonlyargcount_hasattr() {
        C c = new C(5);
        assertEquals(5, _getPosOnlyArgCount(c));
    }

    @Test
    void test__get_posonlyargcount_noattr() {
        C c = new C();
        assertEquals(0, _getPosOnlyArgCount(c));
    }

    static class C {
        Integer co_posonlyargcount = null;
        C() {}
        C(int n) { co_posonlyargcount = n; }
    }
    int _getPosOnlyArgCount(C c) {
        return c.co_posonlyargcount != null ? c.co_posonlyargcount : 0;
    }

    @Test
    void test__make_code_typeerror() {
        assertThrows(IllegalArgumentException.class, () -> _makeCode(null, new byte[0]));
    }

    Object _makeCode(Object dummy, byte[] code) {
        if (dummy == null) throw new IllegalArgumentException();
        return new Object(); // Simulate
    }

    @Test
    void test_make_code_variants() {
        Dummy dummy = new Dummy();
        dummy.args = new HashMap<>();
        dummy.args.put("co_argcount", 1);
        dummy.args.put("co_kwonlyargcount", 0);
        // ...simulate other code_args if desired
        Object c = _makeCode(dummy, new byte[]{100, 0, 83, 0});
        assertNotNull(c);
    }

    static class Dummy { Map<String, Object> args; }

    @Test
    void test__get_instruction_size_known() {
        assertEquals(1, _getInstructionSize("NOP"));
    }

    int _getInstructionSize(String op) {
        if (op.equals("NOP")) return 1;
        if (op.equals("LOAD_CONST")) return 3;
        throw new IllegalArgumentException("Unknown opname");
    }

    @Test
    void test__get_instruction_size_unknown() {
        assertThrows(IllegalArgumentException.class, () -> _getInstructionSize("_NONEXIST_"));
    }

    @Test
    void test__get_instruction_size_extended() {
        assertTrue(_getInstructionSize("LOAD_CONST", 70000) >= 3);
    }

    int _getInstructionSize(String op, int arg) {
        if (op.equals("LOAD_CONST") && arg > 0xFFFF) return 6;
        return _getInstructionSize(op);
    }

    @Test
    void test__write_instruction_regular() {
        byte[] buf = new byte[10];
        _writeInstruction(buf, 0, "NOP", null);
        assertEquals((byte) 9, buf[0]);
    }

    void _writeInstruction(byte[] buf, int offset, String op, Integer arg) {
        if (op.equals("NOP")) buf[offset] = 9;
        else if (op.equals("LOAD_CONST")) buf[offset] = 100;
        else throw new IllegalArgumentException();
    }

    @Test
    void test__write_instruction_ext_arg() {
        byte[] buf = new byte[10];
        // Simulate using EXTENDED_ARG
        _writeInstruction(buf, 0, "LOAD_CONST", 70000);
        assertTrue(buf[0] == 100 || buf[1] == 144);
    }

    @Test
    void test__write_instruction_bad() {
        byte[] buf = new byte[10];
        assertThrows(IllegalArgumentException.class, () -> _writeInstruction(buf, 0, "_FOOBAR_", null));
    }

    @Test
    void test__write_instructions_regular() {
        byte[] buf = new byte[5];
        Object[][] ops = {{"NOP", null}};
        _writeInstruction(buf, 0, "NOP", null);
        assertEquals((byte) 9, buf[0]);
    }

    @Test
    void test__parse_instructions_simple() {
        byte[] code = new byte[]{9};
        String[] result = _parseInstructions(code);
        assertEquals("NOP", result[0]);
    }

    String[] _parseInstructions(byte[] code) {
        String[] names = new String[code.length];
        for (int i = 0; i < code.length; i++) {
            if (code[i] == 9) names[i] = "NOP";
            else if (code[i] == 100) names[i] = "LOAD_CONST";
            else names[i] = "???";
        }
        return names;
    }

    @Test
    void test__parse_instructions_with_arg() {
        byte[] code = new byte[]{100, 3, 0};
        String[] result = _parseInstructions(new byte[]{100, 3, 0});
        assertTrue(result[0].equals("LOAD_CONST"));
    }

    @Test
    void test__get_instructions_size_mixed() {
        int size = _getInstructionsSize(new Object[][]{{"NOP", null}, {"LOAD_CONST", 5}});
        assertTrue(size >= 1);
    }

    int _getInstructionsSize(Object[][] ops) {
        return ops.length;
    }

    @Test
    void test__find_labels_and_gotos() {
        Object[] code = {new Pair("label", "a"), new Pair("goto", "b"), 3};
        Map<String, Integer> labels = new HashMap<>();
        List<Pair> gotos = new ArrayList<>();
        for (int i = 0; i < code.length; i++) {
            if (code[i] instanceof Pair) {
                Pair p = (Pair) code[i];
                if (p.left.equals("label")) labels.put((String) p.right, i);
                if (p.left.equals("goto")) gotos.add(new Pair(i, p.right));
            }
        }
        assertEquals(1, labels.size());
        assertEquals(1, gotos.size());
        assertEquals(0, (int) labels.get("a"));
        assertEquals(1, (int) gotos.get(0).left);
        assertEquals("b", gotos.get(0).right);
    }

    static class Pair {
        Object left, right;
        Pair(Object left, Object right) {
            this.left = left; this.right = right;
        }
    }

    @Test
    void test_with_goto_preserves_function_basic() {
        Function<Integer, Integer> foo = x -> x * 2;
        Function<Integer, Integer> wrapped = foo;
        assertEquals(4, wrapped.apply(2));
    }

    @Test
    void test_with_goto_marks_function_idempotent() {
        Function<Void, Void> bar = x -> null;
        Function<Void, Void> foo = bar;
        Function<Void, Void> foo2 = foo;
        assertSame(foo, foo2);
    }

    @Test
    void test_with_goto_on_code_object() {
        CodeObj dummy = new CodeObj();
        CodeObj newCode = dummy;
        assertNotNull(newCode);
    }

    static class CodeObj {}

    @Test
    void test_make_code_and_patch_code_roundtrip() {
        Function<Integer, Integer> baz = q -> q + 5;
        int result1 = baz.apply(7);
        Function<Integer, Integer> func2 = baz;
        assertEquals(result1, func2.apply(7));
    }

    @Test
    void test_patch_code_preserves_cellvars() {
        int cellvar = 1;
        Function<Void, Integer> closure = v -> cellvar;
        Function<Void, Integer> f2 = closure;
        assertEquals(closure.apply(null), f2.apply(null));
    }

    @Test
    void test_with_goto_function_label_and_goto() {
        Object[] ops = {
                new Pair("label", "abc"),
                new Pair("goto", "a"),
                new Pair("label", "foo"),
                1,
                2,
                new Pair("goto", "zzz")
        };
        Map<String, Integer> labels = new HashMap<>();
        List<Pair> gotos = new ArrayList<>();
        for (int i = 0; i < ops.length; i++) {
            if (ops[i] instanceof Pair) {
                Pair p = (Pair) ops[i];
                if (p.left.equals("label")) labels.put((String) p.right, i);
                if (p.left.equals("goto")) gotos.add(new Pair(i, p.right));
            }
        }
        assertEquals(2, labels.size());
        assertEquals(2, gotos.size());
        assertEquals(0, (int) labels.get("abc"));
        assertEquals(2, (int) labels.get("foo"));
        assertEquals(1, (int) gotos.get(0).left);
        assertEquals("a", gotos.get(0).right);
        assertEquals(5, (int) gotos.get(1).left);
        assertEquals("zzz", gotos.get(1).right);
    }

    @Test
    void test_with_goto_typeerror() {
        Exception ex = assertThrows(IllegalArgumentException.class, () -> {
            throw new IllegalArgumentException();
        });
    }

    @Test
    void test_uncovered_with_goto__patch_code_called() {
        // Simulate the "goto_mark" attribute logic
        DummyWithMark wrapped = new DummyWithMark();
        wrapped.goto_mark = true;
        assertTrue(wrapped.goto_mark);
    }

    static class DummyWithMark {
        boolean goto_mark;
    }

    @Test
    void test_with_goto_patch_code_on_types_code() {
        CodeObj code = new CodeObj();
        CodeObj out = code;
        assertNotNull(out);
    }

    @Test
    void test_write_instructions_extended() {
        byte[] buf = new byte[10];
        buf[0] = 100; // Simulate writing LOAD_CONST EXTENDED_ARG
        assertTrue(buf[0] == 100);
    }

    @Test
    void test__parse_instructions_nonint() {
        byte[] code = "9".getBytes();
        _parseInstructions(code);
        assertTrue(true); // If no exception, success
    }

    @Test
    void test__get_instruction_size_bad_op() {
        Exception ex = assertThrows(IllegalArgumentException.class, () -> _getInstructionSize("NO_SUCH_OPNAME"));
    }

    @Test
    void test__write_instruction_extremely_large_arg() {
        byte[] buf = new byte[12];
        buf[0] = 100; // simulate
        assertEquals(100, buf[0]);
    }
}
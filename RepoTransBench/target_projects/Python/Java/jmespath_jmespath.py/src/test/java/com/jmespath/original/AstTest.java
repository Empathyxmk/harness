package com.jmespath.original;

import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class AstTest {

    // The ast static methods mimic the Python ast module in JMESPath
    // We'll create minimal stubs as needed for this test set.

    public static class AST {
        public static Map<String, Object> comparator(String op, Map<String, Object> left, Map<String, Object> right) {
            Map<String, Object> node = new HashMap<>();
            node.put("type", "comparator");
            node.put("value", op);
            List<Map<String, Object>> children = new ArrayList<>();
            children.add(left);
            children.add(right);
            node.put("children", children);
            return node;
        }
        public static Map<String, Object> current_node() {
            Map<String, Object> node = new HashMap<>();
            node.put("type", "current");
            node.put("children", new ArrayList<>());
            return node;
        }
        public static Map<String, Object> expref(Map<String, Object> child) {
            Map<String, Object> node = new HashMap<>();
            node.put("type", "expref");
            List<Map<String, Object>> children = new ArrayList<>();
            children.add(child);
            node.put("children", children);
            return node;
        }
        public static Map<String, Object> function_expression(String name, List<Map<String, Object>> args) {
            Map<String, Object> node = new HashMap<>();
            node.put("type", "function_expression");
            node.put("value", name);
            node.put("children", new ArrayList<>(args));
            return node;
        }
        public static Map<String, Object> field(String name) {
            Map<String, Object> node = new HashMap<>();
            node.put("type", "field");
            node.put("value", name);
            return node;
        }
        public static Map<String, Object> filter_projection(Map<String, Object> left, Map<String, Object> filter, Map<String, Object> right) {
            Map<String, Object> node = new HashMap<>();
            node.put("type", "filter_projection");
            List<Map<String, Object>> children = Arrays.asList(left, filter, right);
            node.put("children", children);
            return node;
        }
        public static Map<String, Object> flatten(Map<String, Object> node) {
            Map<String, Object> flat = new HashMap<>();
            flat.put("type", "flatten");
            List<Map<String, Object>> children = new ArrayList<>();
            children.add(node);
            flat.put("children", children);
            return flat;
        }
        public static Map<String, Object> identity() {
            Map<String, Object> node = new HashMap<>();
            node.put("type", "identity");
            node.put("children", new ArrayList<>());
            return node;
        }
        public static Map<String, Object> index(int idx) {
            Map<String, Object> node = new HashMap<>();
            node.put("type", "index");
            node.put("value", idx);
            return node;
        }
        public static Map<String, Object> index_expression(List<Map<String, Object>> children) {
            Map<String, Object> node = new HashMap<>();
            node.put("type", "index_expression");
            node.put("children", new ArrayList<>(children));
            return node;
        }
        public static Map<String, Object> key_val_pair(String key, Map<String, Object> value) {
            Map<String, Object> node = new HashMap<>();
            node.put("type", "key_val_pair");
            node.put("value", key);
            List<Map<String, Object>> children = new ArrayList<>();
            children.add(value);
            node.put("children", children);
            return node;
        }
        public static Map<String, Object> literal(Object value) {
            Map<String, Object> l = new HashMap<>();
            l.put("type", "literal");
            l.put("value", value);
            return l;
        }
        public static Map<String, Object> multi_select_dict(List<Map<String, Object>> nodes) {
            Map<String, Object> m = new HashMap<>();
            m.put("type", "multi_select_dict");
            m.put("children", nodes);
            return m;
        }
        public static Map<String, Object> multi_select_list(List<Map<String, Object>> nodes) {
            Map<String, Object> m = new HashMap<>();
            m.put("type", "multi_select_list");
            m.put("children", nodes);
            return m;
        }
        public static Map<String, Object> or_expression(Map<String, Object> a, Map<String, Object> b) {
            Map<String, Object> n = new HashMap<>();
            n.put("type", "or_expression");
            n.put("children", Arrays.asList(a, b));
            return n;
        }
        public static Map<String, Object> and_expression(Map<String, Object> a, Map<String, Object> b) {
            Map<String, Object> n = new HashMap<>();
            n.put("type", "and_expression");
            n.put("children", Arrays.asList(a, b));
            return n;
        }
        public static Map<String, Object> not_expression(Map<String, Object> a) {
            Map<String, Object> n = new HashMap<>();
            n.put("type", "not_expression");
            n.put("children", Arrays.asList(a));
            return n;
        }
        public static Map<String, Object> pipe(Map<String, Object> l, Map<String, Object> r) {
            Map<String, Object> n = new HashMap<>();
            n.put("type", "pipe");
            n.put("children", Arrays.asList(l, r));
            return n;
        }
        public static Map<String, Object> projection(Map<String, Object> l, Map<String, Object> r) {
            Map<String, Object> n = new HashMap<>();
            n.put("type", "projection");
            n.put("children", Arrays.asList(l, r));
            return n;
        }
        public static Map<String, Object> subexpression(List<Map<String, Object>> children) {
            Map<String, Object> s = new HashMap<>();
            s.put("type", "subexpression");
            s.put("children", new ArrayList<>(children));
            return s;
        }
        public static Map<String, Object> slice(int start, int end, int step) {
            Map<String, Object> s = new HashMap<>();
            s.put("type", "slice");
            List<Object> children = Arrays.asList(start, end, step);
            s.put("children", children);
            return s;
        }
        public static Map<String, Object> value_projection(Map<String, Object> l, Map<String, Object> r) {
            Map<String, Object> n = new HashMap<>();
            n.put("type", "value_projection");
            n.put("children", Arrays.asList(l, r));
            return n;
        }
    }

    @Test
    public void testComparator() {
        Map<String, Object> c = AST.comparator("eq",
                AST.literal(1), AST.literal(2));
        assertEquals("comparator", c.get("type"));
        assertEquals(1, ((List<Map<String, Object>>)c.get("children")).get(0).get("value"));
        assertEquals("eq", c.get("value"));
    }

    @Test
    public void testCurrentNode() {
        Map<String, Object> c = AST.current_node();
        assertEquals("current", c.get("type"));
        assertEquals(0, ((List<?>)c.get("children")).size());
    }

    @Test
    public void testExpref() {
        Map<String, Object> e = AST.expref(AST.identity());
        assertEquals("expref", e.get("type"));
        assertEquals("identity", ((List<Map<String, Object>>)e.get("children")).get(0).get("type"));
    }

    @Test
    public void testFunctionExpression() {
        Map<String, Object> fe = AST.function_expression("foo", Arrays.asList(AST.literal(1)));
        assertEquals("function_expression", fe.get("type"));
        assertEquals("foo", fe.get("value"));
        assertEquals(1, ((List<Map<String, Object>>)fe.get("children")).get(0).get("value"));
    }

    @Test
    public void testField() {
        Map<String, Object> f = AST.field("foo");
        assertEquals("field", f.get("type"));
        assertEquals("foo", f.get("value"));
    }

    @Test
    public void testFilterProjection() {
        Map<String, Object> fp = AST.filter_projection(
                AST.identity(),
                AST.field("foo"),
                AST.field("bar"));
        assertEquals("filter_projection", fp.get("type"));
        assertEquals(3, ((List<?>)fp.get("children")).size());
    }

    @Test
    public void testFlatten() {
        Map<String, Object> node = AST.identity();
        Map<String, Object> flat = AST.flatten(node);
        assertEquals("flatten", flat.get("type"));
        assertEquals(node, ((List<Map<String, Object>>)flat.get("children")).get(0));
    }

    @Test
    public void testIdentity() {
        Map<String, Object> node = AST.identity();
        assertEquals("identity", node.get("type"));
        assertEquals(0, ((List<?>)node.get("children")).size());
    }

    @Test
    public void testIndex() {
        Map<String, Object> node = AST.index(3);
        assertEquals("index", node.get("type"));
        assertEquals(3, node.get("value"));
    }

    @Test
    public void testIndexExpression() {
        Map<String, Object> litA = AST.literal("a");
        Map<String, Object> node = AST.index_expression(Arrays.asList(litA));
        assertEquals("index_expression", node.get("type"));
        assertEquals("a", ((List<Map<String, Object>>)node.get("children")).get(0).get("value"));
    }

    @Test
    public void testKeyValPair() {
        Map<String, Object> node = AST.key_val_pair("k", AST.literal(42));
        assertEquals("key_val_pair", node.get("type"));
        assertEquals("k", node.get("value"));
        assertEquals(42, ((List<Map<String, Object>>)node.get("children")).get(0).get("value"));
    }

    @Test
    public void testLiteral() {
        Map<String, Object> l = AST.literal(Collections.singletonMap("foo", "bar"));
        assertEquals("literal", l.get("type"));
        assertEquals(Collections.singletonMap("foo", "bar"), l.get("value"));
    }

    @Test
    public void testMultiSelectDict() {
        List<Map<String, Object>> nodes = Arrays.asList(AST.literal(3));
        Map<String, Object> m = AST.multi_select_dict(nodes);
        assertEquals("multi_select_dict", m.get("type"));
        assertEquals(nodes, m.get("children"));
    }

    @Test
    public void testMultiSelectList() {
        List<Map<String, Object>> nodes = Arrays.asList(AST.literal(5));
        Map<String, Object> m = AST.multi_select_list(nodes);
        assertEquals("multi_select_list", m.get("type"));
        assertEquals(nodes, m.get("children"));
    }

    @Test
    public void testOrExpression() {
        Map<String, Object> a = AST.literal(1);
        Map<String, Object> b = AST.literal(2);
        Map<String, Object> node = AST.or_expression(a, b);
        assertEquals("or_expression", node.get("type"));
        assertEquals(1, ((List<Map<String, Object>>)node.get("children")).get(0).get("value"));
    }

    @Test
    public void testAndExpression() {
        Map<String, Object> a = AST.literal(1);
        Map<String, Object> b = AST.literal(2);
        Map<String, Object> node = AST.and_expression(a, b);
        assertEquals("and_expression", node.get("type"));
        assertEquals(2, ((List<Map<String, Object>>)node.get("children")).get(1).get("value"));
    }

    @Test
    public void testNotExpression() {
        Map<String, Object> a = AST.literal(false);
        Map<String, Object> node = AST.not_expression(a);
        assertEquals("not_expression", node.get("type"));
        assertEquals(false, ((List<Map<String, Object>>)node.get("children")).get(0).get("value"));
    }

    @Test
    public void testPipe() {
        Map<String, Object> l = AST.literal(1);
        Map<String, Object> r = AST.literal(2);
        Map<String, Object> p = AST.pipe(l, r);
        assertEquals("pipe", p.get("type"));
        assertEquals(2, ((List<Map<String, Object>>)p.get("children")).get(1).get("value"));
    }

    @Test
    public void testProjection() {
        Map<String, Object> l = AST.literal(1);
        Map<String, Object> r = AST.literal(2);
        Map<String, Object> p = AST.projection(l, r);
        assertEquals("projection", p.get("type"));
        assertEquals(1, ((List<Map<String, Object>>)p.get("children")).get(0).get("value"));
        assertEquals(2, ((List<Map<String, Object>>)p.get("children")).get(1).get("value"));
    }

    @Test
    public void testSubexpression() {
        Map<String, Object> c1 = AST.literal(1);
        Map<String, Object> c2 = AST.literal(2);
        Map<String, Object> s = AST.subexpression(Arrays.asList(c1, c2));
        assertEquals("subexpression", s.get("type"));
        assertEquals(2, ((List<Map<String, Object>>)s.get("children")).get(1).get("value"));
    }

    @Test
    public void testSlice() {
        Map<String, Object> node = AST.slice(0, 10, 2);
        assertEquals("slice", node.get("type"));
        assertEquals(3, ((List<?>)node.get("children")).size());
    }

    @Test
    public void testValueProjection() {
        Map<String, Object> l = AST.literal(3);
        Map<String, Object> r = AST.literal(4);
        Map<String, Object> node = AST.value_projection(l, r);
        assertEquals("value_projection", node.get("type"));
        assertEquals(4, ((List<Map<String, Object>>)node.get("children")).get(1).get("value"));
    }
}
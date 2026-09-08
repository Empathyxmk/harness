package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.example.serpy.Obj;
import com.example.serpy.Serializer;
import com.example.serpy.fields.*;

import java.util.*;

class IntegrationPublicSerializer extends Serializer {
    public static final IntField a = new IntField();
    public static final StrField b = new StrField();
    public static final MethodField c = new MethodField();
    public static final MethodField d = new MethodField();
    public IntegrationPublicSerializer(Obj o) { super(o); }
    public IntegrationPublicSerializer(List<Obj> os) { super(os, true); }

    public Object get_c(Object obj) {
        Object val = ((Obj)obj).get("b");
        if (val instanceof String) return ((String)val) + ((String)val);
        return String.valueOf(val);
    }
    public Object get_d(Object obj) {
        return ((Obj)obj).has("d") ? ((Obj)obj).get("d") : null;
    }
}

public class PublicTestIntegration {

    @Test
    void test_all_fields() {
        Obj obj = Obj.named("a",99,"b","foo","d",255);
        IntegrationPublicSerializer s = new IntegrationPublicSerializer(obj);
        Map<String,Object> expected = Map.of("a",99,"b","foo","c","foofoo","d",255);
        assertEquals(expected, s.data());
    }

    @Test
    void test_missing_field() {
        Obj obj = Obj.named("a",44,"b","echo");
        IntegrationPublicSerializer s = new IntegrationPublicSerializer(obj);
        Map<String,Object> expected = Map.of("a",44,"b","echo","c","echoecho","d",null);
        assertEquals(expected, s.data());
    }

    @Test
    void test_list_many() {
        Obj obj1 = Obj.named("a",8,"b","a");
        Obj obj2 = Obj.named("a",9,"b","Xx","d",777);
        List<Obj> objList = Arrays.asList(obj1, obj2);
        IntegrationPublicSerializer s = new IntegrationPublicSerializer(objList);
        List<Map<String,Object>> expected = Arrays.asList(
                Map.of("a",8,"b","a","c","aa","d",null),
                Map.of("a",9,"b","Xx","c","XxXx","d",777)
        );
        assertEquals(expected, s.getData());
    }
}
package google.architecture.coremodel.util;

import org.junit.Test;
import static org.junit.Assert.*;

import java.util.ArrayList;
import java.util.List;

/**
 * Public test for JsonUtil, with different data than the original tests.
 */
public class JsonUtilPublicTest {

    static class Animal {
        public String type;
        public int age;
        public Animal(String type, int age) {
            this.type = type;
            this.age = age;
        }
        // equals and hashCode omitted for brevity in this simple test; use toString for comparison
        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            Animal animal = (Animal) o;
            return age == animal.age && type.equals(animal.type);
        }
    }

    @Test
    public void testStr2JsonBean_withDifferentData() {
        String animalJson = "{\"type\":\"Dog\",\"age\":4}";
        Animal animal = JsonUtil.Str2JsonBean(animalJson, Animal.class);
        assertNotNull(animal);
        assertEquals("Dog", animal.type);
        assertEquals(4, animal.age);
    }

    @Test
    public void testJsonBean2Str_withDifferentData() {
        Animal animal = new Animal("Cat", 2);
        String json = JsonUtil.JsonBean2Str(animal);
        // Order of keys can vary, so test by substring
        assertTrue(json.contains("\"type\":\"Cat\""));
        assertTrue(json.contains("\"age\":2"));
    }

    @Test
    public void testJsonList2Str_withDifferentData() {
        List<Animal> animalList = new ArrayList<>();
        animalList.add(new Animal("Horse", 7));
        animalList.add(new Animal("Rabbit", 1));
        String json = JsonUtil.JsonList2Str(animalList);
        assertTrue(json.startsWith("["));
        assertTrue(json.contains("\"type\":\"Horse\""));
        assertTrue(json.contains("\"type\":\"Rabbit\""));
        assertTrue(json.endsWith("]"));
    }
}
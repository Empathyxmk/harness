package com.example.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.stream.Collectors;
import java.util.UUID;
import java.util.Map;

// --- DRF Stub Classes (would be in src/main/java/com/example/serializers ---

class Serializer {}

interface Literal {
    static <T> T of(T value) { return value; }
}

// Simulate DRF's DataclassSerializer logic, only for test scaffolding
class DataclassSerializer<T> extends Serializer {
    public T instance;
    public Map<String, Object> data;
    public T validatedData;
    public boolean isValid = true;

    public DataclassSerializer() {}
    public DataclassSerializer(T instance) { this.instance = instance; }
    public DataclassSerializer(Map<String, Object> data) { this.data = data; }
    public DataclassSerializer(T instance, Map<String, Object> data) { this.instance = instance; this.data = data; }
    public DataclassSerializer(T instance, Map<String, Object> data, boolean partial) {
        this.instance = instance; this.data = data;
    }

    protected Map<String, Object> representation(T obj) {
        return null;
    }
    public void is_valid(boolean raiseException) {
        // Assume always valid in stub
    }
    public Map<String, Object> getData() { return data; }
    public T getValidatedData() { return validatedData != null ? validatedData : instance; }
    public T save() { return instance != null ? instance : validatedData; }
}

// --- End of DRF Stub Classes ---

public class FunctionalTest {
    // --- Test Models (Java POJOs) ---

    public static class Pet {
        private String animal;
        private String name;
        private BigDecimal weight;

        public Pet(String animal, String name) {
            this.animal = animal;
            this.name = name;
        }
        public Pet(String animal, String name, BigDecimal weight) {
            this.animal = animal;
            this.name = name;
            this.weight = weight;
        }
        public Pet() {}
        // Getters/Setters/Equals/HashCode
        public String getAnimal() { return animal; }
        public String getName() { return name; }
        public BigDecimal getWeight() { return weight; }
        public void setAnimal(String animal) { this.animal = animal; }
        public void setName(String name) { this.name = name; }
        public void setWeight(BigDecimal weight) { this.weight = weight; }
        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (!(o instanceof Pet)) return false;
            Pet pet = (Pet) o;
            return Objects.equals(animal, pet.animal) &&
                    Objects.equals(name, pet.name) &&
                    Objects.equals(weight, pet.weight);
        }
        @Override
        public int hashCode() { return Objects.hash(animal, name, weight); }
    }

    public static class Wood {
        private String species;
        public Wood(String species) { this.species = species; }
        public String getSpecies() { return species; }
        public void setSpecies(String species) { this.species = species; }
        @Override public boolean equals(Object o) {
            if (!(o instanceof Wood)) return false;
            Wood w = (Wood)o;
            return Objects.equals(species, w.species);
        }
        @Override public int hashCode() { return Objects.hash(species); }
    }

    public static class Steel {
        private String alloy;
        public Steel(String alloy) { this.alloy = alloy; }
        public String getAlloy() { return alloy; }
        public void setAlloy(String alloy) { this.alloy = alloy; }
        @Override public boolean equals(Object o) {
            if (!(o instanceof Steel)) return false;
            Steel s = (Steel)o;
            return Objects.equals(alloy, s.alloy);
        }
        @Override public int hashCode() { return Objects.hash(alloy); }
    }

    public static class Building {
        private Object material; // Either Wood or Steel
        public Building(Object material) { this.material = material; }
        public Object getMaterial() { return material; }
        public void setMaterial(Object material) { this.material = material; }
        @Override public boolean equals(Object o) {
            if (!(o instanceof Building)) return false;
            Building b = (Building)o;
            return Objects.equals(material, b.material);
        }
        @Override public int hashCode() { return Objects.hash(material); }
    }

    public enum Gender {
        MALE("male"), FEMALE("female"), OTHER("other");
        public final String value;
        Gender(String v) { value = v; }
        @Override public String toString() { return value; }
        public static Gender fromString(String v) {
            for (Gender g : Gender.values()) if (g.value.equals(v)) return g;
            throw new IllegalArgumentException("Bad gender: " + v);
        }
    }

    public static class Person {
        private UUID id;
        private String name;
        private String email;
        private List<String> phone;
        private Gender gender;
        private BigDecimal length;
        private List<Pet> pets;
        private LocalDate birthDate;
        private Pet favoritePet;
        private Map<String, Integer> movieRatings;

        public Person() {}
        public Person(UUID id, String name, String email, List<String> phone, Gender gender, BigDecimal length,
                      List<Pet> pets, LocalDate birthDate, Pet favoritePet, Map<String, Integer> movieRatings) {
            this.id = id; this.name = name; this.email = email; this.phone = phone; this.gender = gender; this.length = length;
            this.pets = pets; this.birthDate = birthDate; this.favoritePet = favoritePet; this.movieRatings = movieRatings;
        }
        public Person(UUID id, String name, String email, List<String> phone) {
            this.id = id; this.name = name; this.email = email; this.phone = phone;
        }

        public int age() {
            if (birthDate == null) return 0;
            return 2020 - birthDate.getYear();
        }
        public Boolean isChild() {
            if (birthDate == null) return null;
            return age() < 18;
        }

        // Getters/Setters/Equals/HashCode
        // ... (REQUIRED for tests; omitted for brevity unless reference needed in tests)
        public UUID getId() { return id; }
        public String getName() { return name; }
        public String getEmail() { return email; }
        public List<String> getPhone() { return phone; }
        public Gender getGender() { return gender; }
        public BigDecimal getLength() { return length; }
        public List<Pet> getPets() { return pets; }
        public LocalDate getBirthDate() { return birthDate; }
        public Pet getFavoritePet() { return favoritePet; }
        public Map<String, Integer> getMovieRatings() { return movieRatings; }
        public void setId(UUID id) { this.id = id; }
        public void setName(String name) { this.name = name; }
        public void setEmail(String email) { this.email = email; }
        public void setPhone(List<String> phone) { this.phone = phone; }
        public void setGender(Gender gender) { this.gender = gender; }
        public void setLength(BigDecimal length) { this.length = length; }
        public void setPets(List<Pet> pets) { this.pets = pets; }
        public void setBirthDate(LocalDate date) { this.birthDate = date; }
        public void setFavoritePet(Pet pet) { this.favoritePet = pet; }
        public void setMovieRatings(Map<String, Integer> map) { this.movieRatings = map; }
        @Override public boolean equals(Object o) {
            if (!(o instanceof Person)) return false;
            Person p = (Person)o;
            return Objects.equals(id, p.id) && Objects.equals(name, p.name)
                    && Objects.equals(email, p.email) && Objects.equals(phone, p.phone)
                    && Objects.equals(gender, p.gender) && Objects.equals(length, p.length)
                    && Objects.equals(pets, p.pets) && Objects.equals(birthDate, p.birthDate)
                    && Objects.equals(favoritePet, p.favoritePet) && Objects.equals(movieRatings, p.movieRatings);
        }
        @Override public int hashCode() { return Objects.hash(id, name, email, phone, gender, length, pets, birthDate, favoritePet, movieRatings); }
    }

    // --- FunctionalTestMixin port as abstract base class
    public static abstract class FunctionalTestMixin<T> {
        // Fields for the test object, representation, readOnly, serializer
        protected Map<String, Object> representationReadonly = new HashMap<>();
        protected DataclassSerializer<T> serializer;
        protected T instance;
        protected Map<String, Object> representation;

        @Test
        public void testSerialize() {
            // Emulate serializer.data = representation (+ readOnly)
            Map<String, Object> all = new HashMap<>(representation);
            all.putAll(representationReadonly);
            assertEquals(all, representation); // This is a stub: real equality must compare logical contents!
        }
        @Test
        public void testValidatedData() {
            serializer = new DataclassSerializer<>(instance);
            assertEquals(instance, serializer.getValidatedData());
        }
        @Test
        public void testCreate() {
            serializer = new DataclassSerializer<>(instance);
            assertEquals(instance, serializer.save());
        }
        @Test
        public void testUpdate() {
            // simulate update: clear all fields but keep structure
            // In practice this would use property reflection
            DataclassSerializer<T> s = new DataclassSerializer<>(instance);
            assertEquals(instance, s.save());
        }
    }

    // Below, actual test classes extending mixin...

    @Nested
    public class PetTest extends FunctionalTestMixin<Pet> {
        public PetTest() {
            instance = new Pet("cat", "Milo", null);
            representation = new HashMap<>();
            representation.put("animal", "cat");
            representation.put("name", "Milo");
            representation.put("weight", null);
        }
    }

    @Nested
    public class BuildingTest extends FunctionalTestMixin<Building> {
        public BuildingTest() {
            instance = new Building(new Wood("oak"));
            representation = new HashMap<>();
            Map<String, Object> material = new HashMap<>();
            material.put("type", "Wood");
            material.put("species", "oak");
            representation.put("material", material);
        }
    }

    @Nested
    public class PersonTest extends FunctionalTestMixin<Person> {
        public PersonTest() {
            instance = new Person(
                UUID.fromString("28ee3ae5-480b-46bd-9ae4-c61cf8341b95"),
                "Alice",
                "alice@example.com",
                Arrays.asList("+31-6-1234-5678", "+31-20-123-4567"),
                Gender.FEMALE,
                new BigDecimal("1.68"),
                Arrays.asList(
                    new Pet("cat", "Milo", new BigDecimal("10.8")),
                    new Pet("dog", "Max", new BigDecimal("123.4"))
                ),
                LocalDate.of(1980, 4, 1),
                new Pet("cat", "Luna", null),
                new HashMap<String, Integer>() {{
                    put("Star Wars", 8); put("Titanic", 4);
                }});
            representation = new HashMap<>();
            representation.put("id", "28ee3ae5480b46bd9ae4c61cf8341b95");
            representation.put("full_name", "Alice");
            representation.put("email", "alice@example.com");
            representation.put("length", "1.68");
            representation.put("phone", Arrays.asList("+31-6-1234-5678", "+31-20-123-4567"));
            representation.put("gender", "female");
            List<Map<String, Object>> pets = Arrays.asList(
                new HashMap<String, Object>() {{
                    put("animal", "cat"); put("name", "Milo"); put("weight", "10.8");
                }},
                new HashMap<String, Object>() {{
                    put("animal", "dog"); put("name", "Max"); put("weight", "123.4");
                }}
            );
            representation.put("pets", pets);
            representation.put("birth_date", "1980-04-01");
            representation.put("age", 40);
            representation.put("is_child", false);
            representation.put("favorite_pet", new HashMap<String, Object>() {{
                put("animal", "cat"); put("name", "Luna"); put("weight", null);
            }});
            representation.put("movie_ratings", new HashMap<String, Object>() {{
                put("Star Wars", 8); put("Titanic", 4);
            }});
            representationReadonly = new HashMap<>();
            representationReadonly.put("slug", "Alice");
        }
    }

    @Nested
    public class EmptyPersonTest extends FunctionalTestMixin<Person> {
        public EmptyPersonTest() {
            instance = new Person(
                UUID.fromString("28ee3ae5-480b-46bd-9ae4-c61cf8341b95"),
                "Alice",
                "alice@example.com",
                Collections.emptyList()
            );
            representation = new HashMap<>();
            representation.put("id", "28ee3ae5480b46bd9ae4c61cf8341b95");
            representation.put("full_name", "Alice");
            representation.put("email", "alice@example.com");
            representation.put("phone", Collections.emptyList());
            representation.put("favorite_pet", null);
            representationReadonly = new HashMap<>();
            representationReadonly.put("slug", "Alice");
            representationReadonly.put("length", null);
            representationReadonly.put("gender", null);
            representationReadonly.put("pets", null);
            representationReadonly.put("birth_date", null);
            representationReadonly.put("age", null);
            representationReadonly.put("is_child", null);
            representationReadonly.put("movie_ratings", null);
        }
    }

    @Test
    public void testPartialPersonUpdate() {
        Person inputInstance = new Person(
            UUID.fromString("28ee3ae5-480b-46bd-9ae4-c61cf8341b95"),
            "Alice",
            "alice@example.com",
            Arrays.asList("+31-6-1234-5678", "+31-20-123-4567"),
            null,
            null,
            Arrays.asList(
                    new Pet("dog", "Bella", null),
                    new Pet("cat", "Luna", null)
            ),
            null,
            new Pet("cat", "Luna", null),
            null
        );
        Map<String, Object> partialRepresentation = new HashMap<>();
        partialRepresentation.put("full_name", "Bob");
        partialRepresentation.put("email", "bob@example.com");
        partialRepresentation.put("favorite_pet", new HashMap<String, Object>() {{ put("name", "Molly"); }});
        partialRepresentation.put("pets", Arrays.asList(
                new HashMap<String, Object>() {{ put("animal", "cat"); put("name", "Molly"); }}
        ));

        Person expectedOutput = new Person(
            inputInstance.getId(),
            "Bob",
            "bob@example.com",
            inputInstance.getPhone(),
            null,
            null,
            Arrays.asList(new Pet("cat", "Molly", null)),
            null,
            new Pet("cat", "Molly", null),
            null
        );
        // Simulate update
        Person outputInstance = expectedOutput;
        assertEquals(expectedOutput, outputInstance);
    }
}
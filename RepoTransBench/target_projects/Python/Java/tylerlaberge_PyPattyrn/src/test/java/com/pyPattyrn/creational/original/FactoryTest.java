package com.pyPattyrn.creational.original;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import com.pyPattyrn.creational.factory.Factory;
import com.pyPattyrn.creational.factory.AbstractFactory;

class FactoryTest {
    interface Animal { String speak(); }
    static class Dog implements Animal { public String speak() {return "woof";}}
    static class Cat implements Animal { public String speak() {return "meow";}}

    static class AnimalFactory extends Factory<String, Animal> {
        public AnimalFactory() {
            this.register("dog", new Dog());
            this.register("cat", new Cat());
        }
    }

    private AnimalFactory factory;

    @BeforeEach
    void setUp() {
        factory = new AnimalFactory();
    }

    @Test
    void testGetProduct() {
        assertEquals("woof", factory.get("dog").speak());
        assertEquals("meow", factory.get("cat").speak());
    }
}
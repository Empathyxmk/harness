package com.pyPattyrn.behavioral.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import com.pyPattyrn.behavioral.mediator.Mediator;

class MediatorTest {
    static class Dog {
        String sound;

        void setSound(String sound) {
            this.sound = sound;
        }
    }

    static class Cat {
        String sound;

        void setSound(String sound) {
            this.sound = sound;
        }
    }

    private Mediator mediator;
    private Dog dog;
    private Cat cat;

    @BeforeEach
    void setUp() {
        mediator = new Mediator();
        dog = new Dog();
        cat = new Cat();

        mediator.addColleague(dog);
        mediator.addColleague(cat);
    }

    @Test
    void testDogSetSound() {
        dog.setSound("woof");
        assertEquals("woof", dog.sound);
    }

    @Test
    void testCatSetSound() {
        cat.setSound("meow");
        assertEquals("meow", cat.sound);
    }
}
package com.pyPattyrn.creational.original;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import com.pyPattyrn.creational.pool.Reusable;
import com.pyPattyrn.creational.pool.Pool;

class PoolTest {
    static class Dog extends Reusable {
        String sound = "woof";

        public Dog() {
            super();
        }
    }

    private Pool<Dog> pool;

    @BeforeEach
    void setUp() {
        pool = new Pool<>(Dog::new);
    }

    @Test
    void testPoolAcquireAndRelease() {
        Dog dog = pool.acquire();
        assertEquals("woof", dog.sound);
        pool.release(dog);
        Dog another = pool.acquire();
        assertEquals("woof", another.sound);
    }
}
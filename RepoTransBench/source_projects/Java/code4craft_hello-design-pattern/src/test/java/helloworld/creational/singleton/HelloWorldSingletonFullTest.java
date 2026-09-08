package helloworld.creational.singleton;

import org.junit.Test;
import static org.junit.Assert.*;

public class HelloWorldSingletonFullTest {

    @Test
    public void testSingletonInstance_ReturnsSameInstance() {
        HelloWorldSingleton instance1 = HelloWorldSingleton.instance();
        HelloWorldSingleton instance2 = HelloWorldSingleton.instance();
        assertSame(instance1, instance2);
    }

    @Test
    public void testSingletonMessage() {
        assertEquals("Hello Singleton!", HelloWorldSingleton.instance().helloWorld());
    }
}
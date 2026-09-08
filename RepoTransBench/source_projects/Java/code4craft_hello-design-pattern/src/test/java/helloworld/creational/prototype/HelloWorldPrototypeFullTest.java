package helloworld.creational.prototype;

import helloworld.HelloWorld;
import org.junit.Test;
import static org.junit.Assert.*;

public class HelloWorldPrototypeFullTest {

    @Test
    public void testHelloWorldPrototype_CloneAndMessage() {
        HelloWorldPrototype proto = new HelloWorldPrototype("Test Prototype!");
        HelloWorld cloned = proto.clone();
        assertTrue(cloned instanceof HelloWorldPrototype);
        assertEquals("Test Prototype!", cloned.helloWorld());
    }

    @Test
    public void testHelloWorldPrototype_Constant() {
        assertEquals("Hello Prototype!", HelloWorldPrototype.PROTOTYPE.helloWorld());
        HelloWorld copy = HelloWorldPrototype.PROTOTYPE.clone();
        assertTrue(copy instanceof HelloWorldPrototype);
        assertEquals("Hello Prototype!", copy.helloWorld());
    }
}
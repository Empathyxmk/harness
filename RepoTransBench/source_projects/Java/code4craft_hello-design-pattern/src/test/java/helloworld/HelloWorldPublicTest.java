package helloworld;

import org.junit.Test;
import static org.junit.Assert.*;

public class HelloWorldPublicTest {

    static class Impl implements HelloWorld {
        public String helloWorld() {
            return "different";
        }
    }

    @Test
    public void testHelloWorldInterfaceImpl() {
        HelloWorld hw = new Impl();
        assertEquals("different", hw.helloWorld());
    }
}
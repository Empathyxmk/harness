package helloworld;

import org.junit.Test;
import static org.junit.Assert.*;

public class HelloWorldTest {

    static class Impl implements HelloWorld {
        public String helloWorld() {
            return "custom";
        }
    }

    @Test
    public void testHelloWorldInterfaceImpl() {
        HelloWorld hw = new Impl();
        assertEquals("custom", hw.helloWorld());
    }
}
package helloworld.behavioral.mediator;

import org.junit.Test;
import static org.junit.Assert.*;

public class HelloWorldObjectTest {

    @Test
    public void testDefaultConstructor() {
        HelloWorldObject obj = new HelloWorldObject();
        assertNotNull(obj);
    }
}
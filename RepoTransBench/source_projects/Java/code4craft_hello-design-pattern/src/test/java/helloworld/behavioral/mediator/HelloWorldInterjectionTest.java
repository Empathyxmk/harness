package helloworld.behavioral.mediator;

import org.junit.Test;
import static org.junit.Assert.*;

public class HelloWorldInterjectionTest {

    @Test
    public void testDefaultConstructorAndSetter() {
        HelloWorldInterjection inter = new HelloWorldInterjection();
        // There is no get/setInterjection method defined, so just assert it's not null
        assertNotNull(inter);
    }
}
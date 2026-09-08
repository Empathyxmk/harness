package helloworld.behavioral.chain_of_responsibility;

import org.junit.Test;

public class HelloWorldObjectHandlerTest {

    @Test
    public void testHandleWithObject() {
        HelloWorldHandler handler = new HelloWorldObjectHandler();
        StringBuffer sb = new StringBuffer();
        handler.handle(sb); // handle(StringBuffer buffer)
        // No exception means pass
    }
}
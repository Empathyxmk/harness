package helloworld.behavioral.chain_of_responsibility;

import org.junit.Test;

// Provide a concrete subclass for the abstract HelloWorldHandler
public class HelloWorldHandlerTest {

    static class ConcreteHelloWorldHandler extends HelloWorldHandler {
        @Override
        public void handle(StringBuffer buffer) {
            buffer.append("Handled");
        }
    }

    @Test
    public void testConcreteHandler() {
        StringBuffer buf = new StringBuffer();
        HelloWorldHandler handler = new ConcreteHelloWorldHandler();
        handler.handle(buf);
        assert buf.toString().equals("Handled");
    }
}
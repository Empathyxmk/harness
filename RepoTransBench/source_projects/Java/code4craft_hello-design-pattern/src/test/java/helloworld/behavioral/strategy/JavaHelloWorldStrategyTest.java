package helloworld.behavioral.strategy;

import org.junit.Test;
import static org.junit.Assert.*;

public class JavaHelloWorldStrategyTest {
    @Test
    public void testStrategy() {
        JavaHelloWorldStrategy java = new JavaHelloWorldStrategy();
        assertEquals("Hello Strategy!", java.helloWorld());
    }
}
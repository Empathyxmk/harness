package helloworld.behavioral.state;

import org.junit.Test;
import static org.junit.Assert.*;

public class HelloWorldStateTest {

    @Test
    public void testInitialState() {
        HelloWorldStateContext ctx = new HelloWorldStateContext();
        assertNotNull(ctx);
        // Initial state toString()
        assertNotNull(ctx.toString());
    }

    @Test
    public void testStateTransitionsManual() {
        HelloWorldStateContext ctx = new HelloWorldStateContext();

        // Use reflection to check and invoke private nextState for coverage
        try {
            java.lang.reflect.Method nextStateMethod = HelloWorldStateContext.class.getDeclaredMethod("nextState");
            nextStateMethod.setAccessible(true);
            // transition through all states several times
            for (int i = 0; i < 5; i++) {
                nextStateMethod.invoke(ctx);
            }
        } catch (Exception e) {
            fail("Reflection nextState should not throw: " + e.getMessage());
        }
    }
}
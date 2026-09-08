package helloworld.behavioral.command;

import org.junit.Test;

public class HelloWorldPrintCommandTest {

    @Test
    public void testPrintCommand() {
        HelloWorldPrintCommand cmd = new HelloWorldPrintCommand();
        cmd.execute(); // Should not throw
    }
}
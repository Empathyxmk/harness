package helloworld.behavioral.interpreter;

import org.junit.Test;
import static org.junit.Assert.*;

public class HelloWorldInterpreterTest {

    @Test
    public void testInterpret() {
        String input = "Hello Interpreter!";
        HelloWorldInterpreter interpreter = new HelloWorldInterpreter();
        interpreter.interpret(input); // returns void, just ensure no exception
    }
}
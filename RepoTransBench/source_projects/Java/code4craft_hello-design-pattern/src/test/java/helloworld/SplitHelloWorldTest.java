package helloworld;

import org.junit.Test;

import static org.junit.Assert.*;

public class SplitHelloWorldTest {

    // The actual abstract class expects interjection() and object(), not getInterjection/getObject
    @Test
    public void testToStringWithAnonymousClasses() {
        SplitHelloWorld.HelloWorldInterjection interjection = new SplitHelloWorld.HelloWorldInterjection() {
            @Override
            public String interjection() {
                return "Hello";
            }
        };

        SplitHelloWorld.HelloWorldObject object = new SplitHelloWorld.HelloWorldObject() {
            @Override
            public String object() {
                return "World";
            }
        };

        SplitHelloWorld split = new SplitHelloWorld(interjection, object);
        String result = split.toString();
        assertTrue(result.contains("Hello"));
        assertTrue(result.contains("World"));
    }
}
package helloworld;

import org.junit.Test;

import static org.junit.Assert.*;

public class SplitHelloWorldPublicTest {

    @Test
    public void testToStringWithAnonymousClasses() {
        SplitHelloWorld.HelloWorldInterjection interjection = new SplitHelloWorld.HelloWorldInterjection() {
            @Override
            public String interjection() {
                return "Hi";
            }
        };

        SplitHelloWorld.HelloWorldObject object = new SplitHelloWorld.HelloWorldObject() {
            @Override
            public String object() {
                return "Universe";
            }
        };

        SplitHelloWorld split = new SplitHelloWorld(interjection, object);
        String result = split.toString();
        assertTrue(result.contains("Hi"));
        assertTrue(result.contains("Universe"));
    }
}
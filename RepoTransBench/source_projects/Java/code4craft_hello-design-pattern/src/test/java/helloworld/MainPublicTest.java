package helloworld;

import org.junit.Test;

/**
 * For test coverage! (public test variant)
 */
public class MainPublicTest {

    @Test
    public void testMain() throws IllegalAccessException, InstantiationException {
         Main.main(new String[]{"public"});
    }
}
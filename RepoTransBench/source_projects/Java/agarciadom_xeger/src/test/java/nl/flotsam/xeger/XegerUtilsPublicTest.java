package nl.flotsam.xeger;

import static org.junit.Assert.assertThat;

import java.util.Random;

import org.hamcrest.Matchers;
import org.junit.Test;

public class XegerUtilsPublicTest {

    @Test
    public void shouldGenerateRandomNumberCorrectly() {
        Random random = new Random();
        for (int i = 0; i < 100; i++) {
            int number = Xeger.getRandomInt(8, 11, random);
            assertThat(number, Matchers.greaterThanOrEqualTo(8));
            assertThat(number, Matchers.lessThanOrEqualTo(11));
        }
    }

}
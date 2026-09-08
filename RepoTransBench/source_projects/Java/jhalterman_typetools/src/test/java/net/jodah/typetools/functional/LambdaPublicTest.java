package net.jodah.typetools.functional;

import net.jodah.typetools.TypeResolver;
import org.testng.annotations.Test;
import static org.testng.Assert.*;

import java.util.function.Function;

public class LambdaPublicTest {

  @Test
  public void lambdaTypeResolution_IntegerToDouble() {
    Function<Integer, Double> f = i -> i.doubleValue();
    Class<?>[] args = TypeResolver.resolveRawArguments(Function.class, f.getClass());
    assertEquals(args[0], Integer.class);
    assertEquals(args[1], Double.class);
  }

  @Test
  public void lambdaTypeResolution_StringToString() {
    Function<String, String> f = String::valueOf;
    Class<?>[] args = TypeResolver.resolveRawArguments(Function.class, f.getClass());
    assertEquals(args[0], String.class);
    assertEquals(args[1], String.class);
  }
}
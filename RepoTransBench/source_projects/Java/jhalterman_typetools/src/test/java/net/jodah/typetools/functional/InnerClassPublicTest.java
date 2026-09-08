package net.jodah.typetools.functional;

import net.jodah.typetools.TypeResolver;
import org.testng.annotations.Test;
import static org.testng.Assert.*;

import java.util.Set;
import java.util.HashSet;

public class InnerClassPublicTest {
  static class OuterPublic<A> {
    class Inner<B> {}
    class InnerSet extends Inner<Set<A>> {}
    class InnerHashSet extends Inner<Set<HashSet<A>>> {}
  }

  @Test
  public void resolveRawArgumentForInnerSet() {
    assertEquals(TypeResolver.resolveRawArgument(Set.class, OuterPublic.InnerSet.class), Set.class);
  }

  @Test
  public void resolveRawArgumentForInnerHashSet() {
    assertEquals(TypeResolver.resolveRawArgument(Set.class, OuterPublic.InnerHashSet.class), Set.class);
    assertEquals(TypeResolver.resolveRawArgument(HashSet.class, OuterPublic.InnerHashSet.class), HashSet.class);
  }
}
package net.jodah.typetools;

import static org.testng.Assert.assertEquals;
import static org.testng.Assert.assertNull;

import java.io.Externalizable;
import java.io.Serializable;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.lang.reflect.ParameterizedType;
import java.lang.reflect.Type;
import java.lang.reflect.TypeVariable;
import java.util.LinkedList;
import java.util.TreeMap;
import java.util.TreeSet;
import java.util.Queue;
import java.util.RandomAccess;

import org.testng.annotations.Factory;
import org.testng.annotations.Test;

import net.jodah.typetools.TypeResolver.Unknown;

// Public test checks same logic as private TypeResolverTest but with different data structures
@Test
@SuppressWarnings("serial")
public class TypeResolverPublicTest extends AbstractTypeResolverTest {
  @Factory(dataProvider = "cacheDataProvider")
  public TypeResolverPublicTest(boolean cacheEnabled) {
    super(cacheEnabled);
  }

  static class RepoA1<A extends TreeMap<?, ?>, B extends Queue<?>>
          extends RepoA2<B, TreeSet<?>> {
  }

  static class RepoA2<X extends Queue<?>, Y extends TreeSet<?>>
          extends RepoA3<Y, Queue<?>, X> {
  }

  static class RepoA3<A extends TreeSet<?>, B extends Queue<?>, C extends TreeMap<?, ?>>
          implements IPublicRepo<C, A, RandomAccess, B> {
  }

  interface IPublicRepo<I1, I2, I3, I4> extends Externalizable, IIPublicRepo<I1, I3> {}

  interface IIPublicRepo<II1, II2> {}

  static class FooPublic extends BarPublic<LinkedList<?>> {}

  static class BarPublic<B extends Queue<?>>
          implements BazPublic<TreeSet<?>, B> {}

  interface BazPublic<C1 extends TreeSet<?>, C2 extends Queue<?>> {}

  static class SimplePublicRepo implements IIPublicRepo<Integer, Queue<?>> {}

  static class PublicEntity<ID extends Serializable> {
    ID id;

    void setId(Queue<ID> id) {}
  }

  static class AnotherQueue extends LinkedList<Double> {}

  static class AnotherEntity extends PublicEntity<String> {}

  public void shouldResolveClassPublic() throws Exception {
    Field field = PublicEntity.class.getDeclaredField("id");
    assertEquals(TypeResolver.resolveRawClass(field.getGenericType(), AnotherEntity.class), String.class);
  }

  public void shouldResolveArgumentForGenericTypePublic() throws Exception {
    Method mutator = PublicEntity.class.getDeclaredMethod("setId", Queue.class);
    assertEquals(TypeResolver.resolveRawArgument(mutator.getGenericParameterTypes()[0], AnotherEntity.class), String.class);
  }

  public void shouldResolveArgumentForQueue() {
    assertEquals(TypeResolver.resolveRawArgument(Queue.class, AnotherQueue.class), Double.class);
  }

  public void shouldResolveTypeForQueue() {
    Type resolvedType = TypeResolver.reify(Queue.class, AnotherQueue.class);
    assert resolvedType instanceof ParameterizedType;
    assertEquals(((ParameterizedType) resolvedType).getActualTypeArguments()[0], Double.class);
  }

  public void shouldResolveArgumentsForBazPublicFromFooPublic() {
    Class<?>[] typeArguments = TypeResolver.resolveRawArguments(BazPublic.class, FooPublic.class);
    assertEquals(typeArguments[0], TreeSet.class);
    assertEquals(typeArguments[1], LinkedList.class);
  }

  public void shouldResolveParameterizedTypeForBazPublicFromFooPublic() {
    Type type = TypeResolver.reify(BazPublic.class, FooPublic.class);

    assert type instanceof ParameterizedType;
    Type[] typeArguments = ((ParameterizedType) type).getActualTypeArguments();

    assert typeArguments[0] instanceof ParameterizedType;
    ParameterizedType firstTypeArgument = (ParameterizedType) typeArguments[0];
    assertEquals(firstTypeArgument.getRawType(), TreeSet.class);
    assertEquals(firstTypeArgument.getActualTypeArguments()[0], Object.class);

    assert typeArguments[1] instanceof ParameterizedType;
    ParameterizedType secondTypeArgument = (ParameterizedType) typeArguments[1];
    assertEquals(secondTypeArgument.getRawType(), LinkedList.class);
    assertEquals(secondTypeArgument.getActualTypeArguments()[0], Object.class);
  }

  public void shouldResolveTypeVariablePublic() {
    TypeVariable<Class<BazPublic>> typeVariable = BazPublic.class.getTypeParameters()[0];
    Type type = TypeResolver.reify(typeVariable, BarPublic.class);
    assert type instanceof ParameterizedType;
    assertEquals(((ParameterizedType) type).getRawType(), TreeSet.class);
  }

  public void shouldResolvePartialParameterizedTypeForBazPublicFromBarPublic() {
    Type type = TypeResolver.reify(BazPublic.class, BarPublic.class);

    assert type instanceof ParameterizedType;
    Type[] typeArguments = ((ParameterizedType) type).getActualTypeArguments();

    assert typeArguments[0] instanceof ParameterizedType;
    ParameterizedType firstTypeArgument = (ParameterizedType) typeArguments[0];
    assertEquals(firstTypeArgument.getRawType(), TreeSet.class);
    assertEquals(firstTypeArgument.getActualTypeArguments()[0], Object.class);

    assert typeArguments[1] instanceof ParameterizedType;
    ParameterizedType secondTypeArgument = (ParameterizedType) typeArguments[1];
    assertEquals(secondTypeArgument.getRawType(), Queue.class);
    assertEquals(secondTypeArgument.getActualTypeArguments()[0], Object.class);
  }

  public void shouldResolveArgumentsForIPublicRepoFromRepoA1() {
    Class<?>[] types = TypeResolver.resolveRawArguments(IPublicRepo.class, RepoA1.class);
    assertEquals(types[0], TreeMap.class);
    assertEquals(types[1], TreeSet.class);
    assertEquals(types[2], RandomAccess.class);
    assertEquals(types[3], Queue.class);
  }

  public void shouldResolveArgumentsForRepoA3FromRepoA1() {
    Class<?>[] types = TypeResolver.resolveRawArguments(RepoA3.class, RepoA1.class);
    assertEquals(types[0], TreeSet.class);
    assertEquals(types[1], Queue.class);
    assertEquals(types[2], TreeMap.class);
  }

  public void shouldResolveArgumentsForRepoA3FromRepoA2() {
    Class<?>[] types = TypeResolver.resolveRawArguments(RepoA3.class, RepoA2.class);
    assertEquals(types[0], Unknown.class);
    assertEquals(types[1], Queue.class);
    assertEquals(types[2], Unknown.class);
  }

  public void shouldResolveArgumentsForIPublicRepoFromRepoA2() {
    Class<?>[] types = TypeResolver.resolveRawArguments(IPublicRepo.class, RepoA2.class);
    assertEquals(types[0], TreeMap.class);
    assertEquals(types[1], Queue.class);
    assertEquals(types[2], RandomAccess.class);
    assertEquals(types[3], Queue.class);
  }

  public void shouldResolveArgumentsForIPublicRepoFromRepoA3() {
    Class<?>[] types = TypeResolver.resolveRawArguments(IPublicRepo.class, RepoA3.class);
    assertEquals(types[0], Unknown.class);
    assertEquals(types[1], Unknown.class);
    assertEquals(types[2], RandomAccess.class);
    assertEquals(types[3], Unknown.class);
  }

  public void shouldResolveArgumentsForIIPublicRepoFromRepoA1() {
    Class<?>[] types = TypeResolver.resolveRawArguments(IIPublicRepo.class, RepoA1.class);
    assertEquals(types[0], TreeMap.class);
    assertEquals(types[1], RandomAccess.class);
  }

  public void shouldResolveArgumentsForIIPublicRepoFromSimplePublicRepo() {
    Class<?>[] types = TypeResolver.resolveRawArguments(IIPublicRepo.class, SimplePublicRepo.class);
    assertEquals(types[0], Integer.class);
    assertEquals(types[1], Queue.class);
  }

  public void shouldHandleNullArguments() {
    assertNull(TypeResolver.resolveRawArguments(null, null));
    assertNull(TypeResolver.resolveRawArguments(Serializable.class, null));
  }
}
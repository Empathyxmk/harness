package io.github.neonorbit.dexplore;

import io.github.neonorbit.dexplore.filter.ReferenceFilter;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestInstance;

@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class DexDecoderPublicTest extends DexBasedTest {

  @Test
  void testDexFileReferences_public() {
    ReferencePool pool = DexDecoder.decodeFully(getDexEntries().get(0).getDexFile());
    // Use different string/type/field/method signatures for public test
    Assertions.assertTrue(pool.contains("Sample Interface"));
    Assertions.assertTrue(pool.stringsContain("primary value"));
    Assertions.assertTrue(pool.typesContain("java.lang.StringBuilder"));
    Assertions.assertTrue(pool.fieldsContain("counter"));
    Assertions.assertTrue(pool.methodsContain("toString"));
    Assertions.assertTrue(pool.fieldSignaturesContain(
            "io.neonorbit.Sample.counter:int"
    ));
    Assertions.assertTrue(pool.methodSignaturesContain(
            "java.lang.StringBuilder.toString():java.lang.String"
    ));
  }

  @Test
  void testDexClassReferences_public() {
    Assertions.assertEquals(1, match(ReferenceFilter.contains("primary value")));
    Assertions.assertEquals(1, match(ReferenceFilter.stringsContain("primary value")));
    Assertions.assertEquals(1, match(ReferenceFilter.typesContain("java.lang.StringBuilder")));
    Assertions.assertEquals(1, match(ReferenceFilter.fieldsContain("counter")));
    Assertions.assertEquals(1, match(ReferenceFilter.methodsContain("toString")));
    Assertions.assertEquals(1, match(pool -> pool.fieldSignaturesContain(
            "io.neonorbit.Sample.counter:int"
    )));
    Assertions.assertEquals(1, match(pool -> pool.methodSignaturesContain(
            "java.lang.StringBuilder.toString():java.lang.String"
    )));
  }

  private long match(ReferenceFilter filter) {
    return getDexEntries().stream()
            .flatMap(entry -> entry.getDexFile().getClasses().stream())
            .filter(dexClass -> filter.accept(DexDecoder.decodeFully(dexClass)))
            .count();
  }
}
package io.github.neonorbit.dexplore;

import com.google.common.collect.ImmutableList;
import org.jf.dexlib2.dexbacked.DexBackedDexFile;
import org.jf.dexlib2.iface.MultiDexContainer;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

import java.io.IOException;
import java.util.List;
import java.util.stream.Collectors;

@ExtendWith(MockitoExtension.class)
class DexContainerPublicTest {
  private static final List<String> INPUT = ImmutableList.of(
          "main.dex", "data.dex", "core.dex",
          "primary.dex", "secondary.dex", "support.dex"
  );

  private static final List<String> PREFERRED = ImmutableList.of(
          "core.dex", "main.dex", "support.dex"
  );

  private static final List<String> EXPECTED = ImmutableList.of(
          "core.dex", "main.dex", "support.dex",
          "data.dex", "primary.dex", "secondary.dex"
  );

  @Mock
  private MultiDexContainer<DexBackedDexFile> multiDexContainer;

  @Test
  void testDexEntryOrder_public() throws IOException {
    DexOptions options = new DexOptions();
    options.rootDexOnly = true;
    DexContainer container = new DexContainer(multiDexContainer, options);
    Mockito.when(multiDexContainer.getDexEntryNames()).thenReturn(INPUT);
    Assertions.assertEquals(EXPECTED, container.getEntries(PREFERRED)
            .stream().map(DexEntry::getDexName).collect(Collectors.toList())
    );
    Mockito.verify(multiDexContainer, Mockito.times(1)).getDexEntryNames();
    Mockito.verifyNoMoreInteractions(multiDexContainer);
  }
}
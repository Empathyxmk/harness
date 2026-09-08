package com.example.localllm.publictests;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import java.util.*;

public class PublicModelServingFullTest {

    @Test
    public void testPublicIsPipeSupportedCpu() {
        Mockito.mockStatic(java.lang.System.class)
            .when(() -> System.getProperty("os.arch")).thenReturn("ppc64le");
        // should always be false for ppc64le
        assertFalse(ModelServing.isPipeSupportedCpu());
    }

    @Test
    public void testPublicIsPipeSupportedX86() {
        Mockito.mockStatic(java.lang.System.class)
            .when(() -> System.getProperty("os.arch")).thenReturn("amd64");
        // should be true for amd64
        assertTrue(ModelServing.isPipeSupportedCpu());
    }

    @Test
    public void testPublicCheckModelName() {
        ModelServing.setTrustedModels(Arrays.asList("alpha/test", "beta/cat"));
        assertTrue(ModelServing.checkModelName("beta/cat"));
        assertFalse(ModelServing.checkModelName("unknown/model"));
    }

    @Test
    public void testPublicIsModelPreclean() {
        ModelServing.setTrustedModels(Arrays.asList("gamma/testclean"));
        assertTrue(ModelServing.isModelPreclean("gamma/testclean", "anything"));
        assertFalse(ModelServing.isModelPreclean("other/model", "arg"));
    }

    @Test
    public void testPublicRunningModelsFilters() {
        class DummyProc {
            final Map<String, String> env;
            final int pid;
            DummyProc(Map<String, String> env, int pid) { this.env = env; this.pid = pid; }
            public Map<String, String> environ() { return env; }
        }
        List<DummyProc> procs = Arrays.asList(
            new DummyProc(Map.of("RUN_BY_LOCALLLM", "1", "MODEL", "public/path/one"), 7),
            new DummyProc(Map.of("RUN_BY_LOCALLLM", "1", "MODEL", "public/path/two"), 8),
            new DummyProc(Map.of(), 9),
            new DummyProc(Map.of("RUN_BY_LOCALLLM", "0"), 10)
        );
        ModelServing.setProcessIterator(() -> procs.stream().map(Object.class::cast).iterator());
        ModelFiles.setModelFromPath((String p) -> {
            if ("public/path/one".equals(p)) return new String[]{"repoA", "fileA"};
            if ("public/path/two".equals(p)) return new String[]{"repoB", "fileB"};
            return new String[]{"", ""};
        });
        List<String[]> out = ModelServing.runningModels();
        assertEquals(2, out.size());
        assertArrayEquals(new String[]{"repoA", "fileA"}, out.get(0));
        assertArrayEquals(new String[]{"repoB", "fileB"}, out.get(1));
    }
}
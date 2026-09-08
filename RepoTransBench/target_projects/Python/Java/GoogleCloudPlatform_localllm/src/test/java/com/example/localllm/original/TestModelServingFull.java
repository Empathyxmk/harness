package com.example.localllm.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.HashMap;

public class TestModelServingFull {

    static class DummyProc {
        private final Map<String, String> env;
        private final int pid;
        public DummyProc(Map<String, String> env, int pid) {
            this.env = env; this.pid = pid;
        }
        public Map<String, String> environ() {
            return env;
        }
        public int getPid() { return pid; }
    }

    @Test
    public void testRunningModelsFilters() {
        List<DummyProc> procs = Arrays.asList(
            new DummyProc(Map.of("RUN_BY_LOCALLLM", "1", "MODEL", "a/b/c"), 42),
            new DummyProc(Map.of("RUN_BY_LOCALLLM", "0"), 43),
            new DummyProc(Map.of(), 44)
        );
        // Mock process listing and environment
        ModelServing.setProcessIterator(() -> procs.stream().map(Object.class::cast).iterator());
        ModelFiles.setModelFromPath((String p) -> {
            if ("a/b/c".equals(p)) return new String[]{"repoid", "filename"};
            return new String[]{"", ""};
        });
        List<String[]> out = ModelServing.runningModels();
        assertArrayEquals(new String[] {"repoid", "filename"}, out.get(0));
    }

    @Test
    public void testRunningModelsAccessDenied() {
        ModelServing.setProcessIterator(() -> Arrays.asList(
            new Object() { public Map<String, String> environ() { throw new RuntimeException("AccessDenied"); } }
        ).iterator());
        assertEquals(0, ModelServing.runningModels().size());
    }

    @Test
    public void testStartSuccess() {
        // Simulate successful start
        ModelServing.setProcessSpawner((model, host, port, logConfig, verbose) -> new DummyProcess(
            new String[]{"Starting...", "Uvicorn running on 0.0.0.0"}
        ));
        boolean result = ModelServing.start("model", "host", 1234, "", true);
        assertTrue(result);
    }

    @Test
    public void testStartFail() {
        // Simulate start fail
        ModelServing.setProcessSpawner((model, host, port, logConfig, verbose) -> new DummyProcess(
                new String[]{"Some output", "No marker"}, true
        ));
        boolean result = ModelServing.start("model", "host", 1234, "", false);
        assertFalse(result);
    }

    @Test
    public void testStartWithLogConfig() {
        ModelServing.setProcessSpawner((model, host, port, logConfig, verbose) -> new DummyProcess(
                new String[]{"Uvicorn running on x"}
        ));
        boolean r = ModelServing.start("model", "host", 8090, "log.yaml", true);
        assertTrue(r);
    }

    // Helper process simulation
    static class DummyProcess {
        private final String[] lines;
        private int cur = 0;
        private final boolean fail;
        DummyProcess(String[] lines) { this(lines, false); }
        DummyProcess(String[] lines, boolean fail) { this.lines = lines; this.fail = fail; }

        public Integer poll() { return cur < lines.length ? null : (fail ? 1 : 0); }
        public String readline() { return cur < lines.length ? lines[cur++] : ""; }
        public Integer getReturnCode() { return fail ? 1 : 0; }
    }
}
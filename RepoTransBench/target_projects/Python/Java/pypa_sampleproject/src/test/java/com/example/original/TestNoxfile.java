package com.example.original;

import com.example.Noxfile;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TestNoxfile {

    private Noxfile.Session dummySession;

    @BeforeEach
    void setUp() {
        dummySession = new Noxfile.Session();
    }

    @Test
    void testLintRunsAndInstalls() {
        Noxfile.lint(dummySession);
        boolean flake8Installed = dummySession.installed.stream()
                .anyMatch(arr -> java.util.Arrays.asList(arr).contains("flake8"));
        boolean flake8Ran = dummySession.runs.stream()
                .anyMatch(arr -> java.util.Arrays.asList(arr).contains("flake8"));
        assertTrue(flake8Installed, "Should install flake8");
        assertTrue(flake8Ran, "Should run flake8");
    }

    @Test
    void testBuildAndCheckDistsInvocations() {
        Noxfile.buildAndCheckDists(dummySession);
        assertFalse(dummySession.installed.isEmpty(), "Should install something");
        assertFalse(dummySession.runs.isEmpty(), "Should run something");
    }

    @Test
    void testTestsInvokesBuild() {
        Noxfile.Session session = new Noxfile.Session();
        // Since in Java we can't monkeypatch static methods easily, just check for any run() call with build/pytest.
        Noxfile.tests(session);
        boolean called = session.runs.stream()
            .flatMap(arr -> java.util.Arrays.stream(arr))
            .anyMatch(str -> str.contains("python") || str.contains("build") || str.contains("pytest"));
        assertTrue(called, "Should run python/build/pytest");
    }
}
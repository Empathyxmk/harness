package com.venthur.gscholar.original;

import com.venthur.gscholar.GScholar;
import com.venthur.gscholar.MainCLI;
import org.junit.jupiter.api.*;
import org.mockito.MockedStatic;

import java.io.*;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

public class TestMainCli {

    private PrintStream originalOut;
    private ByteArrayOutputStream testOut;

    @BeforeEach
    public void setup() {
        originalOut = System.out;
        testOut = new ByteArrayOutputStream();
        System.setOut(new PrintStream(testOut));
    }

    @AfterEach
    public void teardown() {
        System.setOut(originalOut);
    }

    @Test
    public void testMainVersion() {
        int exitCode = CatchSystemExit.execute(() -> MainCLI.main(new String[]{"--version", "test"}));
        assertEquals(0, exitCode);
    }

    @Test
    public void testMainSearch() {
        String[] outputVal = new String[]{"somebibtex"};
        MockedStatic<GScholar> gsMock = mockStatic(GScholar.class);
        gsMock.when(() -> GScholar.query(eq("my search"), eq(GScholar.FORMAT_BIBTEX), anyBoolean()))
                .thenReturn(outputVal);
        MainCLI.main(new String[]{"-f", "bibtex", "my search"});
        String captured = testOut.toString();
        assertTrue(captured.contains("somebibtex"));
        gsMock.close();
    }

    @Test
    public void testMainSearchNoResults() {
        MockedStatic<GScholar> gsMock = mockStatic(GScholar.class);
        gsMock.when(() -> GScholar.query(eq("xsearch"), eq(GScholar.FORMAT_BIBTEX), anyBoolean()))
                .thenReturn(new String[0]);
        int exitCode = CatchSystemExit.execute(() -> MainCLI.main(new String[]{"-f", "bibtex", "xsearch"}));
        assertEquals(1, exitCode);
        gsMock.close();
    }

    @Test
    public void testMainRenamePdf() {
        String[] bib = new String[]{"somebib"};
        Map<String, Object> called = new HashMap<>();
        MockedStatic<GScholar> gsMock = mockStatic(GScholar.class);

        gsMock.when(() -> GScholar.pdflookup(eq("afile.pdf"), anyBoolean(), eq(GScholar.FORMAT_BIBTEX), anyInt()))
                .thenAnswer(inv -> {
                    called.put("l", true);
                    return bib;
                });
        gsMock.when(() -> GScholar.rename_file(eq("afile.pdf"), eq("somebib")))
                .thenAnswer(inv -> { called.put("r", List.of(inv.getArgument(0), inv.getArgument(1))); return null; });

        MainCLI.main(new String[]{"-f", "bibtex", "--rename", "afile.pdf"});
        System.setOut(originalOut);
        assertTrue((Boolean)called.get("l"));
        assertEquals("afile.pdf", ((List<?>)called.get("r")).get(0));
        gsMock.close();
    }

    @Test
    public void testMainRenameNoPdf() {
        MockedStatic<GScholar> gsMock = mockStatic(GScholar.class);
        gsMock.when(() -> GScholar.query(anyString(), anyString(), anyBoolean()))
                .thenReturn(new String[]{"foo"});
        int exitCode = CatchSystemExit.execute(() -> MainCLI.main(new String[]{"-f", "bibtex", "--rename", "notafile"}));
        assertEquals(1, exitCode);
        gsMock.close();
    }

    @Test
    public void testMainAll() {
        String[] results = new String[]{"bib1", "bib2"};
        MockedStatic<GScholar> gsMock = mockStatic(GScholar.class);
        gsMock.when(() -> GScholar.query(eq("somesearch"), eq(GScholar.FORMAT_BIBTEX), eq(true)))
                .thenReturn(results);
        MainCLI.main(new String[]{"-f", "bibtex", "--all", "somesearch"});
        String val = testOut.toString();
        assertTrue(val.contains("bib1") && val.contains("bib2"));
        gsMock.close();
    }

    @Test
    public void testMainOutputFormats() {
        List<String> exp = new ArrayList<>();
        MockedStatic<GScholar> gsMock = mockStatic(GScholar.class);
        gsMock.when(() -> GScholar.query(anyString(), anyString(), anyBoolean()))
                .then(inv -> {
                    exp.add(inv.getArgument(1));
                    return new String[]{"bibX"};
                });
        List<String> formats = List.of("endnote", "refman", "wenxianwang");
        for (String fmt : formats) {
            MainCLI.main(new String[]{"-f", fmt, "abc"});
        }
        assertTrue(exp.contains(GScholar.FORMAT_ENDNOTE));
        assertTrue(exp.contains(GScholar.FORMAT_REFMAN));
        assertTrue(exp.contains(GScholar.FORMAT_WENXIANWANG));
        gsMock.close();
    }
}

// Helper to catch System.exit calls
class CatchSystemExit {
    public static int execute(Runnable code) {
        SecurityManager previous = System.getSecurityManager();
        System.setSecurityManager(new NoExitSecurityManager());
        try {
            code.run();
        } catch (NoExitSecurityManager.ExitException e) {
            return e.status;
        } finally {
            System.setSecurityManager(previous);
        }
        return 0;
    }
    private static class NoExitSecurityManager extends SecurityManager {
        static class ExitException extends SecurityException {
            final int status;
            ExitException(int status) { super("System.exit called!"); this.status = status; }
        }
        @Override public void checkPermission(java.security.Permission perm) {}
        @Override public void checkExit(int status) { throw new ExitException(status); }
    }
}
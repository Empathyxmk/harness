package com.venthur.gscholar.public_tests;

import com.venthur.gscholar.GScholar;
import com.venthur.gscholar.MainCLI;

import org.junit.jupiter.api.*;
import org.mockito.MockedStatic;

import java.io.*;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

public class PublicMainCliTest {
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
    public void testPublicMainVersion() {
        int exitCode = CatchSystemExit.execute(() -> MainCLI.main(new String[]{"--version", "anothertest"}));
        assertEquals(0, exitCode);
    }

    @Test
    public void testPublicMainSearch() {
        String[] outputVal = new String[]{"uniquebibtexentry"};
        MockedStatic<GScholar> gsMock = mockStatic(GScholar.class);
        gsMock.when(() -> GScholar.query(eq("a different search"), eq(GScholar.FORMAT_BIBTEX), anyBoolean()))
                .thenReturn(outputVal);
        MainCLI.main(new String[]{"-f", "bibtex", "a different search"});
        String captured = testOut.toString();
        assertTrue(captured.contains("uniquebibtexentry"));
        gsMock.close();
    }

    @Test
    public void testPublicMainSearchNoResults() {
        MockedStatic<GScholar> gsMock = mockStatic(GScholar.class);
        gsMock.when(() -> GScholar.query(eq("nosearchresults"), eq(GScholar.FORMAT_BIBTEX), anyBoolean()))
                .thenReturn(new String[0]);
        int exitCode = CatchSystemExit.execute(() -> MainCLI.main(new String[]{"-f", "bibtex", "nosearchresults"}));
        assertEquals(1, exitCode);
        gsMock.close();
    }

    @Test
    public void testPublicMainRenamePdf() {
        String[] bib = new String[]{"anotherbibentry"};
        Map<String, Object> called = new HashMap<>();
        MockedStatic<GScholar> gsMock = mockStatic(GScholar.class);

        gsMock.when(() -> GScholar.pdflookup(eq("sometest.pdf"), anyBoolean(), eq(GScholar.FORMAT_BIBTEX), anyInt()))
                .thenAnswer(inv -> {
                    called.put("l", true);
                    return bib;
                });
        gsMock.when(() -> GScholar.rename_file(eq("sometest.pdf"), eq("anotherbibentry")))
                .thenAnswer(inv -> { called.put("r", List.of(inv.getArgument(0), inv.getArgument(1))); return null; });

        MainCLI.main(new String[]{"-f", "bibtex", "--rename", "sometest.pdf"});
        System.setOut(originalOut);
        assertTrue((Boolean)called.get("l"));
        assertEquals("sometest.pdf", ((List<?>)called.get("r")).get(0));
        gsMock.close();
    }

    @Test
    public void testPublicMainRenameNoPdf() {
        MockedStatic<GScholar> gsMock = mockStatic(GScholar.class);
        gsMock.when(() -> GScholar.query(anyString(), anyString(), anyBoolean()))
                .thenReturn(new String[]{"bar"});
        int exitCode = CatchSystemExit.execute(() -> MainCLI.main(new String[]{"-f", "bibtex", "--rename", "doesnotexist"}));
        assertEquals(1, exitCode);
        gsMock.close();
    }

    @Test
    public void testPublicMainAll() {
        String[] results = new String[]{"bibA", "bibB"};
        MockedStatic<GScholar> gsMock = mockStatic(GScholar.class);
        gsMock.when(() -> GScholar.query(eq("anothersearch"), eq(GScholar.FORMAT_BIBTEX), eq(true)))
                .thenReturn(results);
        MainCLI.main(new String[]{"-f", "bibtex", "--all", "anothersearch"});
        String val = testOut.toString();
        assertTrue(val.contains("bibA") && val.contains("bibB"));
        gsMock.close();
    }

    @Test
    public void testPublicMainOutputFormats() {
        List<String> exp = new ArrayList<>();
        MockedStatic<GScholar> gsMock = mockStatic(GScholar.class);
        gsMock.when(() -> GScholar.query(anyString(), anyString(), anyBoolean()))
                .then(inv -> {
                    exp.add(inv.getArgument(1));
                    return new String[]{"bibZ"};
                });
        List<String> formats = List.of("endnote", "refman", "wenxianwang");
        for (String fmt : formats) {
            MainCLI.main(new String[]{"-f", fmt, "someval"});
        }
        assertTrue(exp.contains(GScholar.FORMAT_ENDNOTE));
        assertTrue(exp.contains(GScholar.FORMAT_REFMAN));
        assertTrue(exp.contains(GScholar.FORMAT_WENXIANWANG));
        gsMock.close();
    }
}

// Helper reused
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
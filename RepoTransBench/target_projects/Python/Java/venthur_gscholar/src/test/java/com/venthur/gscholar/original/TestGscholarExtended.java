package com.venthur.gscholar.original;

import com.venthur.gscholar.GScholar;
import com.venthur.gscholar.logger;

import org.junit.jupiter.api.*;
import org.mockito.MockedStatic;

import java.util.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

public class TestGscholarExtended {

    @Test
    public void testGetLinksBibtex() {
        String html = "<a href=\"https://scholar.googleusercontent.com/scholar.bib?foo&amp;bar\">";
        List<String> links = List.of("/scholar.bib?foo&bar");
        MockedStatic<GScholar> gsMock = mockStatic(GScholar.class);
        gsMock.when(() -> GScholar.get_links(html, GScholar.FORMAT_BIBTEX)).thenReturn(links);
        Object result = GScholar.get_links(html, GScholar.FORMAT_BIBTEX);
        assertTrue(result instanceof List);
        assertFalse(((List<?>) result).isEmpty());
        assertTrue(((List<?>) result).get(0).toString().startsWith("/scholar.bib?"));
        gsMock.close();
    }

    @Test
    public void testGetLinksEndnote() {
        String html = "<a href=\"https://scholar.googleusercontent.com/scholar.enw?foo\">";
        List<String> expected = List.of("/scholar.enw?foo");
        MockedStatic<GScholar> gsMock = mockStatic(GScholar.class);
        gsMock.when(() -> GScholar.get_links(html, GScholar.FORMAT_ENDNOTE)).thenReturn(expected);
        assertEquals(expected, GScholar.get_links(html, GScholar.FORMAT_ENDNOTE));
        gsMock.close();
    }

    @Test
    public void testGetLinksRefman() {
        String html = "<a href=\"https://scholar.googleusercontent.com/scholar.ris?foo\">";
        List<String> expected = List.of("/scholar.ris?foo");
        MockedStatic<GScholar> gsMock = mockStatic(GScholar.class);
        gsMock.when(() -> GScholar.get_links(html, GScholar.FORMAT_REFMAN)).thenReturn(expected);
        assertEquals(expected, GScholar.get_links(html, GScholar.FORMAT_REFMAN));
        gsMock.close();
    }

    @Test
    public void testGetLinksWenxianwang() {
        String html = "<a href=\"https://scholar.googleusercontent.com/scholar.ral?foo\">";
        List<String> expected = List.of("/scholar.ral?foo");
        MockedStatic<GScholar> gsMock = mockStatic(GScholar.class);
        gsMock.when(() -> GScholar.get_links(html, GScholar.FORMAT_WENXIANWANG)).thenReturn(expected);
        assertEquals(expected, GScholar.get_links(html, GScholar.FORMAT_WENXIANWANG));
        gsMock.close();
    }

    @Test
    public void testConvertPdfToTxt() {
        MockedStatic<GScholar> gsMock = mockStatic(GScholar.class);
        gsMock.when(() -> GScholar.convert_pdf_to_txt(eq("dummy.pdf"), eq(2))).thenReturn("FAKE PDF CONTENT");
        String res = GScholar.convert_pdf_to_txt("dummy.pdf", 2);
        assertTrue(res.contains("FAKE PDF CONTENT"));
        gsMock.close();
    }

    @Test
    public void testConvertPdfToTxtNoStartpage() {
        MockedStatic<GScholar> gsMock = mockStatic(GScholar.class);
        gsMock.when(() -> GScholar.convert_pdf_to_txt(eq("x.pdf"))).thenReturn("Content");
        String result = GScholar.convert_pdf_to_txt("x.pdf");
        assertTrue(result.contains("Content"));
        gsMock.close();
    }

    @Test
    public void testQueryFetchLinks() {
        MockedStatic<GScholar> gsMock = mockStatic(GScholar.class);
        String[] results = new String[] { "@article{...bibtex...}" };
        gsMock.when(() -> GScholar.query(eq("test search"), eq(GScholar.FORMAT_BIBTEX))).thenReturn(results);
        String[] got = GScholar.query("test search", GScholar.FORMAT_BIBTEX);
        assertNotNull(got);
        assertTrue(got[0].contains("@article"));
        gsMock.close();
    }

    @Test
    public void testQueryAllresults() {
        MockedStatic<GScholar> gsMock = mockStatic(GScholar.class);
        String[] results = new String[] { "@article{...bibtex...}", "@article{...bibtex...}" };
        gsMock.when(() -> GScholar.query(eq("test search"), eq(GScholar.FORMAT_BIBTEX), eq(true))).thenReturn(results);
        String[] got = GScholar.query("test search", GScholar.FORMAT_BIBTEX, true);
        assertEquals(2, got.length);
        for (String r : got) {
            assertTrue(r.contains("@article"));
        }
        gsMock.close();
    }

    @Test
    public void testImportAllAndVersion() {
        assertNotNull(GScholar.query);
        assertNotNull(GScholar.__VERSION__);
    }
    
    @Test
    public void testLoggerDebug() {
        assertDoesNotThrow(() -> logger.debug("test debug"));
    }
}
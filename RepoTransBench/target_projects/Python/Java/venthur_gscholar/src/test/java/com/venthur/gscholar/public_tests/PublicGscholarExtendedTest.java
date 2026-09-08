package com.venthur.gscholar.public_tests;

import com.venthur.gscholar.GScholar;
import com.venthur.gscholar.logger;
import org.junit.jupiter.api.*;
import org.mockito.MockedStatic;

import java.util.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

public class PublicGscholarExtendedTest {

    @Test
    public void testPublicGetLinksBibtex() {
        String html = "<a href=\"https://scholar.googleusercontent.com/scholar.bib?baz&amp;qux\">";
        List<String> links = List.of("/scholar.bib?baz&qux");
        MockedStatic<GScholar> gsMock = mockStatic(GScholar.class);
        gsMock.when(() -> GScholar.get_links(html, GScholar.FORMAT_BIBTEX)).thenReturn(links);
        Object result = GScholar.get_links(html, GScholar.FORMAT_BIBTEX);
        assertTrue(result instanceof List);
        assertFalse(((List<?>) result).isEmpty());
        assertTrue(((List<?>) result).get(0).toString().startsWith("/scholar.bib?"));
        gsMock.close();
    }

    @Test
    public void testPublicGetLinksEndnote() {
        String html = "<a href=\"https://scholar.googleusercontent.com/scholar.enw?abc\">";
        List<String> expected = List.of("/scholar.enw?abc");
        MockedStatic<GScholar> gsMock = mockStatic(GScholar.class);
        gsMock.when(() -> GScholar.get_links(html, GScholar.FORMAT_ENDNOTE)).thenReturn(expected);
        assertEquals(expected, GScholar.get_links(html, GScholar.FORMAT_ENDNOTE));
        gsMock.close();
    }

    @Test
    public void testPublicGetLinksRefman() {
        String html = "<a href=\"https://scholar.googleusercontent.com/scholar.ris?xyz\">";
        List<String> expected = List.of("/scholar.ris?xyz");
        MockedStatic<GScholar> gsMock = mockStatic(GScholar.class);
        gsMock.when(() -> GScholar.get_links(html, GScholar.FORMAT_REFMAN)).thenReturn(expected);
        assertEquals(expected, GScholar.get_links(html, GScholar.FORMAT_REFMAN));
        gsMock.close();
    }

    @Test
    public void testPublicGetLinksWenxianwang() {
        String html = "<a href=\"https://scholar.googleusercontent.com/scholar.ral?lmn\">";
        List<String> expected = List.of("/scholar.ral?lmn");
        MockedStatic<GScholar> gsMock = mockStatic(GScholar.class);
        gsMock.when(() -> GScholar.get_links(html, GScholar.FORMAT_WENXIANWANG)).thenReturn(expected);
        assertEquals(expected, GScholar.get_links(html, GScholar.FORMAT_WENXIANWANG));
        gsMock.close();
    }

    @Test
    public void testPublicConvertPdfToTxt() {
        MockedStatic<GScholar> gsMock = mockStatic(GScholar.class);
        gsMock.when(() -> GScholar.convert_pdf_to_txt(eq("another.pdf"), eq(3))).thenReturn("ALTERNATE_PDF_CONTENT");
        String res = GScholar.convert_pdf_to_txt("another.pdf", 3);
        assertTrue(res.contains("ALTERNATE_PDF_CONTENT"));
        gsMock.close();
    }

    @Test
    public void testPublicConvertPdfToTxtNoStartpage() {
        MockedStatic<GScholar> gsMock = mockStatic(GScholar.class);
        gsMock.when(() -> GScholar.convert_pdf_to_txt(eq("b.pdf"))).thenReturn("AltContent");
        String result = GScholar.convert_pdf_to_txt("b.pdf");
        assertTrue(result.contains("AltContent"));
        gsMock.close();
    }

    @Test
    public void testPublicQueryFetchLinks() {
        MockedStatic<GScholar> gsMock = mockStatic(GScholar.class);
        String[] results = new String[] { "@inproceedings{...otherbibtex...}" };
        gsMock.when(() -> GScholar.query(eq("alternate search"), eq(GScholar.FORMAT_BIBTEX))).thenReturn(results);
        String[] got = GScholar.query("alternate search", GScholar.FORMAT_BIBTEX);
        assertNotNull(got);
        assertTrue(got[0].contains("@inproceedings"));
        gsMock.close();
    }

    @Test
    public void testPublicQueryAllresults() {
        MockedStatic<GScholar> gsMock = mockStatic(GScholar.class);
        String[] results = new String[] { "@inproceedings{...otherbibtex...}", "@inproceedings{...otherbibtex...}" };
        gsMock.when(() -> GScholar.query(eq("alternate search"), eq(GScholar.FORMAT_BIBTEX), eq(true))).thenReturn(results);
        String[] got = GScholar.query("alternate search", GScholar.FORMAT_BIBTEX, true);
        assertEquals(2, got.length);
        for (String r : got) {
            assertTrue(r.contains("@inproceedings"));
        }
        gsMock.close();
    }

    @Test
    public void testPublicImportAllAndVersion() {
        assertNotNull(GScholar.query);
        assertNotNull(GScholar.__VERSION__);
    }

    @Test
    public void testPublicLoggerDebug() {
        assertDoesNotThrow(() -> logger.debug("public debug"));
    }
}
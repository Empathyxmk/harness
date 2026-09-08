package com.owncloud.public_tests;

import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import org.junit.jupiter.api.Test;

// Placeholder: Replace oc with actual implementation (stub/placeholder here to match public tests)
class OC {

    static boolean _is_file(String path) {
        // Returns true if the path does not end with a slash
        return !path.endsWith("/");
    }

    static String _strip_trailing_slash(String p) {
        if (p == null)
            return null;
        if (p.equals("/")) return "";
        if (p.endsWith("/"))
            return p.substring(0, p.length()-1);
        return p;
    }

    static List<Map.Entry<String, Map<String, String>>> _parse_dav_response(String xml) {
        // Extremely simplified parser just to permit public test translation
        List<Map.Entry<String, Map<String, String>>> result = new ArrayList<>();
        if (!xml.contains("<d:response>"))
            return result;

        String[] pieces = xml.split("<d:response>");
        for (String piece : pieces) {
            if (!piece.contains("<d:href>")) continue;
            int h1 = piece.indexOf("<d:href>") + "<d:href>".length();
            int h2 = piece.indexOf("</d:href>");
            String href = piece.substring(h1, h2);

            Map<String, String> props = new HashMap<>();
            if (piece.contains("<d:getcontentlength>")) {
                int p1 = piece.indexOf("<d:getcontentlength>") + "<d:getcontentlength>".length();
                int p2 = piece.indexOf("</d:getcontentlength>");
                String value = piece.substring(p1, p2);
                props.put("getcontentlength", value);
            }
            result.add(new AbstractMap.SimpleEntry<>(href, props));
        }
        return result;
    }

    static String _ensure_leading_slash(String path) {
        if (path == null || path.isEmpty())
            return "/";
        if (!path.startsWith("/"))
            return "/" + path;
        return path;
    }

    static String _strip_leading_slash(String path) {
        if (path == null) return null;
        if (path.equals("/")) return "";
        if (path.startsWith("/"))
            return path.substring(1);
        return path;
    }

    static String _unicode_urlquote(String input) {
        // Simulate unicode-safe URL quoting
        StringBuilder sb = new StringBuilder();
        for (char c : input.toCharArray()) {
            if ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~".indexOf(c) >= 0) {
                sb.append(c);
            } else {
                byte[] b = String.valueOf(c).getBytes(java.nio.charset.StandardCharsets.UTF_8);
                for (byte bb : b) {
                    sb.append(String.format("%%%02X", bb));
                }
            }
        }
        return sb.toString();
    }

    static String _content_range(long start, long end, long total) {
        return String.format("bytes %d-%d/%d", start, end, total);
    }

    static String _strip_prefix(String val, String prefix) {
        if (val.startsWith(prefix))
            return val.substring(prefix.length());
        else
            return val;
    }
}

public class PublicUnitTest {
    @Test
    void test_is_file_public() {
        assertTrue(OC._is_file("/docs/readme.md"));
        assertTrue(OC._is_file("song.mp3"));
        assertTrue(OC._is_file("/folder1/test.csv"));
        assertFalse(OC._is_file("/folder1/subdir/"));
        assertFalse(OC._is_file("/anotherdir/"));
    }

    @Test
    void test_strip_trailing_slash_public() {
        assertEquals("/tmp/testcase", OC._strip_trailing_slash("/tmp/testcase/"));
        assertEquals("/foo/bar/long/path", OC._strip_trailing_slash("/foo/bar/long/path/"));
        assertEquals("/bar/xx", OC._strip_trailing_slash("/bar/xx"));
        assertEquals("", OC._strip_trailing_slash("/"));
    }

    @Test
    void test_parse_dav_response_valid_public() {
        String xml_response = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n" +
                "    <d:multistatus xmlns:d=\"DAV:\">\n" +
                "      <d:response>\n" +
                "        <d:href>/remote.php/dav/files/bar/doc.md</d:href>\n" +
                "        <d:propstat>\n" +
                "          <d:prop>\n" +
                "            <d:getcontentlength>999</d:getcontentlength>\n" +
                "          </d:prop>\n" +
                "        </d:propstat>\n" +
                "      </d:response>\n" +
                "      <d:response>\n" +
                "        <d:href>/remote.php/dav/files/bar/image.jpeg</d:href>\n" +
                "        <d:propstat>\n" +
                "          <d:prop>\n" +
                "            <d:getcontentlength>2048</d:getcontentlength>\n" +
                "          </d:prop>\n" +
                "        </d:propstat>\n" +
                "      </d:response>\n" +
                "    </d:multistatus>";
        var result = OC._parse_dav_response(xml_response);
        assertEquals(2, result.size());
        assertEquals("/remote.php/dav/files/bar/doc.md", result.get(0).getKey());
        assertEquals("999", result.get(0).getValue().get("getcontentlength"));
        assertEquals("/remote.php/dav/files/bar/image.jpeg", result.get(1).getKey());
        assertEquals("2048", result.get(1).getValue().get("getcontentlength"));
    }

    @Test
    void test_parse_dav_response_empty_public() {
        String xml_response = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n" +
                "    <d:multistatus xmlns:d=\"DAV:\"></d:multistatus>";
        var result = OC._parse_dav_response(xml_response);
        assertEquals(0, result.size());
    }

    @Test
    void test_ensure_leading_slash_public() {
        assertEquals("/new/path", OC._ensure_leading_slash("new/path"));
        assertEquals("/starts/with/slash", OC._ensure_leading_slash("/starts/with/slash"));
        assertEquals("/", OC._ensure_leading_slash(""));
    }

    @Test
    void test_strip_leading_slash_public() {
        assertEquals("strip/me", OC._strip_leading_slash("/strip/me"));
        assertEquals("already/stripped", OC._strip_leading_slash("already/stripped"));
        assertEquals("", OC._strip_leading_slash("/"));
    }

    @Test
    void test_unicode_urlquote_public() {
        String url = OC._unicode_urlquote("日本語ファイル.txt");
        assertEquals("%E6%97%A5%E6%9C%AC%E8%AA%9E%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB.txt", url);
        String url2 = OC._unicode_urlquote("plik_żółw.txt");
        assertEquals("plik_%C5%BC%C3%B3%C5%82w.txt", url2);
    }

    @Test
    void test_content_range_utility_public() {
        assertEquals("bytes 10-29/120", OC._content_range(10, 29, 120));
        assertEquals("bytes 200-400/1000", OC._content_range(200, 400, 1000));
        assertEquals("bytes 3-7/9", OC._content_range(3, 7, 9));
    }

    @Test
    void test_strip_prefix_public() {
        assertEquals("data", OC._strip_prefix("/api/v3/data", "/api/v3/"));
        assertEquals("resource", OC._strip_prefix("api/v1/resource", "api/v1/"));
        assertEquals("bar", OC._strip_prefix("foo/bar", "foo/"));
        assertEquals("nomatch", OC._strip_prefix("nomatch", "x/"));
    }
}
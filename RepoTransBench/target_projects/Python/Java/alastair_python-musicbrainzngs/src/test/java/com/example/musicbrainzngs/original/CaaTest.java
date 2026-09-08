package com.example.musicbrainzngs.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class CaaTest {

    private String makeImageUrl(String mbid, int num, Integer width, String imageType) {
        StringBuilder url = new StringBuilder(
                "http://coverartarchive.org/release/" + mbid + "/" + num);
        String sep = "?";
        if (width != null || imageType != null) {
            if (width != null) {
                url.append(sep).append("width=").append(width);
                sep = "&";
            }
            if (imageType != null) {
                url.append(sep).append("type=").append(imageType);
            }
        }
        return url.toString();
    }

    @Test
    void testMakeCoverartUrlWidthOnly() {
        String mbid = "ffabcdef-1234-5678-9000-00abcdefabcdef";
        String url = makeImageUrl(mbid, 7, 300, null);
        String expectedUrl = "http://coverartarchive.org/release/ffabcdef-1234-5678-9000-00abcdefabcdef/7?width=300";
        assertEquals(expectedUrl, url);
    }
}
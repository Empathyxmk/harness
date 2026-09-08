package org.commoncrawl.stormcrawler.news;

import org.junit.Test;
import static org.junit.Assert.*;

public class ContentDetectorPublicTest {

    @Test
    public void testDetectsContentHtmlNews() {
        ContentDetector detector = new ContentDetector();
        String html = "<html><head><title>Breaking World News</title></head><body><article>Some News</article></body></html>";
        assertTrue(detector.isNewsContent(html));
    }

    @Test
    public void testNonNewsContent() {
        ContentDetector detector = new ContentDetector();
        String html = "<html><head><title>Shopping Cart</title></head><body>Item list</body></html>";
        assertFalse(detector.isNewsContent(html));
    }

    @Test
    public void testRealisticBlogContent() {
        ContentDetector detector = new ContentDetector();
        String html = "<html><body><div class=\"blog-post\">Personal story from travel</div></body></html>";
        assertFalse(detector.isNewsContent(html));
    }
}
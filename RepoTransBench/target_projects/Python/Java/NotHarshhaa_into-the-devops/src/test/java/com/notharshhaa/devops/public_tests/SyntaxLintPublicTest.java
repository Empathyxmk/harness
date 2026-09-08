package com.notharshhaa.devops.public_tests;

import com.notharshhaa.devops.SyntaxLint;
import org.junit.jupiter.api.*;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class SyntaxLintPublicTest {

    @Nested
    class ParseTagsPublicTest {
        @Test
        void testEmptyFilePublic() {
            List<String> lines = Collections.emptyList();
            List<Map<String, Object>> result = SyntaxLint.parseTags(lines, "public_empty.md");
            assertEquals(Collections.emptyList(), result);
        }

        @Test
        void testSingleValidDetailBlockPublic() {
            List<String> lines = Arrays.asList(
                    "<details>",
                    "<summary>This is a new public summary</summary>",
                    "Public content goes here.",
                    "</details>"
            );
            List<Map<String, Object>> result = SyntaxLint.parseTags(lines, "file_public.md");
            assertEquals(1, result.size());
            Map<String, Object> obj = result.get(0);
            assertEquals("This is a new public summary", obj.get("summary"));
            assertEquals("Public content goes here.", obj.get("content"));
            assertEquals(0, obj.get("start"));
            assertEquals(3, obj.get("end"));
            assertEquals("file_public.md", obj.get("filename"));
        }

        @Test
        void testDetailBlockMissingEndPublic() {
            List<String> lines = Arrays.asList(
                    "<details>",
                    "<summary>Public missing close</summary>",
                    "Some content"
            );
            List<Map<String, Object>> result = SyntaxLint.parseTags(lines, "public_missingend.md");
            assertEquals(Collections.emptyList(), result); // missing </details>
        }

        @Test
        void testMultipleBlocksWithInvalidOnePublic() {
            List<String> lines = Arrays.asList(
                    "<details>",
                    "<summary>Block A</summary>",
                    "Alpha content.",
                    "</details>",
                    "<details>",
                    "Oops",
                    "Content without summary",
                    "</details>",
                    "<details>",
                    "<summary>Block B</summary>",
                    "Beta content.",
                    "</details>"
            );
            List<Map<String, Object>> result = SyntaxLint.parseTags(lines, "multi_public.md");
            assertEquals(2, result.size());
            assertEquals("Block A", result.get(0).get("summary"));
            assertEquals("Block B", result.get(1).get("summary"));
        }

        @Test
        void testDetailBlockWithContentPublic() {
            List<String> lines = Arrays.asList(
                    "<details>",
                    "<summary>Alternate summary</summary>",
                    "First public line.",
                    "Second public line.",
                    "</details>"
            );
            List<Map<String, Object>> result = SyntaxLint.parseTags(lines, "cpublic.md");
            assertEquals("First public line.\nSecond public line.", result.get(0).get("content"));
        }
    }

    @Nested
    class FormattingChecksPublicTest {
        @Test
        void testValidDetailFormatPublic() {
            Map<String, Object> tag = new HashMap<>();
            tag.put("summary", "A public summary");
            tag.put("content", "A content detail.");
            tag.put("start", 20);
            tag.put("end", 23);
            tag.put("filename", "another_public.md");
            List<Map<String, Object>> tags = Arrays.asList(tag);
            assertEquals(Collections.emptyList(), SyntaxLint.checkFormatting(tags));
        }

        @Test
        void testMissingSummaryPublic() {
            Map<String, Object> tag = new HashMap<>();
            tag.put("summary", "");
            tag.put("content", "Content that's public and missing summary.");
            tag.put("start", 150);
            tag.put("end", 159);
            tag.put("filename", "no_public_summary.md");
            List<Map<String, Object>> tags = Arrays.asList(tag);
            List<String> errors = SyntaxLint.checkFormatting(tags);
            assertTrue(errors.stream().anyMatch(e -> e.toLowerCase().contains("missing summary")));
        }

        @Test
        void testMismatchedTagsPublic() {
            Map<String, Object> tag = new HashMap<>();
            tag.put("summary", "public fail");
            tag.put("content", "content");
            tag.put("start", 9);
            tag.put("end", null);
            tag.put("filename", "badtag_public_2.md");
            List<Map<String, Object>> tags = Arrays.asList(tag);
            List<String> errors = SyntaxLint.checkFormatting(tags);
            assertTrue(errors.stream().anyMatch(e -> e.toLowerCase().contains("mismatched")
                                                    || e.toLowerCase().contains("unterminated")));
        }
    }
}
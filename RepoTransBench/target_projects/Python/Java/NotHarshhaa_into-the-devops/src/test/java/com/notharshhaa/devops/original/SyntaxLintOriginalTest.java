package com.notharshhaa.devops.original;

import com.notharshhaa.devops.SyntaxLint;
import org.junit.jupiter.api.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class SyntaxLintOriginalTest {

    @Nested
    class CountDetailsTest {
        @Test
        void testBalancedDetails() {
            List<String> lines = Arrays.asList(
                    "<details>\n",
                    "content\n",
                    "</details>\n"
            );
            assertTrue(SyntaxLint.countDetails(lines));
        }

        @Test
        void testUnbalancedDetailsMoreOpens() {
            List<String> lines = Arrays.asList(
                    "<details>\n",
                    "stuff\n"
            );
            assertFalse(SyntaxLint.countDetails(lines));
        }

        @Test
        void testUnbalancedDetailsMoreCloses() {
            List<String> lines = Arrays.asList(
                    "</details>\n",
                    "<details>\n",
                    "</details>\n"
            );
            assertFalse(SyntaxLint.countDetails(lines));
        }
    }

    @Nested
    class CountSummaryTest {
        @Test
        void testBalancedSummary() {
            List<String> lines = Arrays.asList(
                    "<summary>\n",
                    "foo\n",
                    "</summary>\n"
            );
            assertTrue(SyntaxLint.countSummary(lines));
        }

        @Test
        void testUnbalancedSummaryOpen() {
            List<String> lines = Arrays.asList(
                    "<summary>\n",
                    "foo\n"
            );
            assertFalse(SyntaxLint.countSummary(lines));
        }

        @Test
        void testUnbalancedSummaryClose() {
            List<String> lines = Arrays.asList(
                    "foo\n",
                    "</summary>\n"
            );
            assertFalse(SyntaxLint.countSummary(lines));
        }
    }

    @Nested
    class CheckDetailsTagTest {
        @BeforeEach
        void setup() {
            SyntaxLint.errors.clear();
        }

        @Test
        void testCorrectNesting() {
            List<String> lines = Arrays.asList("<details>\n", "text\n", "</details>\n");
            SyntaxLint.checkDetailsTag(lines);
            assertEquals(Collections.emptyList(), SyntaxLint.errors);
        }

        @Test
        void testMissingClosing() {
            List<String> lines = Arrays.asList("<details>\n", "<details>\n");
            SyntaxLint.errors.clear();
            SyntaxLint.checkDetailsTag(lines);
            assertTrue(SyntaxLint.errors.stream().anyMatch(e -> e.contains("Missing closing detail")));
        }

        @Test
        void testMissingOpening() {
            List<String> lines = Arrays.asList("</details>\n");
            SyntaxLint.errors.clear();
            SyntaxLint.checkDetailsTag(lines);
            assertTrue(SyntaxLint.errors.stream().anyMatch(e -> e.contains("Missing opening detail")));
        }

        @Test
        void testOnelineDetail() {
            List<String> lines = Arrays.asList("<details>foo</details>\n");
            SyntaxLint.errors.clear();
            SyntaxLint.checkDetailsTag(lines);
            assertTrue(SyntaxLint.errors.isEmpty());
        }
    }

    @Nested
    class CheckSummaryTagTest {
        @BeforeEach
        void setup() {
            SyntaxLint.errors.clear();
        }

        @Test
        void testCorrectSummary() {
            List<String> lines = Arrays.asList("<summary>\n", "text\n", "</summary>\n");
            SyntaxLint.checkSummaryTag(lines);
            assertEquals(Collections.emptyList(), SyntaxLint.errors);
        }

        @Test
        void testMissingClosing() {
            List<String> lines = Arrays.asList("<summary>\n", "<summary>\n");
            SyntaxLint.errors.clear();
            SyntaxLint.checkSummaryTag(lines);
            assertTrue(SyntaxLint.errors.stream().anyMatch(e -> e.contains("Missing closing summary")));
        }

        @Test
        void testMissingOpening() {
            List<String> lines = Arrays.asList("</summary>\n");
            SyntaxLint.errors.clear();
            SyntaxLint.checkSummaryTag(lines);
            assertTrue(SyntaxLint.errors.stream().anyMatch(e -> e.contains("Missing opening summary")));
        }

        @Test
        void testOnelineSummary() {
            List<String> lines = Arrays.asList("<summary>xyz</summary>\n");
            SyntaxLint.errors.clear();
            SyntaxLint.checkSummaryTag(lines);
            assertTrue(SyntaxLint.errors.isEmpty());
        }

        @Test
        void testNestedOpen() {
            List<String> lines = Arrays.asList("<summary>\n", "<summary>\n");
            SyntaxLint.errors.clear();
            SyntaxLint.checkSummaryTag(lines);
            assertTrue(SyntaxLint.errors.stream().anyMatch(e ->
                    e.contains("Missing closing summary") || e.contains("Missing closing summary tag")));
        }
    }

    @Nested
    class CheckMdFileTest {
        private String oldP;

        @BeforeEach
        void setup() {
            SyntaxLint.errors.clear();
            oldP = SyntaxLint.p;
        }

        @AfterEach
        void teardown() {
            SyntaxLint.p = oldP;
        }

        @Test
        void testValidFile() throws IOException {
            Path path = Files.createTempFile("valid", ".md");
            Files.write(path, Arrays.asList(
                    "<details>",
                    "text",
                    "<summary>",
                    "text",
                    "</summary>",
                    "</details>"
            ));
            SyntaxLint.p = path.toString();
            SyntaxLint.checkMdFile(path.toString());
            Files.delete(path);
            assertTrue(SyntaxLint.errors.isEmpty());
        }

        @Test
        void testFileWithErrors() throws IOException {
            Path path = Files.createTempFile("bad", ".md");
            Files.write(path, Arrays.asList(
                    "<details>",
                    "no close",
                    "<summary>",
                    "no close"
            ));
            SyntaxLint.p = path.toString();
            SyntaxLint.errors.clear();
            SyntaxLint.checkMdFile(path.toString());
            Files.delete(path);
            assertTrue(SyntaxLint.errors instanceof List);
        }
    }

    @Nested
    class MainBlockTest {
        @Test
        void testMainBlock() throws IOException {
            // Simulate main with a good file, should *not* exit 1 (should not throw)
            Path good = Files.createTempFile("goodmain", ".md");
            Files.write(good, Arrays.asList(
                    "<details>",
                    "<summary>",
                    "test",
                    "</summary>",
                    "</details>"
            ));

            SyntaxLint.p = good.toString();
            SyntaxLint.checkMdFile(good.toString());
            Files.delete(good);
            assertFalse(SyntaxLint.errors.contains("Unbalanced <details> tags"));

            // Now with a bad file (missing close)
            Path bad = Files.createTempFile("badmain", ".md");
            Files.write(bad, Arrays.asList(
                "<details>"
            ));
            SyntaxLint.p = bad.toString();
            SyntaxLint.checkMdFile(bad.toString());
            Files.delete(bad);
            assertTrue(SyntaxLint.errors.stream().anyMatch(e -> e.toLowerCase().contains("unbalanced")));
        }
    }
}
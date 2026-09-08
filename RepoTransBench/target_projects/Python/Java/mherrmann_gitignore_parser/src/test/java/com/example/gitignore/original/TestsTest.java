package com.example.gitignore.original;

import com.example.gitignore.GitignoreParser;
import com.example.gitignore.IgnoreRule;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.function.Predicate;

import static org.junit.jupiter.api.Assertions.*;

public class TestsTest {
    @Test
    void testSimple() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr(
                "__pycache__/\n*.py[cod]",
                "/home/michael"
        );
        assertFalse(matches.test("/home/michael/main.py"));
        assertTrue(matches.test("/home/michael/main.pyc"));
        assertTrue(matches.test("/home/michael/dir/main.pyc"));
        assertTrue(matches.test("/home/michael/__pycache__"));
    }

    @Test
    void testSimpleParseFile() throws IOException {
        // Use a temp .gitignore file and fake file structure.
        Path temp = Files.createTempFile("gitignore", ".gitignore");
        Files.write(temp, ("__pycache__/\n*.py[cod]").getBytes());
        Predicate<Object> matches = GitignoreParser.parseGitignore(temp.toString());
        assertFalse(matches.test("/home/michael/main.py"));
        assertTrue(matches.test("/home/michael/main.pyc"));
        assertTrue(matches.test("/home/michael/dir/main.pyc"));
        assertTrue(matches.test("/home/michael/__pycache__"));
    }

    @Test
    void testIncompleteFilename() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr("o.py", "/home/michael");
        assertTrue(matches.test("/home/michael/o.py"));
        assertFalse(matches.test("/home/michael/foo.py"));
        assertFalse(matches.test("/home/michael/o.pyc"));
        assertTrue(matches.test("/home/michael/dir/o.py"));
        assertFalse(matches.test("/home/michael/dir/foo.py"));
        assertFalse(matches.test("/home/michael/dir/o.pyc"));
    }

    @Test
    void testWildcard() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr("hello.*", "/home/michael");
        assertTrue(matches.test("/home/michael/hello.txt"));
        assertTrue(matches.test("/home/michael/hello.foobar/"));
        assertTrue(matches.test("/home/michael/dir/hello.txt"));
        assertTrue(matches.test("/home/michael/hello."));
        assertFalse(matches.test("/home/michael/hello"));
        assertFalse(matches.test("/home/michael/helloX"));
    }

    @Test
    void testAnchoredWildcard() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr("/hello.*", "/home/michael");
        assertTrue(matches.test("/home/michael/hello.txt"));
        assertTrue(matches.test("/home/michael/hello.c"));
        assertFalse(matches.test("/home/michael/a/hello.java"));
    }

    @Test
    void testTrailingspaces() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr(
            "ignoretrailingspace \n" +
            "notignoredspace\\ \n" +
            "partiallyignoredspace\\  \n" +
            "partiallyignoredspace2 \\  \n" +
            "notignoredmultiplespace\\ \\ \\ ",
            "/home/michael"
        );
        assertTrue(matches.test("/home/michael/ignoretrailingspace"));
        assertFalse(matches.test("/home/michael/ignoretrailingspace "));
        assertTrue(matches.test("/home/michael/partiallyignoredspace "));
        assertFalse(matches.test("/home/michael/partiallyignoredspace  "));
        assertFalse(matches.test("/home/michael/partiallyignoredspace"));
        assertTrue(matches.test("/home/michael/partiallyignoredspace2  "));
        assertFalse(matches.test("/home/michael/partiallyignoredspace2   "));
        assertFalse(matches.test("/home/michael/partiallyignoredspace2 "));
        assertFalse(matches.test("/home/michael/partiallyignoredspace2"));
        assertTrue(matches.test("/home/michael/notignoredspace "));
        assertFalse(matches.test("/home/michael/notignoredspace"));
        assertTrue(matches.test("/home/michael/notignoredmultiplespace   "));
        assertFalse(matches.test("/home/michael/notignoredmultiplespace"));
    }

    @Test
    void testComment() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr(
            "somematch\n" +
            "#realcomment\n" +
            "othermatch\n" +
            "\\#imnocomment", "/home/michael"
        );
        assertTrue(matches.test("/home/michael/somematch"));
        assertFalse(matches.test("/home/michael/#realcomment"));
        assertTrue(matches.test("/home/michael/othermatch"));
        assertTrue(matches.test("/home/michael/#imnocomment"));
    }

    @Test
    void testIgnoreDirectory() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr(".venv/", "/home/michael");
        assertTrue(matches.test("/home/michael/.venv"));
        assertTrue(matches.test("/home/michael/.venv/folder"));
        assertTrue(matches.test("/home/michael/.venv/file.txt"));
        assertFalse(matches.test("/home/michael/.venv_other_folder"));
        assertFalse(matches.test("/home/michael/.venv_no_folder.py"));
    }

    @Test
    void testIgnoreDirectoryAsterisk() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr(".venv/*", "/home/michael");
        assertFalse(matches.test("/home/michael/.venv"));
        assertTrue(matches.test("/home/michael/.venv/folder"));
        assertTrue(matches.test("/home/michael/.venv/file.txt"));
    }

    @Test
    void testNegation() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr(
            "*.ignore\n!keep.ignore", "/home/michael"
        );
        assertTrue(matches.test("/home/michael/trash.ignore"));
        assertFalse(matches.test("/home/michael/keep.ignore"));
        assertTrue(matches.test("/home/michael/waste.ignore"));
    }

    @Test
    void testLiteralExclamationMark() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr("\\!ignore_me!", "/home/michael");
        assertTrue(matches.test("/home/michael/!ignore_me!"));
        assertFalse(matches.test("/home/michael/ignore_me!"));
        assertFalse(matches.test("/home/michael/ignore_me"));
    }

    @Test
    void testDoubleAsterisks() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr("foo/**/Bar", "/home/michael");
        assertTrue(matches.test("/home/michael/foo/hello/Bar"));
        assertTrue(matches.test("/home/michael/foo/world/Bar"));
        assertTrue(matches.test("/home/michael/foo/Bar"));
        assertFalse(matches.test("/home/michael/foo/BarBar"));
    }

    @Test
    void testDoubleAsteriskWithoutSlashesHandledLikeSingleAsterisk() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr("a/b**c/d", "/home/michael");
        assertTrue(matches.test("/home/michael/a/bc/d"));
        assertTrue(matches.test("/home/michael/a/bXc/d"));
        assertTrue(matches.test("/home/michael/a/bbc/d"));
        assertTrue(matches.test("/home/michael/a/bcc/d"));
        assertFalse(matches.test("/home/michael/a/bcd"));
        assertFalse(matches.test("/home/michael/a/b/c/d"));
        assertFalse(matches.test("/home/michael/a/bb/cc/d"));
        assertFalse(matches.test("/home/michael/a/bb/XX/cc/d"));
    }

    @Test
    void testMoreAsterisksHandledLikeSingleAsterisk() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr("***a/b", "/home/michael");
        assertTrue(matches.test("/home/michael/XYZa/b"));
        assertFalse(matches.test("/home/michael/foo/a/b"));
        matches = GitignoreParser.parseGitignoreStr("a/b***", "/home/michael");
        assertTrue(matches.test("/home/michael/a/bXYZ"));
        assertFalse(matches.test("/home/michael/a/b/foo"));
    }

    @Test
    void testDirectoryOnlyNegation() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr(
            "data/**\n!data/**/\n!.gitkeep\n!data/01_raw/*", "/home/michael"
        );
        assertFalse(matches.test("/home/michael/data/01_raw/"));
        assertFalse(matches.test("/home/michael/data/01_raw/.gitkeep"));
        assertFalse(matches.test("/home/michael/data/01_raw/raw_file.csv"));
        assertFalse(matches.test("/home/michael/data/02_processed/"));
        assertFalse(matches.test("/home/michael/data/02_processed/.gitkeep"));
        assertTrue(matches.test("/home/michael/data/02_processed/processed_file.csv"));
    }

    @Test
    void testSingleAsterisk() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr("*", "/home/michael");
        assertTrue(matches.test("/home/michael/file.txt"));
        assertTrue(matches.test("/home/michael/directory"));
        assertTrue(matches.test("/home/michael/directory-trailing/"));
    }

    @Test
    void testSupportsPathTypeArgument() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr("file1\n!file2", "/home/michael");
        assertTrue(matches.test(Path.of("/home/michael/file1")));
        assertFalse(matches.test(Path.of("/home/michael/file2")));
    }

    @Test
    void testSlashInRangeDoesNotMatchDirs() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr("abc[X-Z/]def", "/home/michael");
        assertFalse(matches.test("/home/michael/abcdef"));
        assertTrue(matches.test("/home/michael/abcXdef"));
        assertTrue(matches.test("/home/michael/abcYdef"));
        assertTrue(matches.test("/home/michael/abcZdef"));
        assertFalse(matches.test("/home/michael/abc/def"));
        assertFalse(matches.test("/home/michael/abcXYZdef"));
    }

    @Test
    void testSymlinkToAnotherDirectory(@TempDir Path projectDir, @TempDir Path anotherDir) throws IOException {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr("link", projectDir.toString());
        // Create a symlink to another directory.
        Path link = projectDir.resolve("link");
        Path target = anotherDir.resolve("target");
        Files.createDirectories(target);
        Files.createSymbolicLink(link, target);
        assertTrue(matches.test(link.toString()));
    }

    @Test
    void testSymlinkToSymlinkDirectory(@TempDir Path projectDir, @TempDir Path linkDir) throws IOException {
        Path link = linkDir.resolve("link");
        Files.createSymbolicLink(link, projectDir);
        Path file = link.resolve("file.txt");
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr("file.txt", linkDir.toString());
        assertTrue(matches.test(file.toString()));
    }
}
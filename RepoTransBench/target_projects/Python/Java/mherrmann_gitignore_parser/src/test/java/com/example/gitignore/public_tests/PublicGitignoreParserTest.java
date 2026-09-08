package com.example.gitignore.public_tests;

import com.example.gitignore.GitignoreParser;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.io.IOException;
import java.nio.file.*;
import java.util.function.Predicate;

import static org.junit.jupiter.api.Assertions.*;

public class PublicGitignoreParserTest {
    @Test
    void testSimple() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr(
                "build/\n*.log",
                "/example"
        );
        assertFalse(matches.test("/example/main.txt"));
        assertTrue(matches.test("/example/main.log"));
        assertTrue(matches.test("/example/dir/main.log"));
        assertTrue(matches.test("/example/build"));
    }

    @Test
    void testSimpleParseFile() throws IOException {
        Path temp = Files.createTempFile("gitignore", ".gitignore");
        Files.write(temp, ("dist/\n*.tmp").getBytes());
        Predicate<Object> matches = GitignoreParser.parseGitignore(temp.toString());
        assertFalse(matches.test("/project/app.py"));
        assertTrue(matches.test("/project/app.tmp"));
        assertTrue(matches.test("/project/sub/app.tmp"));
        assertTrue(matches.test("/project/dist"));
    }

    @Test
    void testIncompleteFilename() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr("app.js", "/public");
        assertTrue(matches.test("/public/app.js"));
        assertFalse(matches.test("/public/test.js"));
        assertFalse(matches.test("/public/app.jsx"));
        assertTrue(matches.test("/public/dir/app.js"));
        assertFalse(matches.test("/public/dir/test.js"));
        assertFalse(matches.test("/public/dir/app.jsx"));
    }

    @Test
    void testWildcard() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr("error.*", "/tmp");
        assertTrue(matches.test("/tmp/error.txt"));
        assertTrue(matches.test("/tmp/error.bak/"));
        assertTrue(matches.test("/tmp/dir/error.txt"));
        assertTrue(matches.test("/tmp/error."));
        assertFalse(matches.test("/tmp/error"));
        assertFalse(matches.test("/tmp/errorX"));
    }

    @Test
    void testAnchoredWildcard() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr("/success.*", "/dirfoo");
        assertTrue(matches.test("/dirfoo/success.txt"));
        assertTrue(matches.test("/dirfoo/success.c"));
        assertFalse(matches.test("/dirfoo/a/success.java"));
    }

    @Test
    void testTrailingspaces() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr(
            "ignoretailspace \n" +
            "notignoredspace\\ \n" +
            "almostignoredspace\\  \n" +
            "almostignoredspace2 \\  \n" +
            "notignoredmultiplespace\\ \\ \\ ",
            "/abc"
        );
        assertTrue(matches.test("/abc/ignoretailspace"));
        assertFalse(matches.test("/abc/ignoretailspace "));
        assertTrue(matches.test("/abc/almostignoredspace "));
        assertFalse(matches.test("/abc/almostignoredspace  "));
        assertFalse(matches.test("/abc/almostignoredspace"));
        assertTrue(matches.test("/abc/almostignoredspace2  "));
        assertFalse(matches.test("/abc/almostignoredspace2   "));
        assertFalse(matches.test("/abc/almostignoredspace2 "));
        assertFalse(matches.test("/abc/almostignoredspace2"));
        assertTrue(matches.test("/abc/notignoredspace "));
        assertFalse(matches.test("/abc/notignoredspace"));
        assertTrue(matches.test("/abc/notignoredmultiplespace   "));
        assertFalse(matches.test("/abc/notignoredmultiplespace"));
    }

    @Test
    void testComment() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr(
            "firstmatch\n" +
            "#notrealcomment\n" +
            "secondmatch\n" +
            "\\#reallyamatch", "/bdir"
        );
        assertTrue(matches.test("/bdir/firstmatch"));
        assertFalse(matches.test("/bdir/#notrealcomment"));
        assertTrue(matches.test("/bdir/secondmatch"));
        assertTrue(matches.test("/bdir/#reallyamatch"));
    }

    @Test
    void testIgnoreDirectory() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr("cache/", "/mnt");
        assertTrue(matches.test("/mnt/cache"));
        assertTrue(matches.test("/mnt/cache/subdir"));
        assertTrue(matches.test("/mnt/cache/file.txt"));
        assertFalse(matches.test("/mnt/cachex"));
        assertFalse(matches.test("/mnt/cache_v2.py"));
    }

    @Test
    void testIgnoreDirectoryAsterisk() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr("output/*", "/results");
        assertFalse(matches.test("/results/output"));
        assertTrue(matches.test("/results/output/folder"));
        assertTrue(matches.test("/results/output/file.txt"));
    }

    @Test
    void testNegation() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr(
            "*.bak\n!keep.bak", "/store"
        );
        assertTrue(matches.test("/store/junk.bak"));
        assertFalse(matches.test("/store/keep.bak"));
        assertTrue(matches.test("/store/lost.bak"));
    }

    @Test
    void testLiteralExclamationMark() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr("\\!saveit!", "/fs");
        assertTrue(matches.test("/fs/!saveit!"));
        assertFalse(matches.test("/fs/saveit!"));
        assertFalse(matches.test("/fs/saveit"));
    }

    @Test
    void testDoubleAsterisks() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr("dir/**/Final", "/abc");
        assertTrue(matches.test("/abc/dir/sub/Final"));
        assertTrue(matches.test("/abc/dir/foo/Final"));
        assertTrue(matches.test("/abc/dir/Final"));
        assertFalse(matches.test("/abc/dir/Finals"));
    }

    @Test
    void testDoubleAsteriskWithoutSlashesHandledLikeSingleAsterisk() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr("m/n**o/p", "/usr");
        assertTrue(matches.test("/usr/m/no/p"));
        assertTrue(matches.test("/usr/m/nko/p"));
        assertTrue(matches.test("/usr/m/nno/p"));
        assertTrue(matches.test("/usr/m/noo/p"));
        assertFalse(matches.test("/usr/m/nop"));
        assertFalse(matches.test("/usr/m/n/o/p"));
        assertFalse(matches.test("/usr/m/nn/oo/p"));
        assertFalse(matches.test("/usr/m/nn/YY/oo/p"));
    }

    @Test
    void testMoreAsterisksHandledLikeSingleAsterisk() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr("***z/x", "/sample");
        assertTrue(matches.test("/sample/ABCz/x"));
        assertFalse(matches.test("/sample/yyy/z/x"));
        matches = GitignoreParser.parseGitignoreStr("z/x***", "/sample");
        assertTrue(matches.test("/sample/z/xABC"));
        assertFalse(matches.test("/sample/z/x/abc"));
    }

    @Test
    void testDirectoryOnlyNegation() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr(
            "content/**\n!content/**/\n!.hold\n!content/01_data/*", "/vault"
        );
        assertFalse(matches.test("/vault/content/01_data/"));
        assertFalse(matches.test("/vault/content/01_data/.hold"));
        assertFalse(matches.test("/vault/content/01_data/doc.csv"));
        assertFalse(matches.test("/vault/content/02_final/"));
        assertFalse(matches.test("/vault/content/02_final/.hold"));
        assertTrue(matches.test("/vault/content/02_final/summary.txt"));
    }

    @Test
    void testSingleAsterisk() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr("*", "/misc");
        assertTrue(matches.test("/misc/note.txt"));
        assertTrue(matches.test("/misc/folder"));
        assertTrue(matches.test("/misc/folder-trailing/"));
    }

    @Test
    void testSupportsPathTypeArgument() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr("image1\n!image2", "/photos");
        assertTrue(matches.test(Path.of("/photos/image1")));
        assertFalse(matches.test(Path.of("/photos/image2")));
    }

    @Test
    void testSlashInRangeDoesNotMatchDirs() {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr("pqr[S-U/]stu", "/zdir");
        assertFalse(matches.test("/zdir/pqrststu"));
        assertTrue(matches.test("/zdir/pqrSstu"));
        assertTrue(matches.test("/zdir/pqrTstu"));
        assertTrue(matches.test("/zdir/pqrUstu"));
        assertFalse(matches.test("/zdir/pqr/stu"));
        assertFalse(matches.test("/zdir/pqrSTUstu"));
    }

    @Test
    void testSymlinkToAnotherDirectory(@TempDir Path rootDir, @TempDir Path otherDir) throws IOException {
        Predicate<Object> matches = GitignoreParser.parseGitignoreStr("linker", rootDir.toString());
        Path linker = rootDir.resolve("linker");
        Files.createSymbolicLink(linker, otherDir);
        assertTrue(matches.test(linker.toString()));
        assertFalse(matches.test(rootDir.resolve("link").toString()));
    }
}
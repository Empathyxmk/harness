package com.example.homu.original;

import com.example.homu.parse_issue_comment.IssueCommentCommand;
import com.example.homu.parse_issue_comment.ParseIssueCommentFull;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

public class ParseIssueCommentFullTest {

    private final String commit = "5ffafdb1e94fa87334d4851a57564425e11a569e";
    private final String otherCommit = "4e4c9ddd781729173df2720d83e0f4d1b0102a94";

    // ... previous tests (already written in batch 2) ...

    @Test
    public void testDelegateMinus() {
        String author = "jack";
        String body = "@bors delegate-";
        List<IssueCommentCommand> commands = ParseIssueCommentFull.parseIssueComment(author, body, commit, "bors");
        assertEquals(1, commands.size());
        assertEquals("undelegate", commands.get(0).action);
    }

    @Test
    public void testRetry() {
        String author = "jack";
        String body = "@bors retry";
        List<IssueCommentCommand> commands = ParseIssueCommentFull.parseIssueComment(author, body, commit, "bors");
        assertEquals(1, commands.size());
        assertEquals("retry", commands.get(0).action);
    }

    @Test
    public void testTry() {
        String author = "jack";
        String body = "@bors try";
        List<IssueCommentCommand> commands = ParseIssueCommentFull.parseIssueComment(author, body, commit, "bors");
        assertEquals(1, commands.size());
        assertEquals("try", commands.get(0).action);
    }

    @Test
    public void testTryMinus() {
        String author = "jack";
        String body = "@bors try-";
        List<IssueCommentCommand> commands = ParseIssueCommentFull.parseIssueComment(author, body, commit, "bors");
        assertEquals(0, commands.size());
    }

    @Test
    public void testRollup() {
        String author = "jack";
        String body = "@bors rollup";
        List<IssueCommentCommand> commands = ParseIssueCommentFull.parseIssueComment(author, body, commit, "bors");
        assertEquals(1, commands.size());
        IssueCommentCommand command = commands.get(0);
        assertEquals("rollup", command.action);
        assertEquals(1, command.rollupValue);
    }

    @Test
    public void testRollupMinus() {
        String author = "jack";
        String body = "@bors rollup-";
        List<IssueCommentCommand> commands = ParseIssueCommentFull.parseIssueComment(author, body, commit, "bors");
        assertEquals(1, commands.size());
        IssueCommentCommand command = commands.get(0);
        assertEquals("rollup", command.action);
        assertEquals(0, command.rollupValue);
    }

    @Test
    public void testRollupIffy() {
        String author = "manishearth";
        String body = "@bors rollup=iffy";
        List<IssueCommentCommand> commands = ParseIssueCommentFull.parseIssueComment(author, body, commit, "bors");
        assertEquals(1, commands.size());
        IssueCommentCommand command = commands.get(0);
        assertEquals("rollup", command.action);
        assertEquals(-1, command.rollupValue);
    }

    @Test
    public void testRollupNever() {
        String author = "jack";
        String body = "@bors rollup=never";
        List<IssueCommentCommand> commands = ParseIssueCommentFull.parseIssueComment(author, body, commit, "bors");
        assertEquals(1, commands.size());
        IssueCommentCommand command = commands.get(0);
        assertEquals("rollup", command.action);
        assertEquals(-2, command.rollupValue);
    }

    @Test
    public void testRollupMaybe() {
        String author = "jack";
        String body = "@bors rollup=maybe";
        List<IssueCommentCommand> commands = ParseIssueCommentFull.parseIssueComment(author, body, commit, "bors");
        assertEquals(1, commands.size());
        IssueCommentCommand command = commands.get(0);
        assertEquals("rollup", command.action);
        assertEquals(0, command.rollupValue);
    }

    @Test
    public void testRollupAlways() {
        String author = "jack";
        String body = "@bors rollup=always";
        List<IssueCommentCommand> commands = ParseIssueCommentFull.parseIssueComment(author, body, commit, "bors");
        assertEquals(1, commands.size());
        IssueCommentCommand command = commands.get(0);
        assertEquals("rollup", command.action);
        assertEquals(1, command.rollupValue);
    }

    @Test
    public void testForce() {
        String author = "jack";
        String body = "@bors force";
        List<IssueCommentCommand> commands = ParseIssueCommentFull.parseIssueComment(author, body, commit, "bors");
        assertEquals(1, commands.size());
        assertEquals("force", commands.get(0).action);
    }

    @Test
    public void testClean() {
        String author = "jack";
        String body = "@bors clean";
        List<IssueCommentCommand> commands = ParseIssueCommentFull.parseIssueComment(author, body, commit, "bors");
        assertEquals(1, commands.size());
        assertEquals("clean", commands.get(0).action);
    }

    @Test
    public void testPing() {
        String author = "jack";
        String body = "@bors ping";
        List<IssueCommentCommand> commands = ParseIssueCommentFull.parseIssueComment(author, body, commit, "bors");
        assertEquals(1, commands.size());
        assertEquals("ping", commands.get(0).action);
        assertEquals("standard", commands.get(0).pingType);
    }

    @Test
    public void testHello() {
        String author = "jack";
        String body = "@bors hello?";
        List<IssueCommentCommand> commands = ParseIssueCommentFull.parseIssueComment(author, body, commit, "bors");
        assertEquals(1, commands.size());
        assertEquals("ping", commands.get(0).action);
        assertEquals("standard", commands.get(0).pingType);
    }

    @Test
    public void testPortalPing() {
        String author = "jack";
        String body = "@bors are you still there?";
        List<IssueCommentCommand> commands = ParseIssueCommentFull.parseIssueComment(author, body, commit, "bors");
        assertEquals(1, commands.size());
        assertEquals("ping", commands.get(0).action);
        assertEquals("portal", commands.get(0).pingType);
    }

    @Test
    public void testTreeclosed() {
        String author = "jack";
        String body = "@bors treeclosed=50";
        List<IssueCommentCommand> commands = ParseIssueCommentFull.parseIssueComment(author, body, commit, "bors");
        assertEquals(1, commands.size());
        assertEquals("treeclosed", commands.get(0).action);
        assertEquals(50, commands.get(0).treeclosedValue.intValue());
    }
}
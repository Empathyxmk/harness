package org.cyclopsgroup.jmxterm;

import org.junit.Test;

import static org.junit.Assert.*;

public class CommandPublicTest {

    static class DummyCommand extends Command {
        public StringBuilder log = new StringBuilder();
        @Override
        public void execute(Session session, String commandLine) {
            log.append("executed ").append(commandLine);
        }
        @Override
        public String getCanonicalName() {
            return "DummyCommand";
        }
        @Override
        public String getDisplayDescription() {
            return "Public Dummy";
        }
        @Override
        public String getDisplayName() {
            return "PublicDummy";
        }
    }

    @Test
    public void testDummyCommandExecution_public() {
        DummyCommand cmd = new DummyCommand();
        // Use different command line text
        cmd.execute(null, "hello world public 123");
        assertTrue(cmd.log.toString().contains("public 123"));
    }
}
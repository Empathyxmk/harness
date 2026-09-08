package org.cyclopsgroup.jmxterm;

import org.junit.Test;

import static org.junit.Assert.*;

public class CommandFactoryPublicTest {

    @Test
    public void testCreateInstance_public() throws Exception {
        // Use SelfRecordingCommand, but different args
        Command c = CommandFactory.createInstance(SelfRecordingCommand.class, "commandX", "2017", "b", "PRIORITY", 7);
        
        assertEquals("commandX", ((SelfRecordingCommand) c).n);
        assertEquals("2017", ((SelfRecordingCommand) c).a1);
        assertEquals("b", ((SelfRecordingCommand) c).a2);
        assertEquals("PRIORITY", ((SelfRecordingCommand) c).a3);
        assertEquals(7, ((SelfRecordingCommand) c).a4);
    }

    @Test(expected = NullPointerException.class)
    public void testCreateInstance_nullClass_public() throws Exception {
        CommandFactory.createInstance(null, "whatever");
    }
}
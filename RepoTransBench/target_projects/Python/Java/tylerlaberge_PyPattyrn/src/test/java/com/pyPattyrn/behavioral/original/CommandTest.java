package com.pyPattyrn.behavioral.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import com.pyPattyrn.behavioral.command.Command;
import com.pyPattyrn.behavioral.command.Invoker;
import com.pyPattyrn.behavioral.command.Receiver;

class CommandTest {
    private Receiver thermostat;

    @BeforeEach
    void setUp() {
        thermostat = new Receiver() {
            public String raiseTemp(int amount) {
                return "Temperature raised by " + amount + " degrees";
            }
            public String lowerTemp(int amount) {
                return "Temperature lowered by " + amount + " degrees";
            }
        };
    }

    static class RaiseTempCommand implements Command {
        private Receiver receiver;
        private int amount;

        public RaiseTempCommand(Receiver receiver, int amount) {
            this.receiver = receiver;
            this.amount = amount;
        }

        @Override
        public Object execute() {
            return ((Receiver) receiver).raiseTemp(amount);
        }
    }

    static class LowerTempCommand implements Command {
        private Receiver receiver;
        private int amount;

        public LowerTempCommand(Receiver receiver, int amount) {
            this.receiver = receiver;
            this.amount = amount;
        }

        @Override
        public Object execute() {
            return ((Receiver) receiver).lowerTemp(amount);
        }
    }

    @Test
    void testRaiseTempCommand() {
        Command cmd = new RaiseTempCommand(thermostat, 5);
        assertEquals("Temperature raised by 5 degrees", cmd.execute());
    }

    @Test
    void testLowerTempCommand() {
        Command cmd = new LowerTempCommand(thermostat, 7);
        assertEquals("Temperature lowered by 7 degrees", cmd.execute());
    }

    @Test
    void testInvokerExecutesCommands() {
        final StringBuilder log = new StringBuilder();
        Invoker invoker = new Invoker();
        Command logCommand = () -> {
            log.append("Executed");
            return null;
        };
        invoker.storeCommand(logCommand);
        invoker.executeCommand();
        assertEquals("Executed", log.toString());
    }
}
package com.sibson.redbeat.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.sibson.redbeat.stubs.*;

public class RedBeatConfigExtraTest {

    @Test
    public void testConfigValues() {
        AppStub app = new AppStub();
        RedBeatConfigStub config = new RedBeatConfigStub(app);

        assertEquals("redbeat:", config.getKeyPrefix());
        assertNull(config.getLockTimeout());

        config.setSchedule("myschedule");
        assertEquals("myschedule", config.getSchedule());
    }
}
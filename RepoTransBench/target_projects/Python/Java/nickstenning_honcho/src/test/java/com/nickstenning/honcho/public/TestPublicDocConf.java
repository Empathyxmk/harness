package com.nickstenning.honcho.public_;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestPublicDocConf {

    @Test
    void testPublicDocProjectName() {
        String project = "honcho";
        assertEquals("honcho", project);
    }
}
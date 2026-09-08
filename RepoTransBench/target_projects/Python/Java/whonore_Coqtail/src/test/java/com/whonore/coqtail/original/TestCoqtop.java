package com.whonore.coqtail.original;

import org.junit.jupiter.api.Test;
import java.util.logging.Logger;
import com.whonore.coqtail.Coqtop;
import static org.junit.jupiter.api.Assertions.*;

public class TestCoqtop {

    @Test
    void testJoinNotEmpty() {
        String[] msgs = { "foo", "", "bar" };
        String result = Coqtop.joinNotEmpty(msgs, "|");
        assertEquals("foo|bar", result);
    }

    @Test
    void testCoqtopErrorAndDuneError() {
        assertThrows(Coqtop.CoqtopError.class, () -> { throw new Coqtop.CoqtopError("stop"); });
        assertThrows(Coqtop.DuneError.class, () -> { throw new Coqtop.DuneError("fail"); });
        try {
            throw new Coqtop.CoqtopError("stop");
        } catch (Exception ce) {
            assertTrue(ce.getMessage().contains("stop"));
        }
        try {
            throw new Coqtop.DuneError("fail");
        } catch (Exception de) {
            assertTrue(de.getMessage().contains("fail"));
        }
    }

    @Test
    void testCoqtopInitAndLogger() {
        Coqtop ct = new Coqtop();
        assertNotNull(ct.states);
        ct.logger.info("hello");
    }

    @Test
    void testIsInValidDuneProjectFalse() {
        Coqtop ct = new Coqtop();
        ct.xml = null;
        assertFalse(ct.isInValidDuneProject("file.v"));
    }
}
package com.initstring.public_;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.initstring.linkedin2username.NameMutator;

public class TestPublicImportPython {
    @Test
    public void testPublicBasicImports() {
        NameMutator nm = new NameMutator("Some Name");
        assertNotNull(nm);
    }
}
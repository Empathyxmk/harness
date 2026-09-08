package org.netbeans.modules.php.twig.editor.parsing;

import org.junit.Test;
import static org.junit.Assert.*;
import java.util.List;
import org.netbeans.modules.php.twig.editor.parsing.TwigParserResult.Block;
import org.netbeans.modules.parsing.api.Snapshot;

public class TwigParserResultTest {

    static class DummyBlock extends Block {
        private final String desc;
        private final int offset;
        private final int length;
        public DummyBlock(Snapshot snap, String desc, int offset, int length) {
            super(snap, desc, offset, length);
            this.desc = desc;
            this.offset = offset;
            this.length = length;
        }
        @Override public String getDescription() { return desc; }
        @Override public int getOffset() { return offset; }
        @Override public int getLength() { return length; }
    }

    static class DummySnapshot extends Snapshot {
        public DummySnapshot() { super(null, null, 0, null, null); }
    }

    @Test
    public void testConstructAndGetBlocks() {
        Snapshot snap = null;
        TwigParserResult res = new TwigParserResult(snap);
        assertNotNull(res.getBlocks());
        // should be modifiable (append)
        Block b = new DummyBlock(null, "block", 0, 5);
        res.getBlocks().add(b);
        assertTrue(res.getBlocks().contains(b));
    }

    @Test
    public void testBlockMethods() {
        Block b = new DummyBlock(null, "desc", 42, 7);
        assertEquals("desc", b.getDescription());
        assertEquals(42, b.getOffset());
        assertEquals(7, b.getLength());
    }
}
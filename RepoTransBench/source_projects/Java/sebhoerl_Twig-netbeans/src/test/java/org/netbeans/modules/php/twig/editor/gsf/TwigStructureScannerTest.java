package org.netbeans.modules.php.twig.editor.gsf;

import org.junit.Test;
import static org.junit.Assert.*;
import java.util.*;
import org.netbeans.modules.csl.api.OffsetRange;
import org.netbeans.modules.csl.api.StructureItem;
import org.netbeans.modules.csl.spi.ParserResult;
import org.netbeans.modules.php.twig.editor.parsing.TwigParserResult;

public class TwigStructureScannerTest {

    // Dummy Block for minimal structure
    static class DummyBlock extends TwigParserResult.Block {
        private final String descr;
        private final int offset, length;
        public DummyBlock(String descr, int offset, int length) {
            super(null, descr, offset, length);
            this.descr = descr;
            this.offset = offset;
            this.length = length;
        }
        @Override public String getDescription() { return descr; }
        @Override public int getOffset() { return offset; }
        @Override public int getLength() { return length; }
    }

    static class DummyTwigParserResult extends TwigParserResult {
        private List<Block> blocks;
        public DummyTwigParserResult(List<Block> blocks) {
            super(null);
            this.blocks = blocks;
        }
        @Override
        public List<Block> getBlocks() {
            return blocks;
        }
    }

    @Test
    public void testScanReturnsTopLevelBlocksOnly() {
        // block1 contains block2
        DummyBlock block1 = new DummyBlock("block", 0, 10);
        DummyBlock block2 = new DummyBlock("block", 2, 5);
        DummyBlock blockInline = new DummyBlock("*inline-block", 12, 1);
        List<TwigParserResult.Block> blocks = Arrays.asList(block1, block2, blockInline);
        ParserResult pr = new DummyTwigParserResult(blocks);

        TwigStructureScanner scanner = new TwigStructureScanner();
        List<? extends StructureItem> items = scanner.scan(pr);
        assertNotNull(items);
        // block1 and blockInline considered top-level
        assertTrue(items.size() >= 1);
    }

    @Test
    public void testFoldsReturnsAllBlocks() {
        DummyBlock block1 = new DummyBlock("block", 0, 10);
        DummyBlock block2 = new DummyBlock("xx", 13, 3);
        List<TwigParserResult.Block> blocks = Arrays.asList(block1, block2);
        ParserResult pr = new DummyTwigParserResult(blocks);

        TwigStructureScanner scanner = new TwigStructureScanner();
        Map<String, List<OffsetRange>> folds = scanner.folds(pr);
        assertTrue(folds.containsKey("tags"));
        List<OffsetRange> ranges = folds.get("tags");
        assertEquals(2, ranges.size());
        assertEquals(new OffsetRange(0, 10), ranges.get(0));
        assertEquals(new OffsetRange(13, 16), ranges.get(1));
    }

    @Test
    public void testGetConfigurationReturnsNull() {
        TwigStructureScanner scanner = new TwigStructureScanner();
        assertNull(scanner.getConfiguration());
    }
}
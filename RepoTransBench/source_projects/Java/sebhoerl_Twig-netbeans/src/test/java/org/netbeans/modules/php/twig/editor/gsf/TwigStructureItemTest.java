package org.netbeans.modules.php.twig.editor.gsf;

import org.junit.Test;
import static org.junit.Assert.*;
import java.util.*;
import org.netbeans.modules.csl.api.ElementKind;
import org.netbeans.modules.csl.api.OffsetRange;
import org.netbeans.modules.php.twig.editor.parsing.TwigParserResult;
import org.netbeans.modules.parsing.api.Snapshot;

public class TwigStructureItemTest {

    static class DummyBlock extends TwigParserResult.Block {
        private final String desc;
        private final int offset;
        private final int length;
        public DummyBlock(String desc, int offset, int length) {
            super(null, desc, offset, length);
            this.desc = desc;
            this.offset = offset;
            this.length = length;
        }
        @Override public String getDescription() { return desc; }
        @Override public int getOffset() { return offset; }
        @Override public int getLength() { return length; }
    }

    @Test
    public void testTwigStructureItemMethods() {
        DummyBlock block = new DummyBlock("block", 1, 10);
        List<TwigParserResult.Block> blocks = Arrays.asList(block);
        TwigStructureItem item = new TwigStructureItem(null, block, blocks);

        assertEquals("block", item.getName());
        assertEquals(ElementKind.METHOD, item.getKind());
        assertEquals(false, item.isLeaf());
        assertNotNull(item.getOffsetRange());
        assertEquals("block", item.getHtml(new org.netbeans.modules.csl.api.HtmlFormatter() {
            private final StringBuilder sb = new StringBuilder();
            @Override
            public void name(String name, boolean main) { sb.append(name); }
            @Override
            public void parameters(String parameters) { sb.append(parameters); }
            @Override
            public void appendText(String text) { sb.append(text); }
            @Override
            public String getText() { return sb.toString(); }
            @Override
            public void active(boolean start) {}
            @Override
            public void reset() { sb.setLength(0); }
        }));
        assertNotNull(item.getNestedItems());
        assertNull(item.getCustomIcon());
        assertNull(item.getSortText());
        assertNull(item.getPosition());
    }
}
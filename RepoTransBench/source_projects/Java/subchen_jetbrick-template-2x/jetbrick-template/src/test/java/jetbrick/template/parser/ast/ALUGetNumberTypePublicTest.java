package jetbrick.template.parser.ast;

import org.junit.Assert;
import org.junit.Test;

public class ALUGetNumberTypePublicTest {

    @Test
    public void testGetNumberTypeWithDifferentInteger() {
        Assert.assertEquals(ALU.TYPE_LONG, ALU.getNumberType(150L));
    }

    @Test
    public void testGetNumberTypeWithDifferentDouble() {
        Assert.assertEquals(ALU.TYPE_DOUBLE, ALU.getNumberType(0.00077d));
    }
}
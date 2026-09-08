package jetbrick.template.parser.ast;

import org.junit.Assert;
import org.junit.Test;

public class ALUPublicTest {
    @Test
    public void testDifferentAdditionCases() {
        // Different test data: bigger numbers
        Assert.assertEquals(100, ALU.eval('+', 70, 30));
    }

    @Test
    public void testDifferentSubtractionCases() {
        // Use different data
        Assert.assertEquals(-20, ALU.eval('-', 10, 30));
    }

    @Test
    public void testDifferentMultiplicationCases() {
        // Different data
        Assert.assertEquals(990, ALU.eval('*', 33, 30));
    }

    @Test
    public void testDifferentDivisionCases() {
        // Different data
        Assert.assertEquals(4, ALU.eval('/', 40, 10));
    }
}
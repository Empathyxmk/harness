package net.redwarp.tool.resizer.worker;

import org.junit.*;

public class OutputTest {

    @Test
    public void testEnumFormat() {
        Assert.assertEquals("png", Output.PNG.getFormat());
        Assert.assertEquals("jpg", Output.JPG.getFormat());
    }
}
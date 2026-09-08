package to.lean.tools.gmail.importer.local.thunderbird;

import org.junit.Test;

import static org.junit.Assert.*;

public class XMozillaStatusPublicTest {

    @Test
    public void testParsesDifferentHexString() {
        int status = XMozillaStatusParser.parseXMozillaStatus("0x0018");
        assertEquals(0x18, status);
    }

    @Test
    public void testParsesDifferentHexStringZero() {
        int status = XMozillaStatusParser.parseXMozillaStatus("0x0");
        assertEquals(0, status);
    }

    @Test
    public void testParsesDifferentHexStringUppercase() {
        int status = XMozillaStatusParser.parseXMozillaStatus("0X0022");
        assertEquals(0x22, status);
    }
}
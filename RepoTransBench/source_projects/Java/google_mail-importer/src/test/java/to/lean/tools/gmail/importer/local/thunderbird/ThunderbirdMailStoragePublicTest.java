package to.lean.tools.gmail.importer.local.thunderbird;

import org.junit.Test;
import java.io.File;

import static org.junit.Assert.*;

public class ThunderbirdMailStoragePublicTest {

    @Test
    public void testCanCreateFromDifferentFile() {
        File file = new File("/tmp/pubmailbox");
        ThunderbirdMailStorage storage = new ThunderbirdMailStorage(file);
        assertNotNull(storage);
    }
}
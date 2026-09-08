import org.junit.Test;
import static org.junit.Assert.*;

public class MetaTest {
    @Test
    public void testProjectStructureExists() {
        assertTrue("pom.xml should exist", new java.io.File("pom.xml").exists());
        assertTrue("README.md should exist", new java.io.File("README.md").exists());
    }
}
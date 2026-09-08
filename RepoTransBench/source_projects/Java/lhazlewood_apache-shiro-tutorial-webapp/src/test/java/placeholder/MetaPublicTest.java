import org.junit.Test;
import static org.junit.Assert.*;

public class MetaPublicTest {
    @Test
    public void testProjectRequiredFilesExist_Public() {
        assertTrue("pom.xml must be present in the repo", new java.io.File("pom.xml").exists());
        assertTrue("LICENSE should exist in project root", new java.io.File("LICENSE").exists());
    }
}
package com.ververica.flink.table.gateway;

import com.ververica.flink.table.gateway.utils.SqlGatewayException;
import org.junit.jupiter.api.Test;

import java.io.File;
import java.net.URL;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

public class SqlGatewayPublicTest {

    @Test
    public void testDiscoverDependenciesWithNonJarExtension() throws Exception {
        URL url = new File("README.md").toURI().toURL(); // Not a jar, not a .jar extension
        List<URL> jars = Collections.singletonList(url);
        try {
            SqlGateway.class.getDeclaredMethod("discoverDependencies", List.class, List.class)
                    .setAccessible(true);
            SqlGateway.discoverDependencies(jars, Collections.emptyList());
            fail("Expected SqlGatewayException");
        } catch (SqlGatewayException e) {
            assertTrue(e.getMessage().contains("Could not load all required JAR files"));
        }
    }

    @Test
    public void testDiscoverDependenciesWithNonExistingDir() throws Exception {
        File fakeDir = new File("fakePublicDirNotExist");
        URL fakeDirUrl = fakeDir.toURI().toURL();
        Exception ex = assertThrows(SqlGatewayException.class, () -> {
            SqlGateway.discoverDependencies(Collections.emptyList(), Collections.singletonList(fakeDirUrl));
        });
        assertTrue(ex.getMessage().contains("Could not load all required JAR files"));
    }

    @Test
    public void testDiscoverDependenciesWithEmptyDir() throws Exception {
        File dir = new File("testPublicDir");
        dir.mkdir();
        dir.deleteOnExit();
        URL dirUrl = dir.toURI().toURL();
        List<URL> out = SqlGateway.discoverDependencies(Collections.emptyList(), Collections.singletonList(dirUrl));
        assertEquals(0, out.size());
        dir.delete();
    }

    @Test
    public void testDiscoverDependenciesWithUnsupportedFileInDir() throws Exception {
        File dir = new File("testPublicDir2");
        dir.mkdir();
        dir.deleteOnExit();
        File file = new File(dir, "otherfile.data");
        file.createNewFile();
        file.deleteOnExit();
        URL dirUrl = dir.toURI().toURL();
        List<URL> out = SqlGateway.discoverDependencies(Collections.emptyList(), Collections.singletonList(dirUrl));
        assertEquals(0, out.size());
        file.delete();
        dir.delete();
    }
}
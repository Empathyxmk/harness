package com.ververica.flink.table.gateway;

import com.ververica.flink.table.gateway.utils.SqlGatewayException;
import org.junit.jupiter.api.Test;

import java.io.File;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

public class SqlGatewayTest {

    @Test
    public void testDiscoverDependenciesWithJarsOnly() throws Exception {
        URL url = new File("build.gradle").toURI().toURL(); // Not a jar but must not throw if no extension
        // Should not be added as a dependency. Expect checkJarFile to fail, so wrap in try-catch.
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
    public void testDiscoverDependenciesWithInvalidDir() throws Exception {
        URL fakeDir = new File("notExistDir").toURI().toURL();
        Exception ex = assertThrows(SqlGatewayException.class, () -> {
            SqlGateway.discoverDependencies(Collections.emptyList(), Collections.singletonList(fakeDir));
        });
        assertTrue(ex.getMessage().contains("Could not load all required JAR files"));
    }

    @Test
    public void testDiscoverDependenciesWithNonDirFile() throws Exception {
        // Use real file
        File f = File.createTempFile("testfile", ".tmp");
        f.deleteOnExit();
        URL url = f.toURI().toURL();
        Exception ex2 = assertThrows(SqlGatewayException.class, () -> {
            SqlGateway.discoverDependencies(Collections.emptyList(), Collections.singletonList(url));
        });
        assertTrue(ex2.getMessage().contains("Could not load all required JAR files"));
    }

    @Test
    public void testDiscoverDependenciesWithDir() throws Exception {
        // Create dir, add a .txt (not .jar)
        File dir = new File("testDir");
        dir.mkdir();
        dir.deleteOnExit();
        File notAJar = new File(dir, "file.txt");
        notAJar.createNewFile();
        notAJar.deleteOnExit();
        URL dirUrl = dir.toURI().toURL();
        List<URL> out = SqlGateway.discoverDependencies(Collections.emptyList(), Collections.singletonList(dirUrl));
        // Should not throw, no .jar, so dependencies = []
        assertEquals(0, out.size());
        notAJar.delete();
        dir.delete();
    }
}
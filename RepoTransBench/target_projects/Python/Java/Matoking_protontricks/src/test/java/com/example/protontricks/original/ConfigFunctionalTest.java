package com.example.protontricks.original;

import org.junit.jupiter.api.Test;
import java.io.IOException;
import java.nio.file.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.Properties;

class ConfigFunctionalTest {
    static class Config {
        final Path configPath;
        final Properties properties = new Properties();

        Config(Path configDir) {
            this.configPath = configDir.resolve("protontricks").resolve("conf.ini");
            if (Files.exists(this.configPath)) {
                try {
                    properties.load(Files.newBufferedReader(this.configPath));
                } catch (IOException ignored) { }
            }
        }

        String get(String section, String option, String defaultValue) {
            String k = section + "." + option;
            return properties.getProperty(k, defaultValue);
        }

        void set(String section, String option, String value) {
            String k = section + "." + option;
            properties.setProperty(k, value);
            try {
                Path dir = configPath.getParent();
                if (!Files.exists(dir)) Files.createDirectories(dir);
                properties.store(Files.newBufferedWriter(configPath), null);
            } catch (IOException ignored) {}
        }
    }

    @Test
    void testFunctionalConfigSet() throws IOException {
        Path tmp = Files.createTempDirectory("confFunc");
        Path customConfig = tmp.resolve("dir");
        Files.createDirectories(customConfig);

        Config conf = new Config(customConfig);

        conf.set("sect", "opt", "val");
        assertEquals("val", conf.get("sect", "opt", null));
        conf.set("sect", "opt", "changed");
        assertEquals("changed", conf.get("sect", "opt", null));

        Path confPath = customConfig.resolve("protontricks").resolve("conf.ini");
        String content = Files.readString(confPath);
        assertTrue(content.contains("sect.opt=changed"));
    }
}
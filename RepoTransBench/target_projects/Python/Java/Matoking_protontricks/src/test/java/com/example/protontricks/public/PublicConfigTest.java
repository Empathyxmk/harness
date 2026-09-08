package com.example.protontricks.public;

import org.junit.jupiter.api.Test;
import java.io.IOException;
import java.nio.file.*;
import java.util.Properties;

import static org.junit.jupiter.api.Assertions.*;

class PublicConfigTest {
    /**
     * Minimal simulation of config.Config.
     */
    static class Config {
        private final Path configPath;
        private final Properties properties = new Properties();

        public Config(Path configDir) {
            this.configPath = configDir.resolve("protontricks").resolve("config.ini");
            if (Files.exists(this.configPath)) {
                try {
                    properties.load(Files.newBufferedReader(this.configPath));
                } catch (IOException e) {
                    // ignore for test
                }
            }
        }

        public String get(String section, String option, String defaultValue) {
            String k = section + "." + option;
            return properties.getProperty(k, defaultValue);
        }

        public String get(String section, String option) {
            return get(section, option, null);
        }

        public void set(String section, String option, String value) {
            String k = section + "." + option;
            properties.setProperty(k, value);
            try {
                Path dir = configPath.getParent();
                if (!Files.exists(dir)) Files.createDirectories(dir);
                properties.store(Files.newBufferedWriter(configPath), null);
            } catch (IOException e) {
                // ignore for test
            }
        }
    }

    @Test
    void testPublicConfigGetSet() throws IOException {
        Path tmpPath = Files.createTempDirectory("protontricksPublicConfig");
        Path customConfig = tmpPath.resolve("someconfig");
        Files.createDirectories(customConfig);

        Config conf = new Config(customConfig);

        String defaultVal = conf.get("publicsection", "optionnotset", "some_public_default");
        assertEquals("some_public_default", defaultVal);

        conf.set("publicsection", "publicopt", "vvvtest");
        assertEquals("vvvtest", conf.get("publicsection", "publicopt"));

        conf.set("publicsection", "publicopt", "publicvalue2");
        assertEquals("publicvalue2", conf.get("publicsection", "publicopt"));

        Path configPath = customConfig.resolve("protontricks").resolve("config.ini");
        assertTrue(Files.exists(configPath));
        String content = Files.readString(configPath);
        assertTrue(content.contains("publicsection.publicopt"));
        assertTrue(content.contains("publicvalue2"));
    }
}
package com.example.protontricks.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.nio.file.*;
import java.util.Properties;
import java.io.IOException;

class ConfigTest {
    static class Config {
        private final Path configPath;
        private final Properties properties = new Properties();

        Config(Path configDir) {
            this.configPath = configDir.resolve("protontricks").resolve("config.ini");
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

        String get(String section, String option) {
            return get(section, option, null);
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
    void testSetAndGetAndDefault() throws IOException {
        Path temp = Files.createTempDirectory("configorig");
        Path customConfig = temp.resolve("origconfig");
        Files.createDirectories(customConfig);

        Config conf = new Config(customConfig);

        assertEquals("the_default", conf.get("something", "notset", "the_default"));

        conf.set("section", "opt", "1");
        assertEquals("1", conf.get("section", "opt"));
        conf.set("section", "opt2", "abc");
        assertEquals("abc", conf.get("section", "opt2"));

        Path configPath = customConfig.resolve("protontricks").resolve("config.ini");
        assertTrue(Files.exists(configPath));
        String content = Files.readString(configPath);
        assertTrue(content.contains("section.opt"));
        assertTrue(content.contains("opt2"));
        assertTrue(content.contains("abc"));
    }
}
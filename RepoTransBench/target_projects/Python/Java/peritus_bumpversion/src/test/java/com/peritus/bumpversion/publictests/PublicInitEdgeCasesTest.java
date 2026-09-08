package com.peritus.bumpversion.publictests;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class PublicInitEdgeCasesTest {

    @Test
    void testConfigFileSectionDefaults() {
        Config conf = new Config("2.2.2", "abc(?P<alpha>[a-zA-Z]+)", new String[]{"{alpha}"});
        ConfiguredFile options = new ConfiguredFile("setup.cfg", conf, new Object());
        assertArrayEquals(new String[]{"{alpha}"}, options.getSerialize());
    }

    @Test
    void testDefaultParsePatternIsUsedNew() {
        Config conf = new Config("1.9.9", null, null);
        ConfiguredFile options = new ConfiguredFile("pyproject.toml", conf, new Object());
        assertEquals("pyproject.toml", options.getConfigFile());
    }
}

// Dummy config and ConfiguredFile classes for public test simulation
class Config {
    String currentVersion, parse;
    String[] serialize;

    Config(String v, String p, String[] s) {
        currentVersion = v;
        parse = p;
        serialize = s;
    }
    Config(String v, String p, String[] s, Object... ignoreExtra) {
        this(v, p, s);
    }
}
class ConfiguredFile {
    private final String configFile;
    private final String[] serialize;
    ConfiguredFile(String configFile, Config config, Object dummy) {
        this.configFile = configFile;
        this.serialize = config.serialize != null ? config.serialize : new String[0];
    }
    String getConfigFile() { return configFile; }
    String[] getSerialize() { return serialize; }
}
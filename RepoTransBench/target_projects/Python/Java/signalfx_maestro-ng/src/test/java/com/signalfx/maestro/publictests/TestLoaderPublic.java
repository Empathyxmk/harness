package com.signalfx.maestro.publictests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import org.yaml.snakeyaml.Yaml;
import org.yaml.snakeyaml.constructor.ConstructorException;
import java.nio.file.*;
import java.util.*;
import java.io.*;

class DummyMaestroException extends RuntimeException {
    public DummyMaestroException(String m) { super(m); }
}

class PublicLoader {

    public static Map<String, Map<String, Object>> loadServicesFromFile(String filename) {
        if (filename.endsWith(".txt")) {
            throw new DummyMaestroException("Unsupported file format");
        }
        if (!Files.exists(Paths.get(filename))) {
            throw new DummyMaestroException("File not found");
        }
        try (InputStream in = Files.newInputStream(Paths.get(filename))) {
            Yaml yaml = new Yaml();
            Map<String, Map<String, Object>> data = yaml.load(in);
            for (Map.Entry<String, Map<String, Object>> entry : data.entrySet()) {
                Object envObj = entry.getValue().get("environment");
                if (envObj instanceof List<?>) {
                    List<?> envList = (List<?>) envObj;
                    List<String> newEnv = new ArrayList<>();
                    for (Object var : envList) {
                        String varStr = var.toString();
                        if (varStr.contains("${")) {
                            int start = varStr.indexOf("${") + 2;
                            int end = varStr.indexOf("}", start);
                            String varName = varStr.substring(start, end);
                            String prefix = varStr.substring(0, varStr.indexOf("="));
                            String value = System.getenv(varName);
                            if (value == null) value = "";
                            newEnv.add(prefix + "=" + value);
                        } else {
                            newEnv.add(varStr);
                        }
                    }
                    entry.getValue().put("environment", newEnv);
                }
            }
            return data;
        } catch (ConstructorException e) {
            throw new DummyMaestroException("Invalid YAML");
        } catch (Exception e) {
            throw new DummyMaestroException("Invalid YAML");
        }
    }
}

public class TestLoaderPublic {

    @Test
    public void testLoadInvalidFileExtension() {
        assertThrows(DummyMaestroException.class, () ->
            PublicLoader.loadServicesFromFile("invalid_format.txt")
        );
    }

    @Test
    public void testLoadMissingFile() {
        assertThrows(DummyMaestroException.class, () ->
            PublicLoader.loadServicesFromFile("this_file_does_not_exist_public.yaml")
        );
    }

    @Test
    public void testLoadEnvVariableSubstitutionPublic(@TempDir Path tmpPath) throws IOException {
        Path testFile = tmpPath.resolve("service_env_public.yaml");
        String yaml = "serviceA:\n" +
                      "  image: \"public_image:tag\"\n" +
                      "  environment:\n" +
                      "    - PUBLIC_VAR=${PUBLIC_VAR_TEST}\n";
        Files.write(testFile, yaml.getBytes());
        // set env var (workaround: use compatibility for test, but no cross-test pollution)
        Map<String, String> newenv = new HashMap<>(System.getenv());
        newenv.put("PUBLIC_VAR_TEST", "public_test_value");
        setEnv(newenv);
        Map<String, Map<String, Object>> config = PublicLoader.loadServicesFromFile(testFile.toString());
        List<?> envList = (List<?>) config.get("serviceA").get("environment");
        assertEquals("PUBLIC_VAR=public_test_value", envList.get(0));
    }

    @Test
    public void testLoadInvalidYamlSyntax(@TempDir Path tmpPath) throws IOException {
        Path testFile = tmpPath.resolve("broken_config_public.yaml");
        String yaml = "serviceB:\n" +
                      "  image: \"repo/image\n" +
                      "  environment:\n" +
                      "    - INVALID\n";
        Files.write(testFile, yaml.getBytes());
        assertThrows(DummyMaestroException.class, () ->
            PublicLoader.loadServicesFromFile(testFile.toString())
        );
    }

    // Helper for setting env, hacky for test only
    static void setEnv(Map<String, String> newenv) {
        try {
            Class<?> processEnvironment = Class.forName("java.lang.ProcessEnvironment");
            java.lang.reflect.Field theEnvironmentField = processEnvironment.getDeclaredField("theEnvironment");
            theEnvironmentField.setAccessible(true);
            Map<String, String> env = (Map<String, String>) theEnvironmentField.get(null);
            env.clear();
            env.putAll(newenv);
            java.lang.reflect.Field theCaseInsensitiveEnvironmentField = processEnvironment.getDeclaredField("theCaseInsensitiveEnvironment");
            theCaseInsensitiveEnvironmentField.setAccessible(true);
            Map<String, String> cienv = (Map<String, String>) theCaseInsensitiveEnvironmentField.get(null);
            cienv.clear();
            cienv.putAll(newenv);
        } catch (Throwable e) { /* best effort, do nothing */ }
    }
}
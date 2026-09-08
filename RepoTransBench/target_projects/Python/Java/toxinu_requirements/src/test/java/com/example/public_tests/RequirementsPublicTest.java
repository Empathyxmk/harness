package com.example.public_tests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.io.*;
import java.nio.file.*;
import java.util.*;

import com.example.Requirements;
import com.example.Requirement;

public class RequirementsPublicTest {
    private Path rootDirectory;
    private Path originalDirectory;
    private Requirements r;

    @BeforeEach
    void setUp() throws IOException {
        rootDirectory = Files.createTempDirectory("reqs");
        originalDirectory = Paths.get(System.getProperty("user.dir"));
        System.setProperty("user.dir", rootDirectory.toString());
        r = new Requirements();
    }

    @AfterEach
    void tearDown() throws IOException {
        System.setProperty("user.dir", originalDirectory.toString());
        Files.walk(rootDirectory)
                .sorted(Comparator.reverseOrder())
                .forEach(path -> {
                    try { Files.delete(path); } catch (IOException e) {}
                });
    }

    @Test
    void testRequirementReprPublic() {
        Requirement r = Requirement.parse("pandas==1.3.1");
        assertEquals("<Requirement: \"pandas==1.3.1\">", r.toDebugString());
    }

    @Test
    void testRequirementParsingPublic() {
        String line = "  pandas==1.3.1,>=1.0.0 # cheese";
        Requirement r = Requirement.parse(line);
        assertEquals(line, r.getLine());
        assertEquals("pandas", r.getName());
        assertEquals(Arrays.asList(
                new AbstractMap.SimpleEntry<>("==", "1.3.1"),
                new AbstractMap.SimpleEntry<>(">=", "1.0.0")
        ), r.getSpecs());
    }

    @Test
    void testDetectFilesPublic() throws IOException {
        Path requirementsPath = rootDirectory.resolve("requirements.txt");
        Files.write(requirementsPath, Arrays.asList("pandas==1.3.1"));

        Path requirementsDir = rootDirectory.resolve("requirements");
        Files.createDirectory(requirementsDir);
        Path testsRequirementsPath = requirementsDir.resolve("tests.txt");
        Files.write(testsRequirementsPath, Arrays.asList("pytest==6.2.5"));

        Map<String, List<String>> dependencies = r.getDependencies();
        assertEquals(Arrays.asList("pytest == 6.2.5"), dependencies.get("tests_require"));
        assertEquals(Arrays.asList("pandas == 1.3.1"), dependencies.get("install_requires"));
        assertEquals(Collections.emptyList(), dependencies.get("dependency_links"));
    }

    @Test
    void testDifferentPathsPublic() throws IOException {
        Path requirementsPath = rootDirectory.resolve("reqs.txt");
        Files.write(requirementsPath, Arrays.asList("pandas==1.3.1"));

        Path mrDir = rootDirectory.resolve("other-requirements");
        Files.createDirectory(mrDir);
        Path testsRequirementsPath = mrDir.resolve("baz.txt");
        Files.write(testsRequirementsPath, Arrays.asList("pytest==6.2.5"));

        r.setRequirementsPath(requirementsPath.toString());
        r.setTestsRequirementsPath(testsRequirementsPath.toString());

        Map<String, List<String>> dependencies = r.getDependencies();
        assertEquals(Arrays.asList("pytest == 6.2.5"), dependencies.get("tests_require"));
        assertEquals(Arrays.asList("pandas == 1.3.1"), dependencies.get("install_requires"));
        assertEquals(Collections.emptyList(), dependencies.get("dependency_links"));
    }

    @Test
    void testEmptyLinesPublic() throws IOException {
        Path requirementsPath = rootDirectory.resolve("requirements.txt");
        List<String> lines = new ArrayList<>();
        lines.add("");
        lines.add("");
        lines.add("pandas==1.3.1 #I like cheese");
        lines.add("");
        lines.add("numpy");
        Files.write(requirementsPath, lines);

        Map<String, List<String>> dependencies = r.getDependencies();
        List<String> expected = Arrays.asList("pandas == 1.3.1", "numpy");
        List<String> actual = dependencies.get("install_requires");
        expected.sort(String::compareTo);
        actual.sort(String::compareTo);
        assertEquals(expected, actual);
    }

    @Test
    void testCommentsLineIgnoredPublic() throws IOException {
        Path requirementsPath = rootDirectory.resolve("requirements.txt");
        List<String> lines = Arrays.asList(
                "# numpy==python3-bar",
                "pandas==1.3.1 #I like cheese"
        );
        Files.write(requirementsPath, lines);

        Path requirementsDir = rootDirectory.resolve("requirements");
        Files.createDirectory(requirementsDir);
        Path testsRequirementsPath = requirementsDir.resolve("tests.txt");
        Files.write(testsRequirementsPath, Arrays.asList("pytest==6.2.5"));

        Map<String, List<String>> dependencies = r.getDependencies();
        assertEquals(Arrays.asList("pytest == 6.2.5"), dependencies.get("tests_require"));
        assertEquals(Arrays.asList("pandas == 1.3.1"), dependencies.get("install_requires"));
        assertEquals(Collections.emptyList(), dependencies.get("dependency_links"));
    }

    @Test
    void testMultiSpecifiersPublic() throws IOException {
        Path requirementsPath = rootDirectory.resolve("requirements.txt");
        Path testsRequirementsPath = rootDirectory.resolve("tests-extra-requirements.txt");

        Files.write(requirementsPath, Arrays.asList("pandas<=1.3.1,>=1.0.5"));
        Files.write(testsRequirementsPath, Arrays.asList("pandas   <=  1.3.1 , >=1.0.5"));

        r.setTestsRequirementsPath("tests-extra-requirements.txt");
        Map<String, List<String>> dependencies = r.getDependencies();
        assertEquals(Arrays.asList("pandas <= 1.3.1, >= 1.0.5"), dependencies.get("install_requires"));
        assertEquals(Arrays.asList("pandas <= 1.3.1, >= 1.0.5"), dependencies.get("tests_require"));
    }

    @Test
    void testIgnoreEveryPrivateLinksPublic() throws IOException {
        Path requirementsPath = rootDirectory.resolve("requirements.txt");
        List<String> lines = Arrays.asList(
            "--no-index --find-links=/tmp/otherwheel SomeOtherPkg",
            "--find-links=/tmp/otherwheel AnotherPkg",
            "-f /tmp/otherwheel YetAnotherPkg",
            "--extra-index-url http://baz.qux SomePkg",
            "-i http://baz.qux TestPkg",
            "pandas",
            "--index-url http://baz.qux OrphanPkg"
        );
        Files.write(requirementsPath, lines);

        Map<String, List<String>> dependencies = r.getDependencies();
        assertEquals(Arrays.asList("pandas"), dependencies.get("install_requires"));
    }

    @Test
    void testIgnoreArgumentsPublic() throws IOException {
        Path requirementsPath = rootDirectory.resolve("requirements.txt");
        List<String> lines = Arrays.asList(
            "pandas",
            "--always-unzip AnotherPackage",
            "-Z YetAnotherPackage"
        );
        Files.write(requirementsPath, lines);

        Map<String, List<String>> dependencies = r.getDependencies();
        assertEquals(Arrays.asList("pandas"), dependencies.get("install_requires"));
    }

    @Test
    void testRequirementsInceptionPublic() throws IOException {
        Path requirementsPath = rootDirectory.resolve("requirements.txt");
        Path requirementsPath02 = rootDirectory.resolve("requirements-04.txt");
        Path requirementsDir = rootDirectory.resolve("requirements");
        Files.createDirectory(requirementsDir);
        Path requirementsPath03 = requirementsDir.resolve("requirements-05.txt");

        Files.write(requirementsPath, Arrays.asList("pandas", "-r requirements-04.txt"));
        Files.write(requirementsPath02, Arrays.asList("numpy", "--requirement requirements/requirements-05.txt"));
        Files.write(requirementsPath03, Arrays.asList("requests==2.25.1"));

        Map<String, List<String>> dependencies = r.getDependencies();
        List<String> expected = Arrays.asList("pandas", "numpy", "requests == 2.25.1");
        List<String> actual = dependencies.get("install_requires");
        expected.sort(String::compareTo);
        actual.sort(String::compareTo);
        assertEquals(expected, actual);
    }
}
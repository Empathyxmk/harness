package com.example.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.io.*;
import java.nio.file.*;
import java.util.*;

import com.example.Requirements;
import com.example.Requirement;

public class RequirementsTest {
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
        // Clean up test files & dirs
        Files.walk(rootDirectory)
                .sorted(Comparator.reverseOrder())
                .forEach(path -> {
                    try { Files.delete(path); } catch (IOException e) {}
                });
    }

    @Test
    void testRequirementRepr() {
        Requirement r = Requirement.parse("requests==2.9.1");
        assertEquals("<Requirement: \"requests==2.9.1\">", r.toDebugString());
    }

    @Test
    void testRequirementParsing() {
        String line = "  requests==2.9.1,>=2.8.1 # jambon";
        Requirement r = Requirement.parse(line);
        assertEquals(line, r.getLine());
        assertEquals("requests", r.getName());
        assertEquals(Arrays.asList(
                new AbstractMap.SimpleEntry<>("==", "2.9.1"),
                new AbstractMap.SimpleEntry<>(">=", "2.8.1")
        ), r.getSpecs());
    }

    @Test
    void testDetectFiles() throws IOException {
        Path requirementsPath = rootDirectory.resolve("requirements.txt");
        Files.write(requirementsPath, Arrays.asList("requests==2.9.1"));

        Path requirementsDir = rootDirectory.resolve("requirements");
        Files.createDirectory(requirementsDir);
        Path testsRequirementsPath = requirementsDir.resolve("tests.txt");
        Files.write(testsRequirementsPath, Arrays.asList("flake8==2.5.4"));

        Map<String, List<String>> dependencies = r.getDependencies();
        assertEquals(Arrays.asList("flake8 == 2.5.4"), dependencies.get("tests_require"));
        assertEquals(Arrays.asList("requests == 2.9.1"), dependencies.get("install_requires"));
        assertEquals(Collections.emptyList(), dependencies.get("dependency_links"));
    }

    @Test
    void testDifferentPaths() throws IOException {
        Path requirementsPath = rootDirectory.resolve("foo.txt");
        Files.write(requirementsPath, Arrays.asList("requests==2.9.1"));

        Path mrDir = rootDirectory.resolve("moar-requirements");
        Files.createDirectory(mrDir);
        Path testsRequirementsPath = mrDir.resolve("bar.txt");
        Files.write(testsRequirementsPath, Arrays.asList("flake8==2.5.4"));

        r.setRequirementsPath(requirementsPath.toString());
        r.setTestsRequirementsPath(testsRequirementsPath.toString());

        Map<String, List<String>> dependencies = r.getDependencies();
        assertEquals(Arrays.asList("flake8 == 2.5.4"), dependencies.get("tests_require"));
        assertEquals(Arrays.asList("requests == 2.9.1"), dependencies.get("install_requires"));
        assertEquals(Collections.emptyList(), dependencies.get("dependency_links"));
    }

    @Test
    void testEmptyLines() throws IOException {
        Path requirementsPath = rootDirectory.resolve("requirements.txt");
        List<String> lines = new ArrayList<>();
        lines.add("");
        lines.add("");
        lines.add("requests==2.9.1 #I like ham");
        lines.add("");
        lines.add("boto");
        Files.write(requirementsPath, lines);

        Map<String, List<String>> dependencies = r.getDependencies();
        List<String> expected = Arrays.asList("requests == 2.9.1", "boto");
        List<String> actual = dependencies.get("install_requires");
        expected.sort(String::compareTo);
        actual.sort(String::compareTo);
        assertEquals(expected, actual);
    }

    @Test
    void testCommentsLineIgnored() throws IOException {
        Path requirementsPath = rootDirectory.resolve("requirements.txt");
        List<String> lines = Arrays.asList(
                "# boto==python3-lol",
                "requests==2.9.1 #I like ham"
        );
        Files.write(requirementsPath, lines);

        Path requirementsDir = rootDirectory.resolve("requirements");
        Files.createDirectory(requirementsDir);
        Path testsRequirementsPath = requirementsDir.resolve("tests.txt");
        Files.write(testsRequirementsPath, Arrays.asList("flake8==2.5.4"));

        Map<String, List<String>> dependencies = r.getDependencies();
        assertEquals(Arrays.asList("flake8 == 2.5.4"), dependencies.get("tests_require"));
        assertEquals(Arrays.asList("requests == 2.9.1"), dependencies.get("install_requires"));
        assertEquals(Collections.emptyList(), dependencies.get("dependency_links"));
    }

    @Test
    void testMultiSpecifiers() throws IOException {
        Path requirementsPath = rootDirectory.resolve("requirements.txt");
        Path testsRequirementsPath = rootDirectory.resolve("tests-requirements.txt");

        Files.write(requirementsPath, Arrays.asList("requests<=2.9.1,>=2.8.5"));
        Files.write(testsRequirementsPath, Arrays.asList("requests   <=  2.9.1 , >=2.8.5"));

        r.setTestsRequirementsPath("tests-requirements.txt");
        Map<String, List<String>> dependencies = r.getDependencies();
        assertEquals(Arrays.asList("requests <= 2.9.1, >= 2.8.5"), dependencies.get("install_requires"));
        assertEquals(Arrays.asList("requests <= 2.9.1, >= 2.8.5"), dependencies.get("tests_require"));
    }

    @Test
    void testIgnoreEveryPrivateLinks() throws IOException {
        Path requirementsPath = rootDirectory.resolve("requirements.txt");
        List<String> lines = Arrays.asList(
            "--no-index --find-links=/tmp/wheelhouse SomePackage",
            "--find-links=/tmp/wheelhouse SomePackage",
            "-f /tmp/wheelhouse SomePackage",
            "--extra-index-url http://foo.bar SomePackage",
            "-i http://foo.bar SomePackage",
            "requests",
            "--index-url http://foo.bar SomePackage"
        );
        Files.write(requirementsPath, lines);

        Map<String, List<String>> dependencies = r.getDependencies();
        assertEquals(Arrays.asList("requests"), dependencies.get("install_requires"));
    }

    @Test
    void testIgnoreArguments() throws IOException {
        Path requirementsPath = rootDirectory.resolve("requirements.txt");
        List<String> lines = Arrays.asList(
            "requests",
            "--always-unzip SomePackage",
            "-Z SomePackage"
        );
        Files.write(requirementsPath, lines);

        Map<String, List<String>> dependencies = r.getDependencies();
        assertEquals(Arrays.asList("requests"), dependencies.get("install_requires"));
    }

    @Test
    void testRequirementsInception() throws IOException {
        Path requirementsPath = rootDirectory.resolve("requirements.txt");
        Path requirementsPath02 = rootDirectory.resolve("requirements-02.txt");
        Path requirementsDir = rootDirectory.resolve("requirements");
        Files.createDirectory(requirementsDir);
        Path requirementsPath03 = requirementsDir.resolve("requirements-03.txt");

        Files.write(requirementsPath, Arrays.asList("requests", "-r requirements-02.txt"));
        Files.write(requirementsPath02, Arrays.asList("boto", "--requirement requirements/requirements-03.txt"));
        Files.write(requirementsPath03, Arrays.asList("isit==0.1.0"));

        Map<String, List<String>> dependencies = r.getDependencies();
        List<String> expected = Arrays.asList("requests", "boto", "isit == 0.1.0");
        List<String> actual = dependencies.get("install_requires");
        expected.sort(String::compareTo);
        actual.sort(String::compareTo);
        assertEquals(expected, actual);
    }

    @Test
    void testDependencyLinks() throws IOException {
        Path requirementsPath = rootDirectory.resolve("requirements.txt");
        List<String> lines = Arrays.asList(
            "boto",
            "-e git+https://github.com/kennethreitz/requests.git@master#egg=requests",
            "-e svn+http://foo:bar@svn.myproject.org/svn/MyProject/trunk@2019#egg=foo01    # COMMENT",
            "-e git+ssh://git@myproject.org/MyProject/#egg=foo02",
            "-e hg+http://hg.myproject.org/MyProject/@da39a3ee5e6b#egg=foo03",
            "-e bzr+https://bzr.myproject.org/MyProject/trunk/@2019#egg=foo04"
        );
        Files.write(requirementsPath, lines);

        Map<String, List<String>> dependencies = r.getDependencies();

        List<String> expected = Arrays.asList("requests", "boto", "foo01", "foo02", "foo03", "foo04");
        List<String> actual = dependencies.get("install_requires");
        expected.sort(String::compareTo);
        actual.sort(String::compareTo);
        assertEquals(expected, actual);

        List<String> expectedLinks = Arrays.asList(
            "git+https://github.com/kennethreitz/requests.git@master#egg=requests",
            "svn+http://foo:bar@svn.myproject.org/svn/MyProject/trunk@2019#egg=foo01",
            "git+ssh://git@myproject.org/MyProject/#egg=foo02",
            "hg+http://hg.myproject.org/MyProject/@da39a3ee5e6b#egg=foo03",
            "bzr+https://bzr.myproject.org/MyProject/trunk/@2019#egg=foo04"
        );
        List<String> actualLinks = dependencies.get("dependency_links");
        expectedLinks.sort(String::compareTo);
        actualLinks.sort(String::compareTo);
        assertEquals(expectedLinks, actualLinks);
    }

    @Test
    void testHttpLink() throws IOException {
        Path requirementsPath = rootDirectory.resolve("requirements.txt");
        List<String> lines = Arrays.asList(
            "boto",
            "http://someserver.org/packages/MyPackage-3.0.tar.gz#egg=foo"
        );
        Files.write(requirementsPath, lines);

        Map<String, List<String>> dependencies = r.getDependencies();
        List<String> expected = Arrays.asList("boto", "foo");
        List<String> actual = dependencies.get("install_requires");
        expected.sort(String::compareTo);
        actual.sort(String::compareTo);
        assertEquals(expected, actual);

        List<String> expectedLinks = Arrays.asList("http://someserver.org/packages/MyPackage-3.0.tar.gz#egg=foo");
        List<String> actualLinks = dependencies.get("dependency_links");
        expectedLinks.sort(String::compareTo);
        actualLinks.sort(String::compareTo);
        assertEquals(expectedLinks, actualLinks);
    }
}
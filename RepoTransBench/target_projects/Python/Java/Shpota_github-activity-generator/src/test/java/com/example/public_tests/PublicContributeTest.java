package com.example.public_tests;

import com.example.contribute.Args;
import com.example.contribute.Contribute;
import org.junit.jupiter.api.*;
import java.io.*;
import java.nio.file.Files;
import java.time.LocalDateTime;
import java.time.Month;
import java.time.temporal.ChronoUnit;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class PublicContributeTest {

    // Clean up repository-* dirs before and after each test
    @BeforeEach
    @AfterEach
    void cleanupRepos() {
        File cwd = new File(".");
        File[] dirs = cwd.listFiles((dir, name) ->
                name.startsWith("repository-") && new File(dir, name).isDirectory());
        if (dirs != null) {
            for (File d : dirs) {
                try {
                    deleteRecursively(d.toPath());
                } catch (Exception ignored) {}
            }
        }
        // Also delete public README.md if created
        File readme = new File("README.md");
        if (readme.exists()) readme.delete();
    }

    private void deleteRecursively(java.nio.file.Path path) throws IOException {
        if (Files.notExists(path)) return;
        if (Files.isDirectory(path)) {
            try (java.nio.file.DirectoryStream<java.nio.file.Path> stream = Files.newDirectoryStream(path)) {
                for (java.nio.file.Path entry : stream) deleteRecursively(entry);
            }
        }
        Files.deleteIfExists(path);
    }

    @Test
    void testMessageAndContributionsPerDayBoundsPublic() {
        LocalDateTime now = LocalDateTime.now();
        String msg = Contribute.message(now);
        // choose different word for check, but still checking part of the message
        assertTrue(msg.contains("Contr"));

        // Max commits capped at 20: use a different high value
        Args args = new Args(false, 9999, 80, null, null, null, 2, 2);
        assertEquals(20, Contribute.contributionsPerDay(args, new Random() {
            @Override public int nextInt(int bound) { return bound - 1; }
        }));

        // Min commits floored at 1: use a different negative
        Args args2 = new Args(false, -20, 80, null, null, null, 2, 2);
        assertEquals(1, Contribute.contributionsPerDay(args2, new Random()));
    }

    @Test
    void testArgumentsAndInvalidArgsPublic() {
        String[] argv = new String[] {
                "--no_weekends", "--max_commits", "9",
                "--frequency", "10", "--days_after", "6",
                "--repository", "repo-test", "--user_name", "Public User",
                "--user_email", "public-user@example.com"
        };
        Args out = Contribute.arguments(argv);
        assertTrue(out.noWeekends);
        assertEquals(9, out.maxCommits);
        assertEquals(10, out.frequency);
        assertEquals("repo-test", out.repository);
        assertEquals("Public User", out.userName);
        assertEquals("public-user@example.com", out.userEmail);
        assertEquals(6, out.daysAfter);

        Exception ex = assertThrows(IllegalArgumentException.class,
                () -> Contribute.arguments(new String[]{"--notarealarg"}));
        assertTrue(ex.getMessage().contains("Unknown argument"));
    }

    @Test
    void testDatesRangePublic() {
        int minDay = 10;
        int maxDay = 13;
        LocalDateTime now = LocalDateTime.now().truncatedTo(ChronoUnit.DAYS);
        Iterable<LocalDateTime> days = Contribute.datesRange(now.minusDays(minDay), now.plusDays(maxDay));
        List<LocalDateTime> daysList = new ArrayList<>();
        for (LocalDateTime d : days) daysList.add(d);
        assertEquals(now.minusDays(minDay).toLocalDate(), daysList.get(0).toLocalDate());
        assertEquals(now.plusDays(maxDay).toLocalDate(), daysList.get(daysList.size() - 1).toLocalDate());
        assertEquals(minDay + maxDay + 1, daysList.size());
    }

    @Test
    void testIsWeekendPublic() {
        // Sunday = 2023-07-09, Tuesday = 2023-07-11
        LocalDateTime sunday = LocalDateTime.of(2023, 7, 9, 0, 0);
        LocalDateTime tuesday = LocalDateTime.of(2023, 7, 11, 0, 0);
        assertTrue(Contribute.isWeekend(sunday));
        assertFalse(Contribute.isWeekend(tuesday));
    }
}
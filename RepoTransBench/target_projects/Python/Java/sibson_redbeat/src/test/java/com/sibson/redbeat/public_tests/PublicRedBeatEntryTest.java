package com.sibson.redbeat.public_tests;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentMatchers;

import java.time.Duration;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.HashMap;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import com.sibson.redbeat.stubs.*;

public class PublicRedBeatEntryTest {
    private AppStub app;
    private RedisStub redis;
    private static final HashMap<String, Object> CELERY_CONFIG_DEFAULT_KWARGS = new HashMap<>();

    @BeforeEach
    public void setup() {
        app = new AppStub();
        redis = app.redbeatRedis;
    }

    private RedBeatSchedulerEntryStub createEntry(String name, String task) {
        return new RedBeatSchedulerEntryStub(name, task, new ScheduleStub(3, false), app);
    }

    @Test
    public void testBasicSave() throws Exception {
        RedBeatSchedulerEntryStub e = createEntry("public_test", "tasks.public_test");
        e.save();
        HashMap<String, Object> expected = new HashMap<>();
        expected.put("name", "public_test");
        expected.put("task", "tasks.public_test");
        expected.put("schedule", e.schedule);
        expected.put("args", null);
        expected.put("kwargs", CELERY_CONFIG_DEFAULT_KWARGS);
        expected.put("options", new HashMap<>());
        expected.put("enabled", true);

        String expectedKey = app.redbeatConf.keyPrefix + "public_test";
        String value = redis.hget(expectedKey, "definition");
        assertEquals(expected, RedBeatStubHelpers.decodeJsonToMap(value, e.schedule));
        assertEquals(0, redis.zrank(app.redbeatConf.scheduleKey, e.key));
        assertEquals(e.score, redis.zscore(app.redbeatConf.scheduleKey, e.key));
    }

    @Test
    public void testFromKeyNonexistentKey() {
        assertThrows(KeyNotFoundException.class, () -> {
            RedBeatSchedulerEntryStub.fromKey("doesnotexist_public", app);
        });
    }

    @Test
    public void testFromKeyMissingMeta() throws Exception {
        RedBeatSchedulerEntryStub initial = createEntry("entry_missing_meta", "tasks.entry_missing_meta");
        initial.save();
        RedBeatSchedulerEntryStub loaded = RedBeatSchedulerEntryStub.fromKey(initial.key, app);
        assertEquals(initial.task, loaded.task);
        assertNotNull(loaded.lastRunAt);
    }

    @Test
    public void testNext() throws Exception {
        RedBeatSchedulerEntryStub initial = createEntry("public_next", "tasks.public_next");
        initial.save();
        LocalDateTime now = app.now();
        RedBeatSchedulerEntryStub n = initial.next(now);

        assertNotNull(now.atZone(ZoneOffset.UTC).getOffset());
        assertEquals(now, n.lastRunAt);
        assertEquals(initial.totalRunCount + 1, n.totalRunCount);

        RedBeatSchedulerEntryStub loaded = RedBeatSchedulerEntryStub.fromKey(initial.key, app);
        assertEquals(now, loaded.lastRunAt);
        assertEquals(initial.totalRunCount + 1, loaded.totalRunCount);

        assertEquals(n.score, redis.zscore(app.redbeatConf.scheduleKey, n.key));
    }

    @Test
    public void testNextOnlyUpdateLastRunAt() {
        RedBeatSchedulerEntryStub initial = createEntry("public_next_only_update", "tasks.public_next_only_update");
        RedBeatSchedulerEntryStub n = initial.nextOnlyUpdateLastRunAt();
        assertTrue(n.lastRunAt.isAfter(initial.lastRunAt));
        assertEquals(initial.totalRunCount, n.totalRunCount);
    }

    @Test
    public void testDelete() throws Exception {
        RedBeatSchedulerEntryStub initial = createEntry("public_delete", "tasks.public_delete");
        initial.save();
        RedBeatSchedulerEntryStub e = RedBeatSchedulerEntryStub.fromKey(initial.key, app);
        e.delete();
        assertFalse(redis.exists(initial.key));
        assertNull(redis.zrank(app.redbeatConf.scheduleKey, initial.key));
    }

    @Test
    public void testDueAtNeverRun() {
        RedBeatSchedulerEntryStub entry = createEntry("public_never_run", "tasks.public_never_run");
        entry.lastRunAt = LocalDateTime.MIN;
        LocalDateTime before = entry.defaultNow();
        LocalDateTime dueAt = entry.getDueAt();
        LocalDateTime after = entry.defaultNow();
        assertTrue(before.isBefore(dueAt));
        assertTrue(dueAt.isBefore(after));
    }

    @Test
    public void testDueAt() {
        RedBeatSchedulerEntryStub entry = createEntry("due_at_public", "tasks.due_at_public");
        LocalDateTime now = entry.defaultNow();
        entry.lastRunAt = now;
        LocalDateTime dueAt = entry.getDueAt();
        assertTrue(now.isBefore(dueAt));
        assertTrue(dueAt.isBefore(now.plus(entry.schedule.getRunEvery())));
    }

    @Test
    public void testDueAtOverdue() {
        LocalDateTime lastRunAt = app.now().minusHours(8);
        RedBeatSchedulerEntryStub entry = createEntry("public_due_at_overdue", "tasks.public_due_at_overdue");
        entry.lastRunAt = lastRunAt;
        LocalDateTime before = entry.defaultNow();
        LocalDateTime dueAt = entry.getDueAt();
        assertTrue(lastRunAt.isBefore(dueAt));
        assertTrue(dueAt.isAfter(before));
    }

    @Test
    public void testScore() {
        int runEvery = 123 * 60;
        RedBeatSchedulerEntryStub entry = createEntry("public_score", "tasks.public_score");
        entry.schedule = new ScheduleStub(runEvery, false);
        entry = entry.nextInstance();
        long score = entry.score;
        LocalDateTime expected = entry.lastRunAt.plusSeconds(runEvery).withNano(0);
        assertEquals(score, RedBeatStubHelpers.toTimestamp(expected));
        assertEquals(expected, RedBeatStubHelpers.fromTimestamp(score));
    }

    @Test
    public void testGenerateKey() {
        RedBeatSchedulerEntryStub entry = createEntry("public_generate_key", "tasks.public_generate_key");
        String key = entry.generateKey(app, "another_public_name");
        assertEquals("redbeat:another_public_name", key);
    }

    @Test
    public void testKeyUsesGenerateKey() {
        RedBeatSchedulerEntryStub entry = createEntry("public_key", "tasks.public_key");
        RedBeatSchedulerEntryStub spyEntry = spy(entry);
        spyEntry.getKey();
        verify(spyEntry, atLeastOnce()).generateKey(app, "public_key");
    }
}
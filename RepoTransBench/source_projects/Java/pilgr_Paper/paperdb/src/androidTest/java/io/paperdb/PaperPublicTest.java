package io.paperdb;

import android.os.SystemClock;
import androidx.test.ext.junit.runners.AndroidJUnit4;

import org.joda.time.DateTime;
import org.joda.time.DateTimeZone;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;

import java.util.List;

import de.javakaffee.kryoserializers.jodatime.JodaDateTimeSerializer;
import io.paperdb.testdata.TestDataGenerator;

import static androidx.test.InstrumentationRegistry.getTargetContext;
import static junit.framework.Assert.assertEquals;
import static junit.framework.TestCase.assertTrue;
import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotEquals;
import static org.junit.Assert.assertNotNull;

@RunWith(AndroidJUnit4.class)
public class PaperPublicTest {

    @Before
    public void setUp() throws Exception {
        Paper.init(getTargetContext());
        Paper.book().destroy();
    }

    @Test
    public void testContains_public() throws Exception {
        assertFalse(Paper.book().contains("cities"));
        Paper.book().write("cities", TestDataGenerator.genPersonList(5));
        assertTrue(Paper.book().contains("cities"));
    }

    @Test
    public void testDelete_public() throws Exception {
        Paper.book().write("countries", TestDataGenerator.genPersonList(2));
        assertTrue(Paper.book().contains("countries"));
        Paper.book().delete("countries");
        assertFalse(Paper.book().contains("countries"));
    }

    @Test
    public void testDeleteNotExisted_public() throws Exception {
        assertFalse(Paper.book().contains("cities"));
        Paper.book().delete("cities");
    }

    @Test
    public void testClear_public() throws Exception {
        Paper.book().write("kings", TestDataGenerator.genPersonList(2));
        Paper.book().write("queens", TestDataGenerator.genPersonList(4));
        assertTrue(Paper.book().contains("kings"));
        assertTrue(Paper.book().contains("queens"));

        Paper.book().destroy();
        assertFalse(Paper.book().contains("kings"));
        assertFalse(Paper.book().contains("queens"));

        Paper.book().write("lords", TestDataGenerator.genPersonList(6));
        assertTrue(Paper.book().contains("lords"));
        assertThat(Paper.book().<List>read("lords")).hasSize(6);
    }

    @Test
    public void testWriteReadNormal_public() {
        Paper.book().write("fruit", "Apple");
        String val = Paper.book().read("fruit", "Banana");
        assertThat(val).isEqualTo("Apple");
    }

    @Test
    public void testWriteReadNormalAfterReinit_public() {
        Paper.book().write("drink", "Water");
        String val = Paper.book().read("drink", "Tea");
        Paper.init(getTargetContext());
        assertThat(val).isEqualTo("Water");
    }

    @Test
    public void testReadNotExisted_public() {
        String val = Paper.book().read("unknown-key");
        assertThat(val).isNull();
    }

    @Test
    public void testReadDefault_public() {
        String val = Paper.book().read("missing-key", "fallback");
        assertThat(val).isEqualTo("fallback");
    }

    @Test(expected = PaperDbException.class)
    public void testWriteNull_public() {
        Paper.book().write("empty_val", null);
    }

    @Test
    public void testReplace_public() {
        Paper.book().write("flower", "Rose");
        assertThat(Paper.book().read("flower")).isEqualTo("Rose");
        Paper.book().write("flower", "Tulip");
        assertThat(Paper.book().read("flower")).isEqualTo("Tulip");
    }

    @Test
    public void testValidKeyNames_public() {
        Paper.book().write("animal", "Lion");
        assertThat(Paper.book().read("animal")).isEqualTo("Lion");

        Paper.book().write("animal.info$@", "Lion");
        assertThat(Paper.book().read("animal.info$@")).isEqualTo("Lion");

        Paper.book().write("creature-123", "Tiger");
        assertThat(Paper.book().read("creature-123")).isEqualTo("Tiger");
    }

    @Test(expected = PaperDbException.class)
    public void testInvalidKeyNameBackslash_public() {
        Paper.book().write("key/with/slash", "Value");
        assertThat(Paper.book().read("key/with/slash")).isEqualTo("Value");
    }

    @Test(expected = PaperDbException.class)
    public void testGetBookWithDefaultBookName_public() {
        Paper.book(Paper.DEFAULT_DB_NAME);
    }

    @Test
    public void testCustomBookReadWrite_public() {
        final String ALT = "alternate";
        assertThat(Paper.book()).isNotSameAs(Paper.book(ALT));
        Paper.book(ALT).destroy();

        Paper.book().write("river", "Amazon");
        Paper.book(ALT).write("river", "Nile");

        assertThat(Paper.book().read("river")).isEqualTo("Amazon");
        assertThat(Paper.book(ALT).read("river")).isEqualTo("Nile");
    }

    @Test
    public void testCustomBookDestroy_public() {
        final String ALT = "alternate";
        Paper.book(ALT).destroy();

        Paper.book().write("river", "Ganges");
        Paper.book(ALT).write("river", "Thames");

        Paper.book(ALT).destroy();

        assertThat(Paper.book().read("river")).isEqualTo("Ganges");
        assertThat(Paper.book(ALT).read("river")).isNull();
    }

    @Test
    public void testGetAllKeys_public() {
        Paper.book().destroy();

        Paper.book().write("ocean", "Pacific");
        Paper.book().write("ocean2", "Atlantic");
        Paper.book().write("ocean3", "Indian");
        List<String> allKeys = Paper.book().getAllKeys();

        assertThat(allKeys.size()).isEqualTo(3);
        assertThat(allKeys.contains("ocean")).isTrue();
        assertThat(allKeys.contains("ocean2")).isTrue();
        assertThat(allKeys.contains("ocean3")).isTrue();
    }

    @Test
    public void testCustomSerializer_public() {
        Paper.addSerializer(DateTime.class, new JodaDateTimeSerializer());
        DateTime now = DateTime.now(DateTimeZone.UTC).plusDays(1);

        Paper.book().write("dt1", now);
        assertEquals(now, Paper.book().read("dt1"));
    }

    @Test
    public void testTimestampNoObject_public() {
        Paper.book().destroy();
        long timestamp = Paper.book().lastModified("nothing_here");
        assertEquals(-1, timestamp);
    }

    @Test
    public void testTimestamp_public() {
        long testStartMS = System.currentTimeMillis();

        Paper.book().destroy();
        Paper.book().write("continent", "Asia");

        long fileWriteMS = Paper.book().lastModified("continent");
        assertNotEquals(-1, fileWriteMS);

        long elapsed = fileWriteMS - testStartMS;
        assertThat(elapsed).isGreaterThanOrEqualTo(0);
        assertNotNull(Paper.book().read("continent"));
    }
}
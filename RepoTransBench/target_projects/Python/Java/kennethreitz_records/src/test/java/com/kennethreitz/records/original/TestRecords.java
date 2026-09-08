package com.kennethreitz.records.original;

import com.kennethreitz.records.RecordCollection;
import com.kennethreitz.records.Record;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.function.Executable;

import java.util.*;
import static org.junit.jupiter.api.Assertions.*;

class IdRecord {
    public int id;
    public IdRecord(int id) { this.id = id; }
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof IdRecord)) return false;
        IdRecord other = (IdRecord) o;
        return this.id == other.id;
    }
    @Override
    public int hashCode() {
        return Integer.hashCode(id);
    }
}

public class TestRecords {

    static void checkId(int i, IdRecord row) {
        assertEquals(i, row.id);
    }

    @Test
    public void testIter() {
        RecordCollection<IdRecord> rows = new RecordCollection<>(() -> new Iterator<IdRecord>() {
            int i = 0, max = 10;
            public boolean hasNext() { return i < max; }
            public IdRecord next() { return new IdRecord(i++); }
        });
        int idx = 0;
        for (IdRecord row : rows)
            checkId(idx++, row);
        assertEquals(10, idx);
    }

    @Test
    public void testNext() {
        RecordCollection<IdRecord> rows = new RecordCollection<>(() -> new Iterator<IdRecord>() {
            int i = 0;
            public boolean hasNext() { return i < 10; }
            public IdRecord next() { return new IdRecord(i++); }
        });
        for (int i = 0; i < 10; i++)
            checkId(i, rows.next());
    }

    @Test
    public void testIterAndNext() {
        RecordCollection<IdRecord> rows = new RecordCollection<>(() -> new Iterator<IdRecord>() {
            int i = 0;
            public boolean hasNext() { return i < 10; }
            public IdRecord next() { return new IdRecord(i++); }
        });
        Iterator<IdRecord> it = rows.iterator();
        int idx1 = 0;
        checkId(idx1++, it.next());
        rows.next(); // cache second row
        checkId(idx1++, it.next()); // read from cache
    }

    @Test
    public void testMultipleIter() {
        RecordCollection<IdRecord> rows = new RecordCollection<>(() -> new Iterator<IdRecord>() {
            int i = 0;
            public boolean hasNext() { return i < 10; }
            public IdRecord next() { return new IdRecord(i++); }
        });
        Iterator<IdRecord> i = rows.iterator();
        Iterator<IdRecord> j = rows.iterator();
        int idx = 0;
        checkId(idx++, i.next());
        checkId(0, j.next());
        checkId(1, j.next());
        checkId(idx++, i.next());
    }

    @Test
    public void testSliceIter() {
        RecordCollection<IdRecord> rows = new RecordCollection<>(() -> new Iterator<IdRecord>() {
            int i = 0;
            public boolean hasNext() { return i < 10; }
            public IdRecord next() { return new IdRecord(i++); }
        });

        List<IdRecord> firstFive = rows.slice(0, 5);
        assertEquals(5, firstFive.size());
        for (int i = 0; i < firstFive.size(); i++)
            checkId(i, firstFive.get(i));
        int size = 0;
        for (IdRecord r : rows)
            checkId(size++, r);
        assertEquals(10, rows.size());
    }

    @Test
    public void testAllReturnsAListOfRecords() {
        List<IdRecord> expected = List.of(new IdRecord(0), new IdRecord(1), new IdRecord(2));
        RecordCollection<IdRecord> rows = new RecordCollection<>(List.of(new IdRecord(0), new IdRecord(1), new IdRecord(2)));
        assertEquals(expected, rows.all());
    }

    @Test
    public void testFirstReturnsASingleRecord() {
        RecordCollection<IdRecord> rows = new RecordCollection<>(List.of(new IdRecord(0)));
        assertEquals(new IdRecord(0), rows.first());
    }

    @Test
    public void testFirstDefaultsToNull() {
        RecordCollection<IdRecord> rows = new RecordCollection<>(Collections.emptyList());
        assertNull(rows.first());
    }

    @Test
    public void testFirstDefaultIsOverridable() {
        RecordCollection<IdRecord> rows = new RecordCollection<>(Collections.emptyList());
        assertEquals("Cheese", rows.first("Cheese"));
    }

    @Test
    public void testFirstRaisesDefaultIfItsAnExceptionSubclass() {
        RecordCollection<IdRecord> rows = new RecordCollection<>(Collections.emptyList());
        class CheeseException extends RuntimeException {}
        assertThrows(CheeseException.class, () -> rows.firstError(CheeseException.class));
    }

    @Test
    public void testFirstRaisesDefaultIfItsAnExceptionInstance() {
        RecordCollection<IdRecord> rows = new RecordCollection<>(Collections.emptyList());
        class CheeseException extends RuntimeException {
            public CheeseException(String msg) { super(msg); }
        }
        assertThrows(CheeseException.class, () -> rows.firstError(new CheeseException("cheddar")));
    }

    @Test
    public void testOneReturnsASingleRecord() {
        RecordCollection<IdRecord> rows = new RecordCollection<>(List.of(new IdRecord(0)));
        assertEquals(new IdRecord(0), rows.one());
    }

    @Test
    public void testOneDefaultsToNull() {
        RecordCollection<IdRecord> rows = new RecordCollection<>(Collections.emptyList());
        assertNull(rows.one());
    }

    @Test
    public void testOneDefaultIsOverridable() {
        RecordCollection<IdRecord> rows = new RecordCollection<>(Collections.emptyList());
        assertEquals("Cheese", rows.one("Cheese"));
    }

    @Test
    public void testOneRaisesWhenMoreThanOne() {
        RecordCollection<IdRecord> rows = new RecordCollection<>(List.of(new IdRecord(0), new IdRecord(1), new IdRecord(2)));
        assertThrows(IllegalArgumentException.class, rows::one);
    }

    @Test
    public void testOneRaisesDefaultIfItsAnExceptionSubclass() {
        RecordCollection<IdRecord> rows = new RecordCollection<>(Collections.emptyList());
        class CheeseException extends RuntimeException {}
        assertThrows(CheeseException.class, () -> rows.oneError(CheeseException.class));
    }

    @Test
    public void testOneRaisesDefaultIfItsAnExceptionInstance() {
        RecordCollection<IdRecord> rows = new RecordCollection<>(Collections.emptyList());
        class CheeseException extends RuntimeException {
            public CheeseException(String msg) { super(msg); }
        }
        assertThrows(CheeseException.class, () -> rows.oneError(new CheeseException("cheddar")));
    }

    @Test
    public void testScalarReturnsASingleRecord() {
        RecordCollection<IdRecord> rows = new RecordCollection<>(List.of(new IdRecord(0)));
        assertEquals(0, rows.scalar());
    }

    @Test
    public void testScalarDefaultsToNull() {
        RecordCollection<IdRecord> rows = new RecordCollection<>(Collections.emptyList());
        assertNull(rows.scalar());
    }

    @Test
    public void testScalarDefaultIsOverridable() {
        RecordCollection<IdRecord> rows = new RecordCollection<>(Collections.emptyList());
        assertEquals("Kaffe", rows.scalar("Kaffe"));
    }

    @Test
    public void testScalarRaisesWhenMoreThanOne() {
        RecordCollection<IdRecord> rows = new RecordCollection<>(List.of(new IdRecord(0), new IdRecord(1), new IdRecord(2)));
        assertThrows(IllegalArgumentException.class, rows::scalar);
    }

    public static class RecordTest {
        @Test
        public void testRecordDir() {
            List<String> keys = Arrays.asList("id", "name", "email");
            List<Object> values = Arrays.asList(1, "", "");
            Record record = new Record(keys, values);
            Set<String> memberSet = record.members();
            for (String key : keys) {
                assertTrue(memberSet.contains(key));
            }
        }

        @Test
        public void testRecordDuplicateColumn() {
            List<String> keys = Arrays.asList("id", "name", "email", "email");
            List<Object> values = Arrays.asList(1, "", "", "");
            Record record = new Record(keys, values);
            assertThrows(IllegalArgumentException.class, () -> record.get("email"));
        }
    }
}
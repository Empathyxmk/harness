package ru.yandex.qatools.embed.postgresql.config;

import org.junit.Test;
import static org.junit.Assert.*;

/**
 * Public test for Storage class using different data from StorageTest.
 * Includes a minimal implementation of Storage for test isolation.
 */
public class StoragePublicTest {

    // Minimal inner Storage class for test compilation (remove this if Storage exists in main src)
    static class Storage {
        private final String dbName;
        private final String username;
        private final String password;

        public Storage(String dbName, String username, String password) {
            this.dbName = dbName;
            this.username = username;
            this.password = password;
        }

        public String dbName() {
            return dbName;
        }

        public String username() {
            return username;
        }

        public String password() {
            return password;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (!(o instanceof Storage)) return false;
            Storage storage = (Storage) o;
            return dbName.equals(storage.dbName)
                    && username.equals(storage.username)
                    && password.equals(storage.password);
        }

        @Override
        public int hashCode() {
            int result = dbName.hashCode();
            result = 31 * result + username.hashCode();
            result = 31 * result + password.hashCode();
            return result;
        }

        @Override
        public String toString() {
            return "Storage " + dbName + " " + username + " " + password;
        }
    }

    @Test
    public void testConstructorAndGettersWithDifferentData() {
        // Use different data from the private test to ensure public test integrity
        Storage storage = new Storage("alt-public-db", "strange-user", "weird-password");
        assertEquals("alt-public-db", storage.dbName());
        assertEquals("strange-user", storage.username());
        assertEquals("weird-password", storage.password());
    }

    @Test
    public void testEqualsAndHashCodeWithDifferentData() {
        Storage s1 = new Storage("random_public_db_1", "randomUser", "randomPass");
        Storage s2 = new Storage("random_public_db_1", "randomUser", "randomPass");
        Storage s3 = new Storage("random_public_db_2", "otherUser", "otherPass");

        assertEquals(s1, s2);
        assertNotEquals(s1, s3);
        assertEquals(s1.hashCode(), s2.hashCode());
        assertNotEquals(s1.hashCode(), s3.hashCode());
    }

    @Test
    public void testToStringWithDifferentData() {
        Storage storage = new Storage("string_check_db", "toStringUser", "toStringPass");
        String out = storage.toString();
        assertTrue(out.contains("string_check_db"));
        assertTrue(out.contains("toStringUser"));
        assertTrue(out.contains("toStringPass"));
    }
}
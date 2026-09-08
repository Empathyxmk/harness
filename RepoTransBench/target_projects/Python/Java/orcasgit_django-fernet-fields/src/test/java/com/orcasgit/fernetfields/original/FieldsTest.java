package com.orcasgit.fernetfields.original;

import com.orcasgit.fernetfields.EncryptedTextField;
import com.orcasgit.fernetfields.EncryptedCharField;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import static org.junit.jupiter.api.Assertions.*;

public class FieldsTest {

    @Test
    public void testEncryptedField() {
        String value = "Secret Data";
        EncryptedTextField field = new EncryptedTextField();
        Object enc = field.getPrepValue(value);
        String dec = field.fromDbValue(enc, null, null, null);
        assertEquals(value, dec);
    }

    @Test
    public void testEncryptedCharField() {
        String value = "HelloWorld";
        EncryptedCharField field = new EncryptedCharField(32);
        Object enc = field.getPrepValue(value);
        String dec = field.fromDbValue(enc, null, null, null);
        assertEquals(value, dec);
    }

    @Test
    public void testEncryptedFieldEmptyString() {
        String value = "";
        EncryptedTextField field = new EncryptedTextField();
        Object enc = field.getPrepValue(value);
        String dec = field.fromDbValue(enc, null, null, null);
        assertEquals("", dec);
    }

    @ParameterizedTest
    @ValueSource(strings = { "the quick brown fox", "test_string_value", "another test message" })
    public void testEncryptedFieldParametrize(String val) {
        EncryptedTextField field = new EncryptedTextField();
        Object enc = field.getPrepValue(val);
        String dec = field.fromDbValue(enc, null, null, null);
        assertEquals(val, dec);
    }
}
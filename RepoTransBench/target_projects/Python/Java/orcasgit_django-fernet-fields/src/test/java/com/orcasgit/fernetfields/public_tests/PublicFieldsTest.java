package com.orcasgit.fernetfields.public_tests;

import com.orcasgit.fernetfields.EncryptedTextField;
import com.orcasgit.fernetfields.EncryptedCharField;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import static org.junit.jupiter.api.Assertions.*;

public class PublicFieldsTest {

    @Test
    public void testEncryptedFieldBasic() {
        String value = "This is secret data for pub";
        EncryptedTextField field = new EncryptedTextField();
        Object enc = field.getPrepValue(value);
        String dec = field.fromDbValue(enc, null, null, null);
        assertEquals(value, dec);
    }

    @Test
    public void testEncryptedCharField() {
        String value = "AlphaBravo";
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
    @ValueSource(strings = { "fox jumps over the lazy dog", "crazy_test_value_PUBLIC_CASE", "another secret message" })
    public void testEncryptedFieldParametrize(String val) {
        EncryptedTextField field = new EncryptedTextField();
        Object enc = field.getPrepValue(val);
        String dec = field.fromDbValue(enc, null, null, null);
        assertEquals(val, dec);
    }
}
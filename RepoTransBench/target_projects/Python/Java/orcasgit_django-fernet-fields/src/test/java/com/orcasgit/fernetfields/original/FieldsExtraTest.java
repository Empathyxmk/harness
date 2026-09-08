package com.orcasgit.fernetfields.original;

import com.orcasgit.fernetfields.FernetField;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import static org.junit.jupiter.api.Assertions.*;

public class FieldsExtraTest {

    @Test
    public void testFernetFieldEncryptDecrypt() {
        FernetField field = new FernetField();
        byte[] data = "SensitiveData123".getBytes();
        Object encrypted = field.getPrepValue(data);
        byte[] decrypted = field.fromDbValue(encrypted, null, null, null);
        assertArrayEquals(data, decrypted);
    }

    @Test
    public void testFernetFieldDifferentData() {
        FernetField field = new FernetField();
        byte[] value = "AnotherSecret".getBytes();
        Object encrypted = field.getPrepValue(value);
        byte[] decrypted = field.fromDbValue(encrypted, null, null, null);
        assertArrayEquals(value, decrypted);
    }

    @Test
    public void testFernetFieldHandlesEmptyBytes() {
        FernetField field = new FernetField();
        byte[] value = new byte[0];
        Object encrypted = field.getPrepValue(value);
        byte[] decrypted = field.fromDbValue(encrypted, null, null, null);
        assertArrayEquals(new byte[0], decrypted);
    }

    @ParameterizedTest
    @ValueSource(strings = { "param_1", "param_2", "param_3" })
    public void testFernetFieldParametrize(String stringVal) {
        FernetField field = new FernetField();
        byte[] val = stringVal.getBytes();
        Object encrypted = field.getPrepValue(val);
        byte[] decrypted = field.fromDbValue(encrypted, null, null, null);
        assertArrayEquals(val, decrypted);
    }
}
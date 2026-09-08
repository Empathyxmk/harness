package com.orcasgit.fernetfields.public_tests;

import com.orcasgit.fernetfields.FernetField;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import static org.junit.jupiter.api.Assertions.*;

public class PublicFieldsExtraTest {

    @Test
    public void testFernetFieldEncryptDecrypt() {
        FernetField field = new FernetField();
        byte[] data = "SensitivePublicData123".getBytes();
        Object encrypted = field.getPrepValue(data);
        byte[] decrypted = field.fromDbValue(encrypted, null, null, null);
        assertArrayEquals(data, decrypted);
    }

    @Test
    public void testFernetFieldDifferentData() {
        FernetField field = new FernetField();
        byte[] value = "UniqueBytesForPublicTest".getBytes();
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
    @ValueSource(strings = { "public_param_1", "another_param_public_2", "extra_data_public_3" })
    public void testFernetFieldParametrize(String stringVal) {
        FernetField field = new FernetField();
        byte[] val = stringVal.getBytes();
        Object encrypted = field.getPrepValue(val);
        byte[] decrypted = field.fromDbValue(encrypted, null, null, null);
        assertArrayEquals(val, decrypted);
    }
}
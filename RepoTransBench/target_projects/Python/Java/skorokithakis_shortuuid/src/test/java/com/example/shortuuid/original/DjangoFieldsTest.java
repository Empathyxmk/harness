package com.example.shortuuid.original;

import org.junit.jupiter.api.*;
import org.mockito.MockedStatic;
import org.mockito.Mockito;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import com.example.shortuuid.django_fields.ShortUUIDField;

class DummySuper {
    String name = "name";
    String path = "path";
    Object[] args = new Object[0];
    java.util.Map<String, Object> kwargs = new java.util.HashMap<>();
    public Object[] deconstruct() { return new Object[]{"name", "path", args, kwargs}; }
}

class DummyShortUUID {
    public DummyShortUUID(String alphabet, boolean dontSortAlphabet) {}
    public String random(int length) { return "X".repeat(length); }
}

class DjangoFieldsTest {

    @Test
    void testShortuuidFieldDeconstructAndGenerate() {
        try (MockedStatic<com.example.shortuuid.django_fields.models.CharField> superField =
                     Mockito.mockStatic(com.example.shortuuid.django_fields.models.CharField.class)) {
            superField.when(() -> com.example.shortuuid.django_fields.models.CharField.class).thenReturn(DummySuper.class);

            try (MockedStatic<com.example.shortuuid.django_fields.ShortUUID> shortUuidMock =
                         Mockito.mockStatic(com.example.shortuuid.django_fields.ShortUUID.class)) {
                shortUuidMock.when(() -> com.example.shortuuid.django_fields.ShortUUID.class)
                        .thenReturn(DummyShortUUID.class);

                ShortUUIDField field = new ShortUUIDField(5, "PRE_", "abc", true);
                String val = field._generateUuid();
                assertEquals("PRE_" + "X".repeat(5), val);

                Object[] deconstructed = field.deconstruct();
                @SuppressWarnings("unchecked")
                java.util.Map<String, Object> kwargs = (java.util.Map<String, Object>)deconstructed[3];

                assertEquals(5, kwargs.get("length"));
                assertEquals("PRE_", kwargs.get("prefix"));
                assertEquals("abc", kwargs.get("alphabet"));
                assertFalse(kwargs.containsKey("default"));
            }
        }
    }

    @Test
    void testShortuuidFieldDefaultMaxLengthAndArgs() {
        ShortUUIDField field = new ShortUUIDField(6, "Q_", "123", false);
        assertEquals(6, field.getLength());
        assertEquals("Q_", field.getPrefix());
        assertEquals("123", field.getAlphabet());
        assertTrue(field.hasMaxLength());
    }
}
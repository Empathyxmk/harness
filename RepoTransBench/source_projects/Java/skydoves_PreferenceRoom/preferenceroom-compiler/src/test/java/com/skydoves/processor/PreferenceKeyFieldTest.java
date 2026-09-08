package com.skydoves.processor;

import com.skydoves.preferenceroom.KeyName;
import com.skydoves.preferenceroom.TypeConverter;
import com.squareup.javapoet.TypeName;
import org.junit.Before;
import org.junit.Test;

import javax.lang.model.element.Modifier;
import javax.lang.model.element.PackageElement;
import javax.lang.model.element.VariableElement;
import javax.lang.model.util.Elements;

import java.lang.annotation.Annotation;
import java.util.Collections;
import java.util.Set;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class PreferenceKeyFieldTest {

    Elements elementUtils;
    VariableElement element;
    PackageElement pkgElement;

    @Before
    public void setup() {
        elementUtils = mock(Elements.class);
        element = mock(VariableElement.class);
        pkgElement = mock(PackageElement.class);
        when(elementUtils.getPackageOf(element)).thenReturn(pkgElement);
        when(pkgElement.isUnnamed()).thenReturn(false);
        when(pkgElement.getQualifiedName()).thenReturn(new javax.lang.model.element.Name() {
            public boolean contentEquals(CharSequence cs) {return "com.test".contentEquals(cs);}
            public int length() { return "com.test".length(); }
            public char charAt(int index) { return "com.test".charAt(index);}
            public CharSequence subSequence(int start, int end) { return "com.test".subSequence(start, end);}
            public String toString() { return "com.test"; }
        });
    }

    @Test
    public void testBooleanField() throws IllegalAccessException {
        when(element.getAnnotation(KeyName.class)).thenReturn(null);
        when(element.asType()).thenReturn(javax.lang.model.type.TypeKind.BOOLEAN.ordinal() == 0 ? TypeName.BOOLEAN : null);
        when(element.getSimpleName()).thenReturn(new javax.lang.model.element.Name() {
            public boolean contentEquals(CharSequence cs) {return "flag".contentEquals(cs);}
            public int length() { return "flag".length(); }
            public char charAt(int index) { return "flag".charAt(index);}
            public CharSequence subSequence(int start, int end) { return "flag".subSequence(start, end);}
            public String toString() { return "flag"; }
        });
        when(element.getConstantValue()).thenReturn(true);
        when(element.getModifiers()).thenReturn(Collections.singleton(Modifier.FINAL));

        PreferenceKeyField field = new PreferenceKeyField(element, elementUtils);
        assertEquals("Boolean", field.typeStringName);
        assertEquals("Flag", field.keyName);
        assertEquals("flag", field.clazzName);
    }

    @Test
    public void testStringFieldWithCustomKeyName() throws IllegalAccessException {
        KeyName keyNameAnnotation = mock(KeyName.class);
        when(keyNameAnnotation.value()).thenReturn("customKey");
        when(element.getAnnotation(KeyName.class)).thenReturn(keyNameAnnotation);
        when(element.asType()).thenReturn(TypeName.get(String.class));
        when(element.getSimpleName()).thenReturn(new javax.lang.model.element.Name() {
            public boolean contentEquals(CharSequence cs) {return "username".contentEquals(cs);}
            public int length() { return "username".length(); }
            public char charAt(int index) { return "username".charAt(index);}
            public CharSequence subSequence(int start, int end) { return "username".subSequence(start, end);}
            public String toString() { return "username"; }
        });
        when(element.getConstantValue()).thenReturn("admin");
        when(element.getModifiers()).thenReturn(Collections.singleton(Modifier.FINAL));

        PreferenceKeyField field = new PreferenceKeyField(element, elementUtils);
        assertEquals("customKey", field.keyName);
        assertEquals("String", field.typeStringName);
    }

    @Test(expected = IllegalAccessException.class)
    public void testPrivateFieldThrows() throws IllegalAccessException {
        when(element.getAnnotation(KeyName.class)).thenReturn(null);
        when(element.asType()).thenReturn(TypeName.BOOLEAN);
        when(element.getSimpleName()).thenReturn(new javax.lang.model.element.Name() {
            public boolean contentEquals(CharSequence cs) {return "flag".contentEquals(cs);}
            public int length() { return "flag".length(); }
            public char charAt(int index) { return "flag".charAt(index);}
            public CharSequence subSequence(int start, int end) { return "flag".subSequence(start, end);}
            public String toString() { return "flag"; }
        });
        when(element.getModifiers()).thenReturn(Collections.singleton(Modifier.PRIVATE));
        when(element.getConstantValue()).thenReturn(true);

        new PreferenceKeyField(element, elementUtils);
    }

    @Test(expected = IllegalAccessException.class)
    public void testNonFinalFieldThrows() throws IllegalAccessException {
        when(element.getAnnotation(KeyName.class)).thenReturn(null);
        when(element.asType()).thenReturn(TypeName.BOOLEAN);
        when(element.getSimpleName()).thenReturn(new javax.lang.model.element.Name() {
            public boolean contentEquals(CharSequence cs) {return "flag".contentEquals(cs);}
            public int length() { return "flag".length(); }
            public char charAt(int index) { return "flag".charAt(index);}
            public CharSequence subSequence(int start, int end) { return "flag".subSequence(start, end);}
            public String toString() { return "flag"; }
        });
        when(element.getModifiers()).thenReturn(Collections.emptySet());
        when(element.getConstantValue()).thenReturn(true);

        new PreferenceKeyField(element, elementUtils);
    }
}
package com.skydoves.processor;

import com.skydoves.preferenceroom.KeyName;
import com.squareup.javapoet.TypeName;
import org.junit.Before;
import org.junit.Test;
import javax.lang.model.element.Modifier;
import javax.lang.model.element.PackageElement;
import javax.lang.model.element.VariableElement;
import javax.lang.model.util.Elements;
import static org.junit.Assert.*;
import static org.mockito.Mockito.*;
import java.util.Collections;

public class PreferenceKeyFieldPublicTest {

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
            public boolean contentEquals(CharSequence cs) {return "com.publictest".contentEquals(cs);}
            public int length() { return "com.publictest".length(); }
            public char charAt(int index) { return "com.publictest".charAt(index);}
            public CharSequence subSequence(int start, int end) { return "com.publictest".subSequence(start, end);}
            public String toString() { return "com.publictest"; }
        });
    }

    @Test
    public void testDifferentBooleanField() throws IllegalAccessException {
        when(element.getAnnotation(KeyName.class)).thenReturn(null);
        when(element.asType()).thenReturn(javax.lang.model.type.TypeKind.BOOLEAN.ordinal() == 0 ? TypeName.BOOLEAN : null);
        when(element.getSimpleName()).thenReturn(new javax.lang.model.element.Name() {
            public boolean contentEquals(CharSequence cs) {return "isActive".contentEquals(cs);}
            public int length() { return "isActive".length(); }
            public char charAt(int index) { return "isActive".charAt(index);}
            public CharSequence subSequence(int start, int end) { return "isActive".subSequence(start, end);}
            public String toString() { return "isActive"; }
        });
        when(element.getConstantValue()).thenReturn(false);
        when(element.getModifiers()).thenReturn(Collections.singleton(Modifier.FINAL));

        PreferenceKeyField field = new PreferenceKeyField(element, elementUtils);
        assertEquals("Boolean", field.typeStringName);
        assertEquals("IsActive", field.keyName);
        assertEquals("isActive", field.clazzName);
    }

    @Test
    public void testStringFieldWithAnotherCustomKeyName() throws IllegalAccessException {
        KeyName keyNameAnnotation = mock(KeyName.class);
        when(keyNameAnnotation.value()).thenReturn("anotherCustomKey");
        when(element.getAnnotation(KeyName.class)).thenReturn(keyNameAnnotation);
        when(element.asType()).thenReturn(TypeName.get(String.class));
        when(element.getSimpleName()).thenReturn(new javax.lang.model.element.Name() {
            public boolean contentEquals(CharSequence cs) {return "displayName".contentEquals(cs);}
            public int length() { return "displayName".length(); }
            public char charAt(int index) { return "displayName".charAt(index);}
            public CharSequence subSequence(int start, int end) { return "displayName".subSequence(start, end);}
            public String toString() { return "displayName"; }
        });
        when(element.getConstantValue()).thenReturn("public_admin");
        when(element.getModifiers()).thenReturn(Collections.singleton(Modifier.FINAL));

        PreferenceKeyField field = new PreferenceKeyField(element, elementUtils);
        assertEquals("anotherCustomKey", field.keyName);
        assertEquals("String", field.typeStringName);
    }

    @Test(expected = IllegalAccessException.class)
    public void testPrivateFieldThrowsPublic() throws IllegalAccessException {
        when(element.getAnnotation(KeyName.class)).thenReturn(null);
        when(element.asType()).thenReturn(TypeName.BOOLEAN);
        when(element.getSimpleName()).thenReturn(new javax.lang.model.element.Name() {
            public boolean contentEquals(CharSequence cs) {return "isActive".contentEquals(cs);}
            public int length() { return "isActive".length(); }
            public char charAt(int index) { return "isActive".charAt(index);}
            public CharSequence subSequence(int start, int end) { return "isActive".subSequence(start, end);}
            public String toString() { return "isActive"; }
        });
        when(element.getModifiers()).thenReturn(Collections.singleton(Modifier.PRIVATE));
        when(element.getConstantValue()).thenReturn(false);

        new PreferenceKeyField(element, elementUtils);
    }

    @Test(expected = IllegalAccessException.class)
    public void testNonFinalFieldThrowsPublic() throws IllegalAccessException {
        when(element.getAnnotation(KeyName.class)).thenReturn(null);
        when(element.asType()).thenReturn(TypeName.BOOLEAN);
        when(element.getSimpleName()).thenReturn(new javax.lang.model.element.Name() {
            public boolean contentEquals(CharSequence cs) {return "isActive".contentEquals(cs);}
            public int length() { return "isActive".length(); }
            public char charAt(int index) { return "isActive".charAt(index);}
            public CharSequence subSequence(int start, int end) { return "isActive".subSequence(start, end);}
            public String toString() { return "isActive"; }
        });
        when(element.getModifiers()).thenReturn(Collections.emptySet());
        when(element.getConstantValue()).thenReturn(false);

        new PreferenceKeyField(element, elementUtils);
    }
}
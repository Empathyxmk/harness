package com.skydoves.processor;

import com.google.common.base.VerifyException;
import com.skydoves.preferenceroom.DefaultPreference;
import com.skydoves.preferenceroom.PreferenceEntity;
import com.squareup.javapoet.TypeName;
import org.junit.Test;

import javax.lang.model.element.Element;
import javax.lang.model.element.PackageElement;
import javax.lang.model.element.TypeElement;
import javax.lang.model.util.Elements;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

import java.lang.annotation.Annotation;
import java.util.Collections;

public class PreferenceEntityAnnotatedClassTest {

    @Test(expected = VerifyException.class)
    public void testMissingEntityNameThrows() {
        TypeElement typeElement = mock(TypeElement.class);
        Elements elements = mock(Elements.class);
        PreferenceEntity annotation = mock(PreferenceEntity.class);

        when(typeElement.getAnnotation(PreferenceEntity.class)).thenReturn(annotation);
        when(annotation.value()).thenReturn("");
        when(typeElement.getSimpleName()).thenReturn(new javax.lang.model.element.Name() {
            @Override public boolean contentEquals(CharSequence cs) {return "MyPreference".contentEquals(cs);}
            @Override public int length() {return "MyPreference".length();}
            @Override public char charAt(int i) {return "MyPreference".charAt(i);}
            @Override public CharSequence subSequence(int start, int end) {return "MyPreference".subSequence(start,end);}
            @Override public String toString() {return "MyPreference";}
        });

        PackageElement pkg = mock(PackageElement.class);
        when(elements.getPackageOf(typeElement)).thenReturn(pkg);
        when(pkg.isUnnamed()).thenReturn(false);
        when(pkg.getQualifiedName()).thenReturn(new javax.lang.model.element.Name() {
            public boolean contentEquals(CharSequence cs) {return "pkg".contentEquals(cs);}
            public int length() { return "pkg".length(); }
            public char charAt(int index) { return "pkg".charAt(index);}
            public CharSequence subSequence(int start, int end) { return "pkg".subSequence(start, end);}
            public String toString() { return "pkg"; }
        });

        when(typeElement.getEnclosedElements()).thenReturn(Collections.emptyList());

        new PreferenceEntityAnnotatedClass(typeElement, elements);
    }

    @Test
    public void testWithDefaultPreferenceAndEncryptEntity() {
        TypeElement typeElement = mock(TypeElement.class);
        Elements elements = mock(Elements.class);

        PreferenceEntity pe = mock(PreferenceEntity.class);
        DefaultPreference dp = mock(DefaultPreference.class);
        com.skydoves.preferenceroom.EncryptEntity ee = mock(com.skydoves.preferenceroom.EncryptEntity.class);

        when(typeElement.getAnnotation(PreferenceEntity.class)).thenReturn(pe);
        when(typeElement.getAnnotation(DefaultPreference.class)).thenReturn(dp);
        when(typeElement.getAnnotation(com.skydoves.preferenceroom.EncryptEntity.class)).thenReturn(ee);
        when(typeElement.getSimpleName()).thenReturn(new javax.lang.model.element.Name() {
            @Override public boolean contentEquals(CharSequence cs) {return "NameA".contentEquals(cs);}
            @Override public int length() {return "NameA".length();}
            @Override public char charAt(int i) {return "NameA".charAt(i);}
            @Override public CharSequence subSequence(int start, int end) {return "NameA".subSequence(start,end);}
            @Override public String toString() {return "NameA";}
        });
        when(pe.value()).thenReturn("EntityX");
        when(elements.getPackageOf(typeElement)).thenReturn(mock(PackageElement.class));
        when(typeElement.getEnclosedElements()).thenReturn(Collections.emptyList());
        when(ee.value()).thenReturn("ENCRYPTED_VALUE");

        PreferenceEntityAnnotatedClass clz = new PreferenceEntityAnnotatedClass(typeElement, elements);
        assertEquals("EntityX", clz.entityName);
        assertTrue(clz.isDefaultPreference);
        assertTrue(clz.isEncryption);
        assertEquals("ENCRYPTED_VALUE", clz.encryptionKey);
    }
}
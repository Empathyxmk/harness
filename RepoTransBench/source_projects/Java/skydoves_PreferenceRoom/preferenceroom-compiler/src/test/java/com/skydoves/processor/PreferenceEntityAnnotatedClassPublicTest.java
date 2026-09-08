package com.skydoves.processor;

import com.google.common.base.VerifyException;
import com.skydoves.preferenceroom.DefaultPreference;
import com.skydoves.preferenceroom.PreferenceEntity;
import org.junit.Test;

import javax.lang.model.element.Element;
import javax.lang.model.element.PackageElement;
import javax.lang.model.element.TypeElement;
import javax.lang.model.util.Elements;
import static org.junit.Assert.*;
import static org.mockito.Mockito.*;
import java.util.Collections;

public class PreferenceEntityAnnotatedClassPublicTest {

    @Test(expected = VerifyException.class)
    public void testMissingEntityNameThrowsPublic() {
        TypeElement typeElement = mock(TypeElement.class);
        Elements elements = mock(Elements.class);
        PreferenceEntity annotation = mock(PreferenceEntity.class);

        // Use different class name and test value
        when(typeElement.getAnnotation(PreferenceEntity.class)).thenReturn(annotation);
        when(annotation.value()).thenReturn("");
        when(typeElement.getSimpleName()).thenReturn(new javax.lang.model.element.Name() {
            @Override public boolean contentEquals(CharSequence cs) {return "TestPreference".contentEquals(cs);}
            @Override public int length() {return "TestPreference".length();}
            @Override public char charAt(int i) {return "TestPreference".charAt(i);}
            @Override public CharSequence subSequence(int start, int end) {return "TestPreference".subSequence(start,end);}
            @Override public String toString() {return "TestPreference";}
        });

        PackageElement pkg = mock(PackageElement.class);
        when(elements.getPackageOf(typeElement)).thenReturn(pkg);
        when(pkg.isUnnamed()).thenReturn(false);
        when(pkg.getQualifiedName()).thenReturn(new javax.lang.model.element.Name() {
            public boolean contentEquals(CharSequence cs) {return "public.pkg".contentEquals(cs);}
            public int length() { return "public.pkg".length(); }
            public char charAt(int index) { return "public.pkg".charAt(index);}
            public CharSequence subSequence(int start, int end) { return "public.pkg".subSequence(start, end);}
            public String toString() { return "public.pkg"; }
        });

        when(typeElement.getEnclosedElements()).thenReturn(Collections.emptyList());

        new PreferenceEntityAnnotatedClass(typeElement, elements);
    }

    @Test
    public void testWithDifferentDefaultPreferenceAndEncryptEntity() {
        TypeElement typeElement = mock(TypeElement.class);
        Elements elements = mock(Elements.class);

        PreferenceEntity pe = mock(PreferenceEntity.class);
        DefaultPreference dp = mock(DefaultPreference.class);
        com.skydoves.preferenceroom.EncryptEntity ee = mock(com.skydoves.preferenceroom.EncryptEntity.class);

        when(typeElement.getAnnotation(PreferenceEntity.class)).thenReturn(pe);
        when(typeElement.getAnnotation(DefaultPreference.class)).thenReturn(dp);
        when(typeElement.getAnnotation(com.skydoves.preferenceroom.EncryptEntity.class)).thenReturn(ee);
        when(typeElement.getSimpleName()).thenReturn(new javax.lang.model.element.Name() {
            @Override public boolean contentEquals(CharSequence cs) {return "NameB".contentEquals(cs);}
            @Override public int length() {return "NameB".length();}
            @Override public char charAt(int i) {return "NameB".charAt(i);}
            @Override public CharSequence subSequence(int start, int end) {return "NameB".subSequence(start,end);}
            @Override public String toString() {return "NameB";}
        });
        when(pe.value()).thenReturn("EntityY");
        when(elements.getPackageOf(typeElement)).thenReturn(mock(PackageElement.class));
        when(typeElement.getEnclosedElements()).thenReturn(Collections.emptyList());
        when(ee.value()).thenReturn("PUBLIC_ENCRYPTED_VAL");

        PreferenceEntityAnnotatedClass clz = new PreferenceEntityAnnotatedClass(typeElement, elements);
        assertEquals("EntityY", clz.entityName);
        assertTrue(clz.isDefaultPreference);
        assertTrue(clz.isEncryption);
        assertEquals("PUBLIC_ENCRYPTED_VAL", clz.encryptionKey);
    }
}
package com.skydoves.processor;

import com.skydoves.preferenceroom.InjectPreference;
import com.skydoves.preferenceroom.PreferenceRoomImpl;
import com.squareup.javapoet.TypeSpec;

import org.junit.Test;

import javax.lang.model.element.TypeElement;
import javax.lang.model.util.Elements;

import java.util.Arrays;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class InjectorGeneratorTest {

    @Test
    public void generateClassNameTest() {
        PreferenceComponentAnnotatedClass pcac = mock(PreferenceComponentAnnotatedClass.class);
        TypeElement injectedElement = mock(TypeElement.class);
        Elements elementUtils = mock(Elements.class);

        when(injectedElement.getSimpleName()).thenReturn(new javax.lang.model.element.Name() {
            @Override public boolean contentEquals(CharSequence cs) { return "MyClass".contentEquals(cs);}
            @Override public int length() { return "MyClass".length();}
            @Override public char charAt(int index) { return "MyClass".charAt(index);}
            @Override public CharSequence subSequence(int start, int end) { return "MyClass".subSequence(start, end);}
            @Override public String toString() { return "MyClass";}
        });

        when(elementUtils.getPackageOf(injectedElement)).thenReturn(mock(javax.lang.model.element.PackageElement.class));

        InjectorGenerator generator = new InjectorGenerator(pcac, injectedElement, elementUtils);
        TypeSpec spec = generator.generate();

        assertEquals("MyClass_Injector", spec.name);
        assertTrue(spec.toString().contains("PreferenceRoom"));
    }
}
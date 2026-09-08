package com.skydoves.processor;

import com.skydoves.preferenceroom.InjectPreference;
import com.skydoves.preferenceroom.PreferenceRoomImpl;
import com.squareup.javapoet.TypeSpec;
import org.junit.Test;
import javax.lang.model.element.TypeElement;
import javax.lang.model.util.Elements;
import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class InjectorGeneratorPublicTest {

    @Test
    public void generateDifferentClassNameTest() {
        PreferenceComponentAnnotatedClass pcac = mock(PreferenceComponentAnnotatedClass.class);
        TypeElement injectedElement = mock(TypeElement.class);
        Elements elementUtils = mock(Elements.class);

        // Use different name for the injected class
        when(injectedElement.getSimpleName()).thenReturn(new javax.lang.model.element.Name() {
            @Override public boolean contentEquals(CharSequence cs) { return "PublicClass".contentEquals(cs);}
            @Override public int length() { return "PublicClass".length();}
            @Override public char charAt(int index) { return "PublicClass".charAt(index);}
            @Override public CharSequence subSequence(int start, int end) { return "PublicClass".subSequence(start, end);}
            @Override public String toString() { return "PublicClass";}
        });

        when(elementUtils.getPackageOf(injectedElement)).thenReturn(mock(javax.lang.model.element.PackageElement.class));

        InjectorGenerator generator = new InjectorGenerator(pcac, injectedElement, elementUtils);
        TypeSpec spec = generator.generate();

        assertEquals("PublicClass_Injector", spec.name);
        assertTrue(spec.toString().contains("PreferenceRoom"));
    }
}
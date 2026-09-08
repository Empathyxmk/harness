package com.netease.qa.testng;

import org.testng.annotations.ITestAnnotation;
import org.testng.IRetryAnalyzer;
import org.junit.*;
import static org.mockito.Mockito.*;

import java.lang.reflect.Method;
import java.lang.reflect.Constructor;

public class RetryListenerPublicTest {

    static class AnotherDummyTest {}

    @Test
    public void testTransformSetsRetryAnalyzerWhenNull() throws Exception {
        RetryListener listener = new RetryListener();
        ITestAnnotation annotation = mock(ITestAnnotation.class);
        when(annotation.getRetryAnalyzer()).thenReturn(null);

        listener.transform(annotation, AnotherDummyTest.class, (Constructor) null, (Method) null);
        verify(annotation).setRetryAnalyzer(TestngRetry.class);
    }

    @Test
    public void testTransformDoesNotOverrideIfAlreadySet() throws Exception {
        RetryListener listener = new RetryListener();
        ITestAnnotation annotation = mock(ITestAnnotation.class);
        IRetryAnalyzer mockedRetry = mock(IRetryAnalyzer.class);
        when(annotation.getRetryAnalyzer()).thenReturn(mockedRetry);

        listener.transform(annotation, AnotherDummyTest.class, (Constructor) null, (Method) null);
        verify(annotation, never()).setRetryAnalyzer(any());
    }
}
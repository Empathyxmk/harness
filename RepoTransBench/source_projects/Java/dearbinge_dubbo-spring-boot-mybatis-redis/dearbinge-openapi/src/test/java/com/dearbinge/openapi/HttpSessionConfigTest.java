package com.dearbinge.openapi;

import com.dearbinge.openapi.HttpSessionConfig;
import org.junit.jupiter.api.Test;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;

import static org.mockito.Mockito.*;

class HttpSessionConfigTest {

    @Test
    void testAddInterceptors() {
        HttpSessionConfig config = new HttpSessionConfig();
        InterceptorRegistry registry = mock(InterceptorRegistry.class);
        when(registry.addInterceptor(any())).thenReturn(null);
        config.addInterceptors(registry);
        verify(registry).addInterceptor(any());
    }
}
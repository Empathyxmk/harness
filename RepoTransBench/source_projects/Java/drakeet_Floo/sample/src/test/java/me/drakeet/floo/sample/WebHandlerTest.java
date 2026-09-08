package me.drakeet.floo.sample;

import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import me.drakeet.floo.Urls;

import org.junit.Before;
import org.junit.Test;
import org.mockito.ArgumentCaptor;
import org.mockito.Mockito;

import static org.junit.Assert.*;
import static org.mockito.Matchers.any;
import static org.mockito.Mockito.*;

public class WebHandlerTest {

    private Context context;
    private Bundle extras;
    private WebHandler handler;
    private Uri webUri;
    private Uri nonWebUri;

    @Before
    public void setUp() {
        context = mock(Context.class);
        extras = new Bundle();
        handler = new WebHandler();
        webUri = Uri.parse("https://example.com");
        nonWebUri = Uri.parse("foo://bar");
    }

    @Test
    public void testOnTargetNotFound_webScheme_withoutFlags() {
        boolean result = handler.onTargetNotFound(context, webUri, extras, null);
        assertTrue(result);
        // Should have started activity
        verify(context).startActivity(any(Intent.class));
    }

    @Test
    public void testOnTargetNotFound_webScheme_withFlags() {
        boolean result = handler.onTargetNotFound(context, webUri, extras, Intent.FLAG_ACTIVITY_NEW_TASK);
        assertTrue(result);
        ArgumentCaptor<Intent> captor = ArgumentCaptor.forClass(Intent.class);
        verify(context).startActivity(captor.capture());
        Intent started = captor.getValue();
        assertEquals(webUri.toString(), started.getStringExtra("url"));
        assertEquals(Intent.FLAG_ACTIVITY_NEW_TASK, started.getFlags());
    }

    @Test
    public void testOnTargetNotFound_nonWebScheme() {
        boolean result = handler.onTargetNotFound(context, nonWebUri, extras, null);
        assertFalse(result);
        verify(context, never()).startActivity(any(Intent.class));
    }
}
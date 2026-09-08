package me.drakeet.floo.sample;

import android.content.Context;
import android.net.Uri;
import android.os.Bundle;
import android.widget.Toast;

import org.junit.Before;
import org.junit.Test;
import org.mockito.ArgumentCaptor;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class TargetNotFoundToasterTest {

    private Context context;
    private Bundle extras;
    private TargetNotFoundToaster handler;
    private Uri uri;

    @Before
    public void setUp() {
        context = mock(Context.class);
        extras = new Bundle();
        handler = new TargetNotFoundToaster();
        uri = Uri.parse("some://missing");
    }

    @Test
    public void testOnTargetNotFound_alwaysReturnsTrue() {
        boolean result = handler.onTargetNotFound(context, uri, extras, null);
        assertTrue(result);
    }
}
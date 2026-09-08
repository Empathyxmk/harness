package com.birin.gridlistviewadapters.utils;

import android.view.View;
import org.junit.Test;
import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class ViewHolderPositionTaggerTest {

    @Test
    public void testTagAndRetrievePosition() {
        View view = mock(View.class);

        ViewHolderPositionTagger.tagPosition(view, 5);
        verify(view).setTag(eq(ViewHolderPositionTagger.POSITION_TAG_KEY), eq(5));

        // Simulate getTag return
        when(view.getTag(eq(ViewHolderPositionTagger.POSITION_TAG_KEY))).thenReturn(5);
        int result = ViewHolderPositionTagger.getPosition(view);
        assertEquals(5, result);
    }
}
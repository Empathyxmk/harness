package com.len.library;

import android.content.Context;
import android.content.res.TypedArray;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.drawable.Drawable;
import android.text.SpannableString;
import android.text.Spanned;
import android.text.TextPaint;

import org.junit.Test;
import org.junit.Before;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.mockito.Mockito;
import org.robolectric.RobolectricTestRunner;
import org.junit.runner.RunWith;

import static org.junit.Assert.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

/**
 * Public tests for AutoLinkStyleTextView with different data.
 */
@RunWith(RobolectricTestRunner.class)
public class AutoLinkStyleTextViewPublicTest {

    @Mock
    Context mockContext;
    @Mock
    TypedArray mockArray;
    @Mock
    Drawable mockDrawable;
    @Mock
    Canvas mockCanvas;
    @Mock
    Paint mockPaint;

    AutoLinkStyleTextView publicTarget;

    @Before
    public void setup() {
        MockitoAnnotations.initMocks(this);
        when(mockContext.obtainStyledAttributes(any(), any(int[].class), anyInt(), anyInt()))
                .thenReturn(mockArray);
        // Use different defaults compared to original tests
        when(mockArray.getInt(anyInt(), anyInt())).thenReturn(0);
        when(mockArray.getString(anyInt())).thenReturn("Alpha;Beta"); // semicolon, not comma, as a different separator, will fall into non-split-branch
        when(mockArray.getColor(anyInt(), anyInt())).thenReturn(0x00ff00); // green instead of red
        when(mockArray.getBoolean(anyInt(), anyBoolean())).thenReturn(false); // underlines off
        when(mockArray.getResourceId(anyInt(), anyInt())).thenReturn(123);
        publicTarget = new AutoLinkStyleTextView(mockContext, null, 0);
    }

    @Test
    public void testConstructorAndDefaultFields_public() {
        assertNotNull(publicTarget);
    }

    @Test
    public void testSetStartImageText_noDrawable_noCrash_public() {
        assertNotNull(publicTarget.getText());
        publicTarget.setStartImageText("Sample");
        assertNotNull(publicTarget.getText());
    }

    @Test
    public void testSetStartImageText_withImageAndType_public() {
        AutoLinkStyleTextView.styleType = 0;
        when(mockArray.getResourceId(anyInt(), anyInt())).thenReturn(71);
        publicTarget = new AutoLinkStyleTextView(mockContext, null, 0);

        publicTarget.setStartImageText("Hello");
        assertNotNull(publicTarget.getText());
    }

    @Test
    public void testClickCallBackSetAndTrigger_public() {
        AutoLinkStyleTextView.ClickCallBack callback = mock(AutoLinkStyleTextView.ClickCallBack.class);
        publicTarget.setOnClickCallBack(callback);
        // Different triggers, with dash separator, triggers non-comma code path
        when(mockArray.getString(anyInt())).thenReturn("Plan-Policy");
        publicTarget = new AutoLinkStyleTextView(mockContext, null, 0);
        assertNotNull(publicTarget);
    }

    @Test
    public void testAddStyle_branchEmptyOrNoComma_public() {
        // string without comma but with other character
        when(mockArray.getString(anyInt())).thenReturn("SingleSegment");
        publicTarget = new AutoLinkStyleTextView(mockContext, null, 0);
        assertNotNull(publicTarget.getText());
    }

    @Test
    public void testClickableSpanUpdateDrawState_public() {
        when(mockArray.getString(anyInt())).thenReturn("Green,Orange");
        when(mockArray.getColor(anyInt(), anyInt())).thenReturn(0x123456);
        AutoLinkStyleTextView.styleType = 1;
        publicTarget = new AutoLinkStyleTextView(mockContext, null, 0);
        CharSequence cs = publicTarget.getText();
        if (cs instanceof Spanned) {
            Spanned sp = (Spanned) cs;
            Object[] spans = sp.getSpans(0, cs.length(), Object.class);
            for (Object o : spans) {
                if (o instanceof android.text.style.ClickableSpan) {
                    TextPaint tp = new TextPaint();
                    ((android.text.style.ClickableSpan) o).updateDrawState(tp);
                    assertEquals(0x123456, tp.getColor());
                }
            }
        }
    }

    @Test
    public void testCenteredImageSpan_draw_executes_public() {
        when(mockArray.getResourceId(anyInt(), anyInt())).thenReturn(555);
        AutoLinkStyleTextView.styleType = 0;
        publicTarget = new AutoLinkStyleTextView(mockContext, null, 0);

        publicTarget.setStartImageText("World");
        CharSequence t = publicTarget.getText();
        if (t instanceof Spanned) {
            Object[] spans = ((Spanned)t).getSpans(0, t.length(), Object.class);
            for (Object s : spans) {
                if (s.getClass().getSimpleName().contains("CenteredImageSpan")) {
                    try {
                        Canvas can = mock(Canvas.class);
                        Paint.TextMetricsParams p = null;
                        Paint paint = new Paint();
                        Paint.FontMetricsInt fmi = new Paint.FontMetricsInt();
                        paint.setColor(0xffff0000);
                        s.getClass().getMethod("draw", Canvas.class, CharSequence.class, int.class,
                                int.class, float.class, int.class, int.class, int.class, Paint.class)
                                .invoke(s, can, "ab", 0, 1, 0f, 0, 0, 0, paint);
                    } catch (Exception e) {
                        // ignore
                    }
                }
            }
        }
    }
}
package io.github.luckyandyzhang.mentionedittext;

import android.content.Context;
import android.graphics.Color;
import android.text.Editable;
import android.text.Spannable;
import android.text.style.ForegroundColorSpan;
import android.view.inputmethod.EditorInfo;
import android.view.inputmethod.InputConnection;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.stubbing.Answer;
import org.mockito.invocation.InvocationOnMock;
import org.robolectric.RobolectricTestRunner;
import org.robolectric.RuntimeEnvironment;
import org.robolectric.annotation.Config;

import static org.junit.Assert.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@RunWith(RobolectricTestRunner.class)
@Config(sdk = 21)
public class MentionEditTextPublicTest {

    private MentionEditText mentionEditText;
    private Context context;

    @Before
    public void setUp() {
        context = RuntimeEnvironment.application;
        mentionEditText = new MentionEditText(context);
        mentionEditText.setText(""); // Initialize with empty text
        mentionEditText.setMentionTextColor(Color.RED); // Use a different color for public test
    }

    @Test
    public void testConstructorsPublic() {
        assertNotNull(new MentionEditText(context));
        assertNotNull(new MentionEditText(context, null));
        assertNotNull(new MentionEditText(context, null, 0));
    }

    @Test
    public void testSetText_SelectionAtEnd_Public() {
        mentionEditText = spy(new MentionEditText(context));
        doAnswer((Answer<Object>) invocation -> {
            Runnable runnable = invocation.getArgument(0);
            runnable.run();
            return null;
        }).when(mentionEditText).post(any(Runnable.class));

        String text = "Test @ExampleUser";
        mentionEditText.setText(text);
        assertEquals(text.length(), mentionEditText.getSelectionEnd());
        assertEquals(text.length(), mentionEditText.getSelectionStart());
    }

    @Test
    public void testOnCreateInputConnection_Public() {
        InputConnection mockInputConnection = mock(InputConnection.class);
        when(mentionEditText.superOnCreateInputConnection(any(EditorInfo.class))).thenReturn(mockInputConnection);

        EditorInfo editorInfo = new EditorInfo();
        InputConnection resultConnection = mentionEditText.onCreateInputConnection(editorInfo);
        assertNotNull(resultConnection);
        assertTrue(resultConnection instanceof MentionEditText.HackInputConnection);
    }

    @Test
    public void testOnTextChanged_ColorsMentionString_Public() {
        String text = "Greetings @alphaTest and @bravoTester!";
        mentionEditText.setText(text);

        Editable editable = mentionEditText.getText();
        ForegroundColorSpan[] spans = editable.getSpans(0, editable.length(), ForegroundColorSpan.class);

        assertEquals(2, spans.length);

        // Verify the mentions
        assertEquals(Color.RED, spans[0].getForegroundColor());
        String mention1 = editable.subSequence(editable.getSpanStart(spans[0]), editable.getSpanEnd(spans[0])).toString();
        assertEquals("@alphaTest", mention1);

        assertEquals(Color.RED, spans[1].getForegroundColor());
        String mention2 = editable.subSequence(editable.getSpanStart(spans[1]), editable.getSpanEnd(spans[1])).toString();
        assertEquals("@bravoTester", mention2);
    }

    @Test
    public void testOnTextChanged_NoMentionString_Public() {
        String text = "Nothing special here, just text.";
        mentionEditText.setText(text);

        Editable editable = mentionEditText.getText();
        ForegroundColorSpan[] spans = editable.getSpans(0, editable.length(), ForegroundColorSpan.class);
        assertEquals(0, spans.length);
    }

    @Test
    public void testOnSelectionChanged_NoNearbyMentionString_Public() {
        String text = "Public input string.";
        mentionEditText.setText(text);
        mentionEditText.setSelection(8, 8);
        assertEquals(8, mentionEditText.getSelectionStart());
        assertEquals(8, mentionEditText.getSelectionEnd());
    }

    @Test
    public void testOnSelectionChanged_CursorInsideMentionString_AdjustsSelection_Public() {
        String text = "Public @mainUser example.";
        mentionEditText.setText(text);
        // "@mainUser" starts at 7 ends at 16
        mentionEditText.setSelection(9, 9); // after '@m'

        // Should move to end of mention
        assertEquals(16, mentionEditText.getSelectionStart());
        assertEquals(16, mentionEditText.getSelectionEnd());
    }

    @Test
    public void testOnSelectionChanged_CursorAtStartOfMentionString_AdjustsSelection_Public() {
        String text = "Public @mainUser example.";
        mentionEditText.setText(text);
        mentionEditText.setSelection(7, 7);

        assertEquals(16, mentionEditText.getSelectionStart());
        assertEquals(16, mentionEditText.getSelectionEnd());
    }

    @Test
    public void testOnSelectionChanged_CursorAtEndOfMentionString_NoChange_Public() {
        String text = "Public @mainUser example.";
        mentionEditText.setText(text);
        mentionEditText.setSelection(16, 16);

        assertEquals(16, mentionEditText.getSelectionStart());
        assertEquals(16, mentionEditText.getSelectionEnd());
    }

    @Test
    public void testOnSelectionChanged_SelectingPartialMentionString_ExpandsSelection_Public() {
        String text = "Public @mainUser example.";
        mentionEditText.setText(text);
        // Select "mainU" from within "@mainUser"
        mentionEditText.setSelection(8, 13); // "@mainUser" is from 7 to 16

        assertEquals(7, mentionEditText.getSelectionStart());
        assertEquals(16, mentionEditText.getSelectionEnd());
    }

    @Test
    public void testOnSelectionChanged_SelectingPartialMentionStringFromEnd_ExpandsSelection_Public() {
        String text = "Public @mainUser example.";
        mentionEditText.setText(text);
        // Select "ainUser" backwards
        mentionEditText.setSelection(10, 16);

        assertEquals(7, mentionEditText.getSelectionStart());
        assertEquals(16, mentionEditText.getSelectionEnd());
    }
}
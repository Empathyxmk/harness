package io.github.luckyandyzhang.mentionedittext;

import android.content.Context;
import android.graphics.Color;
import android.text.Editable;
import android.text.Spannable;
import android.text.TextWatcher;
import android.text.style.ForegroundColorSpan;
import android.view.KeyEvent;
import android.view.inputmethod.EditorInfo;
import android.view.inputmethod.InputConnection;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.ArgumentCaptor;
import org.mockito.invocation.InvocationOnMock;
import org.mockito.stubbing.Answer;
import org.robolectric.RobolectricTestRunner;
import org.robolectric.RuntimeEnvironment;
import org.robolectric.annotation.Config;

import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.doAnswer;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.spy;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@RunWith(RobolectricTestRunner.class)
@Config(sdk = 21) // Specify Android SDK version for Robolectric
public class MentionEditTextTest {

    private MentionEditText mentionEditText;
    private Context context;

    @Before
    public void setUp() {
        context = RuntimeEnvironment.application;
        mentionEditText = new MentionEditText(context);
        mentionEditText.setText(""); // Initialize with empty text
        mentionEditText.setMentionTextColor(Color.BLUE); // Set a color for testing
    }

    @Test
    public void testConstructors() {
        assertNotNull(new MentionEditText(context));
        assertNotNull(new MentionEditText(context, null));
        assertNotNull(new MentionEditText(context, null, 0));
    }

    @Test
    public void testSetText_SelectionAtEnd() {
        // Mocking the post method to execute the Runnable immediately
        mentionEditText = spy(new MentionEditText(context));
        doAnswer(new Answer() {
            @Override
            public Object answer(InvocationOnMock invocation) throws Throwable {
                Runnable runnable = invocation.getArgument(0);
                runnable.run();
                return null;
            }
        }).when(mentionEditText).post(any(Runnable.class));

        String text = "Hello @World";
        mentionEditText.setText(text);
        assertEquals(text.length(), mentionEditText.getSelectionEnd());
        assertEquals(text.length(), mentionEditText.getSelectionStart());
    }

    @Test
    public void testOnCreateInputConnection() {
        InputConnection mockInputConnection = mock(InputConnection.class);
        when(mentionEditText.superOnCreateInputConnection(any(EditorInfo.class))).thenReturn(mockInputConnection); // Mock super call

        EditorInfo editorInfo = new EditorInfo();
        InputConnection resultConnection = mentionEditText.onCreateInputConnection(editorInfo);
        assertNotNull(resultConnection);
        assertTrue(resultConnection instanceof MentionEditText.HackInputConnection);
    }

    @Test
    public void testOnTextChanged_ColorsMentionString() {
        String text = "Hello @testuser this is a @seconduser mention.";
        mentionEditText.setText(text);

        Editable editable = mentionEditText.getText();
        ForegroundColorSpan[] spans = editable.getSpans(0, editable.length(), ForegroundColorSpan.class);

        // Check if spans are applied for both mentions
        assertEquals(2, spans.length);

        // Verify the first mention
        assertEquals(Color.BLUE, spans[0].getForegroundColor());
        String mention1 = editable.subSequence(editable.getSpanStart(spans[0]), editable.getSpanEnd(spans[0])).toString();
        assertEquals("@testuser", mention1);

        // Verify the second mention
        assertEquals(Color.BLUE, spans[1].getForegroundColor());
        String mention2 = editable.subSequence(editable.getSpanStart(spans[1]), editable.getSpanEnd(spans[1])).toString();
        assertEquals("@seconduser", mention2);
    }

    @Test
    public void testOnTextChanged_NoMentionString() {
        String text = "Hello world, no mention here.";
        mentionEditText.setText(text);

        Editable editable = mentionEditText.getText();
        ForegroundColorSpan[] spans = editable.getSpans(0, editable.length(), ForegroundColorSpan.class);
        assertEquals(0, spans.length);
    }

    @Test
    public void testOnSelectionChanged_NoNearbyMentionString() {
        String text = "This is some text.";
        mentionEditText.setText(text);
        mentionEditText.setSelection(5, 5); // Cursor in the middle of plain text
        // No change expected
        assertEquals(5, mentionEditText.getSelectionStart());
        assertEquals(5, mentionEditText.getSelectionEnd());
    }

    @Test
    public void testOnSelectionChanged_CursorInsideMentionString_AdjustsSelection() {
        String text = "Hello @user there.";
        mentionEditText.setText(text);
        // Simulate cursor placed inside "@user" (e.g., after '@u')
        mentionEditText.setSelection(7, 7); // @user starts at 6, ends at 11. Cursor at index 7.

        // The cursor should be moved to the end of the mention string.
        assertEquals(11, mentionEditText.getSelectionStart());
        assertEquals(11, mentionEditText.getSelectionEnd());
    }

    @Test
    public void testOnSelectionChanged_CursorAtStartOfMentionString_AdjustsSelection() {
        String text = "Hello @user there.";
        mentionEditText.setText(text);
        // Simulate cursor placed at the start of "@user"
        mentionEditText.setSelection(6, 6);

        // The cursor should be moved to the end of the mention string.
        assertEquals(11, mentionEditText.getSelectionStart());
        assertEquals(11, mentionEditText.getSelectionEnd());
    }

    @Test
    public void testOnSelectionChanged_CursorAtEndOfMentionString_NoChange() {
        String text = "Hello @user there.";
        mentionEditText.setText(text);
        // Simulate cursor placed at the end of "@user"
        mentionEditText.setSelection(11, 11);

        // No change expected
        assertEquals(11, mentionEditText.getSelectionStart());
        assertEquals(11, mentionEditText.getSelectionEnd());
    }

    @Test
    public void testOnSelectionChanged_SelectingPartialMentionString_ExpandsSelection() {
        String text = "Hello @user there.";
        mentionEditText.setText(text);
        // Simulate selecting "user" within "@user"
        mentionEditText.setSelection(7, 11); // "@user" is from index 6 to 11

        // Selection should expand to include the whole mention string
        assertEquals(6, mentionEditText.getSelectionStart());
        assertEquals(11, mentionEditText.getSelectionEnd());
    }

    @Test
    public void testOnSelectionChanged_SelectingPartialMentionStringFromEnd_ExpandsSelection() {
        String text = "Hello @user there.";
        mentionEditText.setText(text);
        // Simulate selecting "ser" backwards from end of "@user"
        mentionEditText.setSelection(8, 11);

        // Selection should expand to include the whole mention string
        assertEquals(6, mentionEditText.getSelectionStart());
        assertEquals(11, mentionEditText.getSelectionEnd());
    }

    @Test
    public void testOnSelectionChanged_SelectingPartialMentionStringFromStart_ExpandsSelection() {
        String text = "Hello @user there.";
        mentionEditText.setText(text);
        // Simulate selecting "@us" from start of "@user"
        mentionEditText.setSelection(6, 9);

        // Selection should expand to include the whole mention string
        assertEquals(6, mentionEditText.getSelectionStart());
        assertEquals(11, mentionEditText.getSelectionEnd());
    }

    @Test
    public void testOnSelectionChanged_FullSelectionOfMentionString_AllowsSelection() {
        String text = "Hello @user there.";
        mentionEditText.setText(text);
        mentionEditText.setSelection(6, 11); // Selecting "@user"

        // Should allow full selection without moving.
        assertEquals(6, mentionEditText.getSelectionStart());
        assertEquals(11, mentionEditText.getSelectionEnd());
        assertTrue(mentionEditText.isSelected()); // Internal mIsSelected should be true
    }

    @Test
    public void testOnSelectionChanged_CancelSelection_ResetsIsSelected() {
        String text = "Hello @user there.";
        mentionEditText.setText(text);
        mentionEditText.setSelection(6, 11); // Select
        assertTrue(mentionEditText.isSelected());

        mentionEditText.setSelection(11, 11); // Move cursor to end of mention, effectively deselecting
        assertFalse(mentionEditText.isSelected());
    }

    @Test
    public void testSetPattern_ClearsPreviousPatterns() {
        mentionEditText.addPattern("#", "#[0-9]+");
        mentionEditText.addPattern("$", "\\$[a-zA-Z]+");
        assertEquals(2, mentionEditText.getPatternMapSize());

        mentionEditText.setPattern("@", "@[\\u4e00-\\u9fa5\\w\\-]+");
        assertEquals(1, mentionEditText.getPatternMapSize());
        assertNotNull(mentionEditText.getPatternMap().get("@"));
    }

    @Test
    public void testAddPattern() {
        mentionEditText.addPattern("$", "\\$[a-zA-Z]+");
        assertEquals(1, mentionEditText.getPatternMapSize());
        assertNotNull(mentionEditText.getPatternMap().get("$"));
    }

    @Test
    public void testRemovePattern() {
        mentionEditText.addPattern("$", "\\$[a-zA-Z]+");
        mentionEditText.removePattern("$");
        assertEquals(0, mentionEditText.getPatternMapSize());
        assertNull(mentionEditText.getPatternMap().get("$"));
    }

    @Test
    public void testRemovePattern_NonExistent() {
        mentionEditText.addPattern("$", "\\$[a-zA-Z]+");
        mentionEditText.removePattern("£"); // Try to remove non-existent
        assertEquals(1, mentionEditText.getPatternMapSize());
    }

    @Test
    public void testAddMentionString_AppendsTextAndAddsRange() {
        String mention = "@newuser";
        mentionEditText.addMentionString(mention);
        assertEquals(mention + " ", mentionEditText.getText().toString());
        assertEquals(1, mentionEditText.getMentionList().size());
        assertEquals(0, mentionEditText.getMentionList().get(0).from);
        assertEquals(mention.length(), mentionEditText.getMentionList().get(0).to);
    }

    @Test
    public void testAddMentionString_WithExistingText() {
        mentionEditText.setText("Existing text ");
        String mention = "@newuser";
        mentionEditText.addMentionString(mention);
        assertEquals("Existing text @newuser ", mentionEditText.getText().toString());
        assertEquals(1, mentionEditText.getMentionList().size());
        assertEquals("Existing text ".length(), mentionEditText.getMentionList().get(0).from);
        assertEquals("Existing text ".length() + mention.length(), mentionEditText.getMentionList().get(0).to);
    }

    @Test
    public void testRemoveMentionString() {
        mentionEditText.setText("Hello @user there.");
        mentionEditText.removeMentionString("@user"); // Should remove the first occurrence.
        assertEquals("Hello  there.", mentionEditText.getText().toString());
        assertEquals(0, mentionEditText.getMentionList().size()); // No mentions should remain in the list
    }

    @Test
    public void testRemoveMentionString_MultipleMentions() {
        mentionEditText.setText("Hello @user and @another.");
        mentionEditText.removeMentionString("@user");
        assertEquals("Hello  and @another.", mentionEditText.getText().toString());
        assertEquals(1, mentionEditText.getMentionList().size());
        assertEquals("@another", mentionEditText.getText().subSequence(
                mentionEditText.getMentionList().get(0).from,
                mentionEditText.getMentionList().get(0).to
        ).toString());
    }

    @Test
    public void testRemoveMentionString_NonExistent() {
        mentionEditText.setText("Hello world.");
        mentionEditText.removeMentionString("@user");
        assertEquals("Hello world.", mentionEditText.getText().toString());
        assertEquals(0, mentionEditText.getMentionList().size());
    }

    @Test
    public void testGetMentionList() {
        mentionEditText.setText("Hello @user and @another here.");
        List<String> mentions = mentionEditText.getMentionList();
        assertEquals(2, mentions.size());
        assertTrue(mentions.contains("@user"));
        assertTrue(mentions.contains("@another"));
    }

    @Test
    public void testClear() {
        mentionEditText.setText("Hello @user.");
        mentionEditText.clear();
        assertEquals("", mentionEditText.getText().toString());
        assertTrue(mentionEditText.getMentionList().isEmpty());
    }

    @Test
    public void testSetOnMentionInputListener_Null() {
        mentionEditText.setOnMentionInputListener(null);
        // No crash, just setting null.
    }

    @Test
    public void testSetOnMentionInputListener_CallbackTriggered() {
        MentionEditText.OnMentionInputListener mockListener = mock(MentionEditText.OnMentionInputListener.class);
        mentionEditText.setOnMentionInputListener(mockListener);

        mentionEditText.setText("text");
        mentionEditText.setSelection(mentionEditText.getText().length());
        mentionEditText.getText().append("@"); // Simulate '@' input

        verify(mockListener, times(1)).onMentionCharacterInput();
    }

    @Test
    public void testHackInputConnection_DeleteSurroundingText_DeleteMention() {
        mentionEditText.setText("text @user|"); // '|' indicates cursor position
        mentionEditText.setSelection(10, 10); // Cursor after @user

        InputConnection ic = mentionEditText.onCreateInputConnection(new EditorInfo());
        // Simulate backspace, deleting one character before cursor
        // HackInputConnection should detect if it's deleting a mention
        ic.deleteSurroundingText(1, 0);

        // Expect "@user" to be deleted
        assertEquals("text ", mentionEditText.getText().toString());
        assertEquals(0, mentionEditText.getMentionList().size());
        assertEquals(5, mentionEditText.getSelectionStart());
        assertEquals(5, mentionEditText.getSelectionEnd());
    }

    @Test
    public void testHackInputConnection_DeleteSurroundingText_DeletePartialMention_ShouldDeleteFull() {
        mentionEditText.setText("text @user|"); // '|' indicates cursor position
        mentionEditText.setSelection(8, 8); // Cursor inside @user, e.g. after @u

        InputConnection ic = mentionEditText.onCreateInputConnection(new EditorInfo());
        ic.deleteSurroundingText(1, 0); // Delete 's'

        // Expect "@user" to be deleted
        assertEquals("text ", mentionEditText.getText().toString());
        assertEquals(0, mentionEditText.getMentionList().size());
        assertEquals(5, mentionEditText.getSelectionStart());
        assertEquals(5, mentionEditText.getSelectionEnd());
    }

    @Test
    public void testHackInputConnection_DeleteSurroundingText_DeleteNormalText() {
        mentionEditText.setText("text user|");
        mentionEditText.setSelection(9, 9); // Cursor after 'r'

        InputConnection ic = mentionEditText.onCreateInputConnection(new EditorInfo());
        ic.deleteSurroundingText(1, 0); // Delete 'r'

        assertEquals("text use", mentionEditText.getText().toString());
        assertEquals(8, mentionEditText.getSelectionStart());
        assertEquals(8, mentionEditText.getSelectionEnd());
    }

    @Test
    public void testHackInputConnection_DeleteSurroundingText_SelectionAcrossMention() {
        mentionEditText.setText("before @user after");
        // Select 'e @use' (part of "before @user")
        mentionEditText.setSelection(4, 11);

        InputConnection ic = mentionEditText.onCreateInputConnection(new EditorInfo());
        ic.deleteSurroundingText(0, 0); // Simulate deletion of selected text

        // Should delete "e @user"
        assertEquals("bfor after", mentionEditText.getText().toString());
        assertEquals(0, mentionEditText.getMentionList().size());
    }

    @Test
    public void testHackInputConnection_SendKeyEvent_DeleteAction() {
        mentionEditText.setText("text @user|");
        mentionEditText.setSelection(10, 10); // Cursor after @user

        InputConnection ic = mentionEditText.onCreateInputConnection(new EditorInfo());
        KeyEvent event = new KeyEvent(KeyEvent.ACTION_DOWN, KeyEvent.KEYCODE_DEL);
        ic.sendKeyEvent(event);

        assertEquals("text ", mentionEditText.getText().toString());
        assertEquals(0, mentionEditText.getMentionList().size());
        assertEquals(5, mentionEditText.getSelectionStart());
        assertEquals(5, mentionEditText.getSelectionEnd());
    }

    @Test
    public void testHackInputConnection_SendKeyEvent_OtherAction() {
        mentionEditText.setText("text @user|");
        mentionEditText.setSelection(10, 10); // Cursor after @user

        InputConnection mockInputConnection = mock(InputConnection.class);
        when(mentionEditText.superOnCreateInputConnection(any(EditorInfo.class))).thenReturn(mockInputConnection);
        MentionEditText.HackInputConnection spyConnection = spy(new MentionEditText.HackInputConnection(mockInputConnection, true, mentionEditText));

        KeyEvent event = new KeyEvent(KeyEvent.ACTION_DOWN, KeyEvent.KEYCODE_A); // 'A' key
        spyConnection.sendKeyEvent(event);

        verify(mockInputConnection, times(1)).sendKeyEvent(event);
        // Should not trigger intelligent deletion
        assertEquals("text @user", mentionEditText.getText().toString());
    }

    @Test
    public void testHackInputConnection_SendKeyEvent_MultipleDeletions() {
        mentionEditText.setText("first @user second @test third");
        mentionEditText.setSelection(17, 17); // After @test

        InputConnection ic = mentionEditText.onCreateInputConnection(new EditorInfo());

        // First deletion, delete @test
        KeyEvent event = new KeyEvent(KeyEvent.ACTION_DOWN, KeyEvent.KEYCODE_DEL);
        ic.sendKeyEvent(event);
        assertEquals("first @user second  third", mentionEditText.getText().toString());
        assertEquals(1, mentionEditText.getMentionList().size());
        assertEquals(16, mentionEditText.getSelectionStart());
        assertEquals(16, mentionEditText.getSelectionEnd());

        // Second deletion, delete space after "second"
        event = new KeyEvent(KeyEvent.ACTION_DOWN, KeyEvent.KEYCODE_DEL);
        ic.sendKeyEvent(event);
        assertEquals("first @user second third", mentionEditText.getText().toString());
        assertEquals(15, mentionEditText.getSelectionStart());
        assertEquals(15, mentionEditText.getSelectionEnd());

        // Third deletion, delete 'd' from "third"
        event = new KeyEvent(KeyEvent.ACTION_DOWN, KeyEvent.KEYCODE_DEL);
        ic.sendKeyEvent(event);
        assertEquals("first @user second thir", mentionEditText.getText().toString());
        assertEquals(14, mentionEditText.getSelectionStart());
        assertEquals(14, mentionEditText.getSelectionEnd());
    }

    @Test
    public void testGetRangeOfClosestMentionString() {
        mentionEditText.setText("Hello @user and @another.");

        // Cursor within "@user"
        MentionEditText.Range range1 = mentionEditText.getRangeOfClosestMentionString(7, 7); // 'u' in @user
        assertNotNull(range1);
        assertEquals(6, range1.from);
        assertEquals(11, range1.to);

        // Cursor between mentions
        MentionEditText.Range range2 = mentionEditText.getRangeOfClosestMentionString(12, 12); // space after @user
        assertNull(range2);

        // Cursor within "@another"
        MentionEditText.Range range3 = mentionEditText.getRangeOfClosestMentionString(20, 20); // 'o' in @another
        assertNotNull(range3);
        assertEquals(16, range3.from);
        assertEquals(24, range3.to);

        // Cursor at very end
        MentionEditText.Range range4 = mentionEditText.getRangeOfClosestMentionString(25, 25);
        assertNull(range4);

        // Selection spanning multiple mentions
        MentionEditText.Range range5 = mentionEditText.getRangeOfClosestMentionString(6, 24); // select from @user to @another
        assertNull(range5); // Should return null if selection covers multiple or part of one.
    }

    @Test
    public void testGetRangeOfNearbyMentionString() {
        mentionEditText.setText("Hello @user and @another.");

        // Cursor exactly at start of mention
        MentionEditText.Range range1 = mentionEditText.getRangeOfNearbyMentionString(6, 6);
        assertNotNull(range1);
        assertEquals(6, range1.from);
        assertEquals(11, range1.to);

        // Cursor exactly at end of mention
        MentionEditText.Range range2 = mentionEditText.getRangeOfNearbyMentionString(11, 11);
        assertNotNull(range2);
        assertEquals(6, range2.from);
        assertEquals(11, range2.to);

        // Cursor just after mention
        MentionEditText.Range range3 = mentionEditText.getRangeOfNearbyMentionString(12, 12);
        assertNull(range3);

        // Cursor just before mention
        MentionEditText.Range range4 = mentionEditText.getRangeOfNearbyMentionString(5, 5);
        assertNull(range4);

        // Selection covering exactly one mention
        MentionEditText.Range range5 = mentionEditText.getRangeOfNearbyMentionString(6, 11);
        assertNotNull(range5);
        assertEquals(6, range5.from);
        assertEquals(11, range5.to);
    }


    @Test
    public void testGetMentionTextColor() {
        mentionEditText.setMentionTextColor(Color.RED);
        assertEquals(Color.RED, mentionEditText.getMentionTextColor());
    }

    @Test
    public void testSetMentionTextColor() {
        mentionEditText.setMentionTextColor(Color.GREEN);
        assertEquals(Color.GREEN, mentionEditText.getMentionTextColor());

        // Verify that changing color reapplies spans
        String text = "Hello @user";
        mentionEditText.setText(text);
        ForegroundColorSpan[] spans = mentionEditText.getText().getSpans(0, mentionEditText.getText().length(), ForegroundColorSpan.class);
        assertEquals(1, spans.length);
        assertEquals(Color.GREEN, spans[0].getForegroundColor());
    }

    @Test
    public void testMentionInputListener_NoInput() {
        MentionEditText.OnMentionInputListener mockListener = mock(MentionEditText.OnMentionInputListener.class);
        mentionEditText.setOnMentionInputListener(mockListener);

        mentionEditText.setText("abc");
        mentionEditText.setSelection(3);
        verify(mockListener, never()).onMentionCharacterInput();
    }

    @Test
    public void testMentionInputListener_InputThenDelete() {
        MentionEditText.OnMentionInputListener mockListener = mock(MentionEditText.OnMentionInputListener.class);
        mentionEditText.setOnMentionInputListener(mockListener);

        mentionEditText.setText("a");
        mentionEditText.setSelection(1);
        mentionEditText.getText().append("@"); // Input '@'
        verify(mockListener, times(1)).onMentionCharacterInput();

        mentionEditText.getText().delete(1, 2); // Delete '@'
        // Listener should not be called again if char is deleted
        verify(mockListener, times(1)).onMentionCharacterInput();
    }

    @Test
    public void testMentionInputListener_InputNotAtEnd() {
        MentionEditText.OnMentionInputListener mockListener = mock(MentionEditText.OnMentionInputListener.class);
        mentionEditText.setOnMentionInputListener(mockListener);

        mentionEditText.setText("abc");
        mentionEditText.setSelection(1);
        mentionEditText.getText().insert(1, "@"); // Insert '@' in the middle
        verify(mockListener, times(1)).onMentionCharacterInput();
    }

    @Test
    public void testHackInputConnection_PerformEditorAction() {
        InputConnection mockInputConnection = mock(InputConnection.class);
        when(mentionEditText.superOnCreateInputConnection(any(EditorInfo.class))).thenReturn(mockInputConnection);
        MentionEditText.HackInputConnection spyConnection = spy(new MentionEditText.HackInputConnection(mockInputConnection, true, mentionEditText));

        spyConnection.performEditorAction(EditorInfo.IME_ACTION_DONE);
        verify(mockInputConnection, times(1)).performEditorAction(EditorInfo.IME_ACTION_DONE);
    }

    @Test
    public void testHackInputConnection_CommitText() {
        InputConnection mockInputConnection = mock(InputConnection.class);
        when(mentionEditText.superOnCreateInputConnection(any(EditorInfo.class))).thenReturn(mockInputConnection);
        MentionEditText.HackInputConnection spyConnection = spy(new MentionEditText.HackInputConnection(mockInputConnection, true, mentionEditText));

        spyConnection.commitText("abc", 1);
        verify(mockInputConnection, times(1)).commitText("abc", 1);
    }

    @Test
    public void testHackInputConnection_SetComposingText() {
        InputConnection mockInputConnection = mock(InputConnection.class);
        when(mentionEditText.superOnCreateInputConnection(any(EditorInfo.class))).thenReturn(mockInputConnection);
        MentionEditText.HackInputConnection spyConnection = spy(new MentionEditText.HackInputConnection(mockInputConnection, true, mentionEditText));

        spyConnection.setComposingText("abc", 1);
        verify(mockInputConnection, times(1)).setComposingText("abc", 1);
    }

    @Test
    public void testHackInputConnection_SetSelection_WithinMention() {
        mentionEditText.setText("Hello @user there.");
        mentionEditText.setSelection(6, 11); // select @user
        assertTrue(mentionEditText.isSelected());

        InputConnection mockInputConnection = mock(InputConnection.class);
        when(mentionEditText.superOnCreateInputConnection(any(EditorInfo.class))).thenReturn(mockInputConnection);
        MentionEditText.HackInputConnection spyConnection = spy(new MentionEditText.HackInputConnection(mockInputConnection, true, mentionEditText));

        // Try to set selection from 7 to 8 (inside @user)
        spyConnection.setSelection(7, 8);
        // Expect that setSelection on MentionEditText is called to correct it
        ArgumentCaptor<Integer> startCaptor = ArgumentCaptor.forClass(Integer.class);
        ArgumentCaptor<Integer> endCaptor = ArgumentCaptor.forClass(Integer.class);
        // The selection logic is handled in onSelectionChanged, which is triggered by setSelection.
        // We're checking if the underlying input connection is called.
        verify(mockInputConnection, times(1)).setSelection(anyInt(), anyInt());
        // The MentionEditText itself will adjust it. No direct assertion on the mock input connection.
    }

    @Test
    public void testHackInputConnection_SetSelection_OutsideMention() {
        InputConnection mockInputConnection = mock(InputConnection.class);
        when(mentionEditText.superOnCreateInputConnection(any(EditorInfo.class))).thenReturn(mockInputConnection);
        MentionEditText.HackInputConnection spyConnection = spy(new MentionEditText.HackInputConnection(mockInputConnection, true, mentionEditText));

        spyConnection.setSelection(0, 5);
        verify(mockInputConnection, times(1)).setSelection(0, 5);
    }

    @Test
    public void testHackInputConnection_InvalidRange_NoCrash() {
        InputConnection mockInputConnection = mock(InputConnection.class);
        when(mentionEditText.superOnCreateInputConnection(any(EditorInfo.class))).thenReturn(mockInputConnection);
        MentionEditText.HackInputConnection spyConnection = spy(new MentionEditText.HackInputConnection(mockInputConnection, true, mentionEditText));

        // Invalid ranges for deleteSurroundingText
        spyConnection.deleteSurroundingText(-1, 0);
        spyConnection.deleteSurroundingText(0, -1);
        spyConnection.deleteSurroundingText(-1, -1);
        // Should not crash, just pass to super
        verify(mockInputConnection, times(3)).deleteSurroundingText(anyInt(), anyInt());
    }

    @Test
    public void testRange_IsEqual() {
        MentionEditText.Range r1 = new MentionEditText.Range(0, 5);
        MentionEditText.Range r2 = new MentionEditText.Range(0, 5);
        MentionEditText.Range r3 = new MentionEditText.Range(1, 5);
        MentionEditText.Range r4 = new MentionEditText.Range(0, 6);

        assertTrue(r1.isEqual(r2));
        assertTrue(r1.isEqual(0, 5));
        assertFalse(r1.isEqual(r3));
        assertFalse(r1.isEqual(r4));
        assertFalse(r1.isEqual(1, 5));
        assertFalse(r1.isEqual(0, 6));
    }

    @Test
    public void testRange_GetAnchorPosition() {
        MentionEditText.Range r1 = new MentionEditText.Range(0, 5); // Represents "@user"
        assertEquals(5, r1.getAnchorPosition(3)); // Cursor at 3 (inside), anchor should be 5
        assertEquals(5, r1.getAnchorPosition(0)); // Cursor at 0 (start), anchor should be 5
        assertEquals(5, r1.getAnchorPosition(5)); // Cursor at 5 (end), anchor should be 5

        MentionEditText.Range r2 = new MentionEditText.Range(6, 11); // Represents "@user"
        assertEquals(11, r2.getAnchorPosition(6));
        assertEquals(11, r2.getAnchorPosition(11));
        assertEquals(11, r2.getAnchorPosition(8));
    }

    @Test
    public void testRange_ToString() {
        MentionEditText.Range r1 = new MentionEditText.Range(0, 5);
        assertEquals("Range{from=0, to=5}", r1.toString());
    }

    @Test
    public void testMentionPattern_Custom() {
        mentionEditText.setPattern("#", "#[0-9]+");
        mentionEditText.setText("This is #123 and not @abc.");

        Editable editable = mentionEditText.getText();
        ForegroundColorSpan[] spans = editable.getSpans(0, editable.length(), ForegroundColorSpan.class);
        assertEquals(1, spans.length);
        assertEquals(Color.BLUE, spans[0].getForegroundColor());
        assertEquals("#123", editable.subSequence(editable.getSpanStart(spans[0]), editable.getSpanEnd(spans[0])).toString());
    }

    @Test
    public void testHighlightMentionString_EmptyText() {
        mentionEditText.setText("");
        // Should not crash, no spans expected
        ForegroundColorSpan[] spans = mentionEditText.getText().getSpans(0, 0, ForegroundColorSpan.class);
        assertEquals(0, spans.length);
    }

    @Test
    public void testReplaceMentionText_NoMentions() {
        mentionEditText.setText("Hello world");
        String replaced = mentionEditText.getMentionText();
        assertEquals("Hello world", replaced);
    }

    @Test
    public void testReplaceMentionText_SingleMention() {
        mentionEditText.setText("Hello @user");
        String replaced = mentionEditText.getMentionText();
        assertEquals("Hello ", replaced);
    }

    @Test
    public void testReplaceMentionText_MultipleMentions() {
        mentionEditText.setText("Hello @user and @another.");
        String replaced = mentionEditText.getMentionText();
        assertEquals("Hello  and .", replaced);
    }

    @Test
    public void testReplaceMentionTag_NoMentions() {
        mentionEditText.setText("Hello world");
        String replaced = mentionEditText.getMentionText(MentionEditText.DEFAULT_METION_TAG);
        assertEquals("Hello world", replaced);
    }

    @Test
    public void testReplaceMentionTag_SingleMention() {
        mentionEditText.setText("Hello @user");
        String replaced = mentionEditText.getMentionText(MentionEditText.DEFAULT_METION_TAG);
        assertEquals("Hello @user", replaced); // This method replaces with the tag itself
    }

    @Test
    public void testReplaceMentionTag_MultipleMentions() {
        mentionEditText.setText("Hello @user and @another.");
        String replaced = mentionEditText.getMentionText(MentionEditText.DEFAULT_METION_TAG);
        assertEquals("Hello @ and @.", replaced);
    }

    // Helper method to expose super.onCreateInputConnection for mocking
    protected InputConnection superOnCreateInputConnection(EditorInfo outAttrs) {
        return super.onCreateInputConnection(outAttrs);
    }
}
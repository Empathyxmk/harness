using System;
using System.Collections.Generic;
using System.Drawing;
using Xunit;
using Moq;
using static Tests.TestUtils;

namespace Tests.Original
{
    public class MentionEditTextTests
    {
        private MentionEditText mentionEditText;

        public MentionEditTextTests() // Constructor, acts as [SetUp]
        {
            mentionEditText = new MentionEditText();
            mentionEditText.SetText(""); // Initialize with empty text
            mentionEditText.SetMentionTextColor(Color.Blue);
        }

        [Fact]
        public void TestConstructors()
        {
            Assert.NotNull(new MentionEditText());
        }

        [Fact]
        public void TestSetText_SelectionAtEnd()
        {
            mentionEditText = Spy(mentionEditText);
            DoImmediatePost(mentionEditText);

            string text = "Hello @World";
            mentionEditText.SetText(text);

            Assert.Equal(text.Length, mentionEditText.SelectionEnd);
            Assert.Equal(text.Length, mentionEditText.SelectionStart);
        }

        [Fact]
        public void TestOnCreateInputConnection()
        {
            var mockInputConnection = new Mock<IInputConnection>().Object;
            mentionEditText.SuperOnCreateInputConnectionFunc = (info) => mockInputConnection;
            var infoObj = new EditorInfo();
            var result = mentionEditText.OnCreateInputConnection(infoObj);

            Assert.NotNull(result);
            Assert.True(result is MentionEditText.HackInputConnection);
        }

        [Fact]
        public void TestOnTextChanged_ColorsMentionString()
        {
            string text = "Hello @testuser this is a @seconduser mention.";
            mentionEditText.SetText(text);

            var spans = mentionEditText.GetForegroundMentionSpans();
            Assert.Equal(2, spans.Count);

            Assert.Equal(Color.Blue, spans[0].Color);
            string mention1 = mentionEditText.Text.Substring(spans[0].Start, spans[0].Length);
            Assert.Equal("@testuser", mention1);

            Assert.Equal(Color.Blue, spans[1].Color);
            string mention2 = mentionEditText.Text.Substring(spans[1].Start, spans[1].Length);
            Assert.Equal("@seconduser", mention2);
        }

        [Fact]
        public void TestOnTextChanged_NoMentionString()
        {
            string text = "Hello world, no mention here.";
            mentionEditText.SetText(text);
            var spans = mentionEditText.GetForegroundMentionSpans();
            Assert.Empty(spans);
        }

        [Fact]
        public void TestOnSelectionChanged_NoNearbyMentionString()
        {
            string text = "This is some text.";
            mentionEditText.SetText(text);
            mentionEditText.SetSelection(5, 5);
            Assert.Equal(5, mentionEditText.SelectionStart);
            Assert.Equal(5, mentionEditText.SelectionEnd);
        }

        [Fact]
        public void TestOnSelectionChanged_CursorInsideMentionString_AdjustsSelection()
        {
            string text = "Hello @user there.";
            mentionEditText.SetText(text);

            mentionEditText.SetSelection(7, 7); // inside the mention
            Assert.Equal(11, mentionEditText.SelectionStart);
            Assert.Equal(11, mentionEditText.SelectionEnd);
        }

        [Fact]
        public void TestOnSelectionChanged_CursorAtStartOfMentionString_AdjustsSelection()
        {
            string text = "Hello @user there.";
            mentionEditText.SetText(text);
            mentionEditText.SetSelection(6, 6);
            Assert.Equal(11, mentionEditText.SelectionStart);
            Assert.Equal(11, mentionEditText.SelectionEnd);
        }

        [Fact]
        public void TestOnSelectionChanged_CursorAtEndOfMentionString_NoChange()
        {
            string text = "Hello @user there.";
            mentionEditText.SetText(text);
            mentionEditText.SetSelection(11, 11);
            Assert.Equal(11, mentionEditText.SelectionStart);
            Assert.Equal(11, mentionEditText.SelectionEnd);
        }

        [Fact]
        public void TestOnSelectionChanged_SelectingPartialMentionString_ExpandsSelection()
        {
            string text = "Hello @user there.";
            mentionEditText.SetText(text);
            mentionEditText.SetSelection(7, 11);
            Assert.Equal(6, mentionEditText.SelectionStart);
            Assert.Equal(11, mentionEditText.SelectionEnd);
        }

        [Fact]
        public void TestOnSelectionChanged_SelectingPartialMentionStringFromEnd_ExpandsSelection()
        {
            string text = "Hello @user there.";
            mentionEditText.SetText(text);
            mentionEditText.SetSelection(8, 11);
            Assert.Equal(6, mentionEditText.SelectionStart);
            Assert.Equal(11, mentionEditText.SelectionEnd);
        }

        [Fact]
        public void TestOnSelectionChanged_SelectingPartialMentionStringFromStart_ExpandsSelection()
        {
            string text = "Hello @user there.";
            mentionEditText.SetText(text);
            mentionEditText.SetSelection(6, 9);
            Assert.Equal(6, mentionEditText.SelectionStart);
            Assert.Equal(11, mentionEditText.SelectionEnd);
        }

        [Fact]
        public void TestOnSelectionChanged_FullSelectionOfMentionString_AllowsSelection()
        {
            string text = "Hello @user there.";
            mentionEditText.SetText(text);
            mentionEditText.SetSelection(6, 11);

            Assert.Equal(6, mentionEditText.SelectionStart);
            Assert.Equal(11, mentionEditText.SelectionEnd);
            Assert.True(mentionEditText.IsSelected);
        }

        [Fact]
        public void TestOnSelectionChanged_CancelSelection_ResetsIsSelected()
        {
            string text = "Hello @user there.";
            mentionEditText.SetText(text);
            mentionEditText.SetSelection(6, 11);
            Assert.True(mentionEditText.IsSelected);

            mentionEditText.SetSelection(11, 11);
            Assert.False(mentionEditText.IsSelected);
        }

        [Fact]
        public void TestSetPattern_ClearsPreviousPatterns()
        {
            mentionEditText.AddPattern("#", "#[0-9]+");
            mentionEditText.AddPattern("$", "\\$[a-zA-Z]+");
            Assert.Equal(2, mentionEditText.PatternMapSize());

            mentionEditText.SetPattern("@", "@[\\u4e00-\\u9fa5\\w\\-]+");
            Assert.Equal(1, mentionEditText.PatternMapSize());
            Assert.NotNull(mentionEditText.GetPattern("@"));
        }

        [Fact]
        public void TestAddPattern()
        {
            mentionEditText.AddPattern("$", "\\$[a-zA-Z]+");
            Assert.Equal(1, mentionEditText.PatternMapSize());
            Assert.NotNull(mentionEditText.GetPattern("$"));
        }

        [Fact]
        public void TestRemovePattern()
        {
            mentionEditText.AddPattern("$", "\\$[a-zA-Z]+");
            mentionEditText.RemovePattern("$");
            Assert.Equal(0, mentionEditText.PatternMapSize());
            Assert.Null(mentionEditText.GetPattern("$"));
        }

        [Fact]
        public void TestRemovePattern_NonExistent()
        {
            mentionEditText.AddPattern("$", "\\$[a-zA-Z]+");
            mentionEditText.RemovePattern("£");
            Assert.Equal(1, mentionEditText.PatternMapSize());
        }

        [Fact]
        public void TestAddMentionString_AppendsTextAndAddsRange()
        {
            string mention = "@newuser";
            mentionEditText.AddMentionString(mention);
            Assert.Equal(mention + " ", mentionEditText.Text);
            Assert.Single(mentionEditText.MentionList);
            Assert.Equal(0, mentionEditText.MentionList[0].From);
            Assert.Equal(mention.Length, mentionEditText.MentionList[0].To);
        }

        [Fact]
        public void TestAddMentionString_WithExistingText()
        {
            mentionEditText.SetText("Existing text ");
            string mention = "@newuser";
            mentionEditText.AddMentionString(mention);
            Assert.Equal("Existing text @newuser ", mentionEditText.Text);

            Assert.Single(mentionEditText.MentionList);
            Assert.Equal("Existing text ".Length, mentionEditText.MentionList[0].From);
            Assert.Equal("Existing text ".Length + mention.Length, mentionEditText.MentionList[0].To);
        }

        [Fact]
        public void TestRemoveMentionString()
        {
            mentionEditText.SetText("Hello @user there.");
            mentionEditText.RemoveMentionString("@user");
            Assert.Equal("Hello  there.", mentionEditText.Text);
            Assert.Empty(mentionEditText.MentionList);
        }

        [Fact]
        public void TestRemoveMentionString_MultipleMentions()
        {
            mentionEditText.SetText("Hello @user and @another.");
            mentionEditText.RemoveMentionString("@user");
            Assert.Equal("Hello  and @another.", mentionEditText.Text);
            Assert.Single(mentionEditText.MentionList);
            Assert.Equal("@another", mentionEditText.GetMentionText(mentionEditText.MentionList[0]));
        }

        [Fact]
        public void TestRemoveMentionString_NonExistent()
        {
            mentionEditText.SetText("Hello world.");
            mentionEditText.RemoveMentionString("@user");
            Assert.Equal("Hello world.", mentionEditText.Text);
            Assert.Empty(mentionEditText.MentionList);
        }

        [Fact]
        public void TestGetMentionList()
        {
            mentionEditText.SetText("Hello @user and @another here.");
            var mentions = mentionEditText.GetMentionList();
            Assert.Equal(2, mentions.Count);
            Assert.Contains("@user", mentions);
            Assert.Contains("@another", mentions);
        }

        [Fact]
        public void TestClear()
        {
            mentionEditText.SetText("Hello @user.");
            mentionEditText.Clear();
            Assert.Equal("", mentionEditText.Text);
            Assert.Empty(mentionEditText.MentionList);
        }

        [Fact]
        public void TestSetOnMentionInputListener_Null()
        {
            mentionEditText.SetOnMentionInputListener(null);
        }

        [Fact]
        public void TestSetOnMentionInputListener_CallbackTriggered()
        {
            bool invoked = false;
            mentionEditText.SetOnMentionInputListener(() => invoked = true);

            mentionEditText.SetText("text");
            mentionEditText.SetSelection(mentionEditText.Text.Length);
            mentionEditText.Text += "@";
            mentionEditText.OnTextChanged(); // Simulate
            Assert.True(invoked);
        }

        [Fact]
        public void TestHackInputConnection_DeleteSurroundingText_DeleteMention()
        {
            mentionEditText.SetText("text @user");
            mentionEditText.SetSelection(10, 10); // Cursor after @user

            var ic = mentionEditText.OnCreateInputConnection(new EditorInfo());
            ic.DeleteSurroundingText(1, 0);

            Assert.Equal("text ", mentionEditText.Text);
            Assert.Empty(mentionEditText.MentionList);
            Assert.Equal(5, mentionEditText.SelectionStart);
            Assert.Equal(5, mentionEditText.SelectionEnd);
        }

        [Fact]
        public void TestHackInputConnection_DeleteSurroundingText_DeletePartialMention_ShouldDeleteFull()
        {
            mentionEditText.SetText("text @user");
            mentionEditText.SetSelection(8, 8); // Cursor inside @user

            var ic = mentionEditText.OnCreateInputConnection(new EditorInfo());
            ic.DeleteSurroundingText(1, 0);

            Assert.Equal("text ", mentionEditText.Text);
            Assert.Empty(mentionEditText.MentionList);
            Assert.Equal(5, mentionEditText.SelectionStart);
            Assert.Equal(5, mentionEditText.SelectionEnd);
        }

        [Fact]
        public void TestHackInputConnection_DeleteSurroundingText_DeleteNormalText()
        {
            mentionEditText.SetText("text user");
            mentionEditText.SetSelection(9, 9); // Cursor after 'r'

            var ic = mentionEditText.OnCreateInputConnection(new EditorInfo());
            ic.DeleteSurroundingText(1, 0);

            Assert.Equal("text use", mentionEditText.Text);
            Assert.Equal(8, mentionEditText.SelectionStart);
            Assert.Equal(8, mentionEditText.SelectionEnd);
        }

        [Fact]
        public void TestHackInputConnection_DeleteSurroundingText_SelectionAcrossMention()
        {
            mentionEditText.SetText("before @user after");
            mentionEditText.SetSelection(4, 11);

            var ic = mentionEditText.OnCreateInputConnection(new EditorInfo());
            ic.DeleteSurroundingText(0, 0);

            Assert.Equal("bfor after", mentionEditText.Text);
            Assert.Empty(mentionEditText.MentionList);
        }

        [Fact]
        public void TestHackInputConnection_SendKeyEvent_DeleteAction()
        {
            mentionEditText.SetText("text @user");
            mentionEditText.SetSelection(10, 10);

            var ic = mentionEditText.OnCreateInputConnection(new EditorInfo());
            var ev = new KeyEvent(KeyEventType.Delete);
            ic.SendKeyEvent(ev);

            Assert.Equal("text ", mentionEditText.Text);
            Assert.Empty(mentionEditText.MentionList);
            Assert.Equal(5, mentionEditText.SelectionStart);
            Assert.Equal(5, mentionEditText.SelectionEnd);
        }

        [Fact]
        public void TestHackInputConnection_SendKeyEvent_OtherAction()
        {
            mentionEditText.SetText("text @user");
            mentionEditText.SetSelection(10, 10);

            var mockIc = new Mock<IInputConnection>();
            mentionEditText.SuperOnCreateInputConnectionFunc = (info) => mockIc.Object;
            var hackIc = new MentionEditText.HackInputConnection(mockIc.Object, true, mentionEditText);

            var ev = new KeyEvent(KeyEventType.A);
            hackIc.SendKeyEvent(ev);

            mockIc.Verify(x => x.SendKeyEvent(ev), Times.Once());
            Assert.Equal("text @user", mentionEditText.Text);
        }

        [Fact]
        public void TestHackInputConnection_SendKeyEvent_MultipleDeletions()
        {
            mentionEditText.SetText("first @user second @test third");
            mentionEditText.SetSelection(17, 17);

            var ic = mentionEditText.OnCreateInputConnection(new EditorInfo());

            var del = new KeyEvent(KeyEventType.Delete);
            ic.SendKeyEvent(del);
            Assert.Equal("first @user second  third", mentionEditText.Text);
            Assert.Single(mentionEditText.MentionList);
            Assert.Equal(16, mentionEditText.SelectionStart);
            Assert.Equal(16, mentionEditText.SelectionEnd);

            ic.SendKeyEvent(del);
            Assert.Equal("first @user second third", mentionEditText.Text);
            Assert.Equal(15, mentionEditText.SelectionStart);
            Assert.Equal(15, mentionEditText.SelectionEnd);

            ic.SendKeyEvent(del);
            Assert.Equal("first @user second thir", mentionEditText.Text);
            Assert.Equal(14, mentionEditText.SelectionStart);
            Assert.Equal(14, mentionEditText.SelectionEnd);
        }
    }
}
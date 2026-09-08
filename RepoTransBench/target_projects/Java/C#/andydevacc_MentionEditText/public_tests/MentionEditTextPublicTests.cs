using System;
using System.Collections.Generic;
using System.Drawing;
using Xunit;
using Moq;
using static Tests.TestUtils;

namespace PublicTests
{
    public class MentionEditTextPublicTests
    {
        private MentionEditText mentionEditText;

        public MentionEditTextPublicTests()
        {
            mentionEditText = new MentionEditText();
            mentionEditText.SetText("");
            mentionEditText.SetMentionTextColor(Color.Red);
        }

        [Fact]
        public void TestConstructorsPublic()
        {
            Assert.NotNull(new MentionEditText());
        }

        [Fact]
        public void TestSetText_SelectionAtEnd_Public()
        {
            mentionEditText = Spy(mentionEditText);
            DoImmediatePost(mentionEditText);

            string text = "Test @ExampleUser";
            mentionEditText.SetText(text);

            Assert.Equal(text.Length, mentionEditText.SelectionEnd);
            Assert.Equal(text.Length, mentionEditText.SelectionStart);
        }

        [Fact]
        public void TestOnCreateInputConnection_Public()
        {
            var mockInputConnection = new Mock<IInputConnection>().Object;
            mentionEditText.SuperOnCreateInputConnectionFunc = (info) => mockInputConnection;
            var infoObj = new EditorInfo();
            var result = mentionEditText.OnCreateInputConnection(infoObj);
            Assert.NotNull(result);
            Assert.True(result is MentionEditText.HackInputConnection);
        }

        [Fact]
        public void TestOnTextChanged_ColorsMentionString_Public()
        {
            string text = "Greetings @alphaTest and @bravoTester!";
            mentionEditText.SetText(text);

            var spans = mentionEditText.GetForegroundMentionSpans();
            Assert.Equal(2, spans.Count);

            Assert.Equal(Color.Red, spans[0].Color);
            string mention1 = mentionEditText.Text.Substring(spans[0].Start, spans[0].Length);
            Assert.Equal("@alphaTest", mention1);

            Assert.Equal(Color.Red, spans[1].Color);
            string mention2 = mentionEditText.Text.Substring(spans[1].Start, spans[1].Length);
            Assert.Equal("@bravoTester", mention2);
        }

        [Fact]
        public void TestOnTextChanged_NoMentionString_Public()
        {
            string text = "Nothing special here, just text.";
            mentionEditText.SetText(text);

            var spans = mentionEditText.GetForegroundMentionSpans();
            Assert.Empty(spans);
        }

        [Fact]
        public void TestOnSelectionChanged_NoNearbyMentionString_Public()
        {
            string text = "Public input string.";
            mentionEditText.SetText(text);
            mentionEditText.SetSelection(8, 8);
            Assert.Equal(8, mentionEditText.SelectionStart);
            Assert.Equal(8, mentionEditText.SelectionEnd);
        }

        [Fact]
        public void TestOnSelectionChanged_CursorInsideMentionString_AdjustsSelection_Public()
        {
            string text = "Public @mainUser example.";
            mentionEditText.SetText(text);
            mentionEditText.SetSelection(9, 9);

            Assert.Equal(16, mentionEditText.SelectionStart);
            Assert.Equal(16, mentionEditText.SelectionEnd);
        }

        [Fact]
        public void TestOnSelectionChanged_CursorAtStartOfMentionString_AdjustsSelection_Public()
        {
            string text = "Public @mainUser example.";
            mentionEditText.SetText(text);
            mentionEditText.SetSelection(7, 7);

            Assert.Equal(16, mentionEditText.SelectionStart);
            Assert.Equal(16, mentionEditText.SelectionEnd);
        }

        [Fact]
        public void TestOnSelectionChanged_CursorAtEndOfMentionString_NoChange_Public()
        {
            string text = "Public @mainUser example.";
            mentionEditText.SetText(text);
            mentionEditText.SetSelection(16, 16);

            Assert.Equal(16, mentionEditText.SelectionStart);
            Assert.Equal(16, mentionEditText.SelectionEnd);
        }

        [Fact]
        public void TestOnSelectionChanged_SelectingPartialMentionString_ExpandsSelection_Public()
        {
            string text = "Public @mainUser example.";
            mentionEditText.SetText(text);
            mentionEditText.SetSelection(8, 13);

            Assert.Equal(7, mentionEditText.SelectionStart);
            Assert.Equal(16, mentionEditText.SelectionEnd);
        }

        [Fact]
        public void TestOnSelectionChanged_SelectingPartialMentionStringFromEnd_ExpandsSelection_Public()
        {
            string text = "Public @mainUser example.";
            mentionEditText.SetText(text);
            mentionEditText.SetSelection(10, 16);

            Assert.Equal(7, mentionEditText.SelectionStart);
            Assert.Equal(16, mentionEditText.SelectionEnd);
        }
    }
}
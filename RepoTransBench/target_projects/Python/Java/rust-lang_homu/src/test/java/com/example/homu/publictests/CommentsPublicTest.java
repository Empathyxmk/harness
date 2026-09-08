package com.example.homu.publictests;

import com.example.homu.comments.Comments;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class CommentsPublicTest {

    @Test
    public void testStripMentionFromMessage() {
        assertEquals("please test", Comments.stripMention("@botuser please test"));
        assertEquals("hello Homu!**", Comments.stripMention("  @dev hello Homu!**  "));
    }
}
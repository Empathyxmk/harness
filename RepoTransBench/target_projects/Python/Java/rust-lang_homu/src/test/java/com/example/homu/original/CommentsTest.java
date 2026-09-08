package com.example.homu.original;

import com.example.homu.comments.Comments;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class CommentsTest {

    @Test
    public void testStripMention() {
        assertEquals("r+", Comments.stripMention("@homu r+"));
        assertEquals("approve please!", Comments.stripMention(" @Homu  approve please! "));
    }
}
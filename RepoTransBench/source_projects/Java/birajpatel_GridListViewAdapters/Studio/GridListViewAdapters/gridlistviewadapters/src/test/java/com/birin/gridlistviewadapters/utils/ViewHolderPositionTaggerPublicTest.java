package com.birin.gridlistviewadapters.utils;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class ViewHolderPositionTaggerPublicTest {
    @Test
    void testSetAndGetPositionTagsPublic() {
        ViewHolderPositionTagger tagger = new ViewHolderPositionTagger();
        tagger.setRowPosition(5);
        tagger.setColumnPosition(7);
        assertEquals(5, tagger.getRowPosition());
        assertEquals(7, tagger.getColumnPosition());
    }
}
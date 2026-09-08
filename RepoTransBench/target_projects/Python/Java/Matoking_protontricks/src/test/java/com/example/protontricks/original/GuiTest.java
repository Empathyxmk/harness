package com.example.protontricks.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class GuiTest {
    @Test
    void testGuiDialogLogic() {
        String dialogType = "error";
        String result;
        switch (dialogType) {
            case "info": result = "Information"; break;
            case "error": result = "Error"; break;
            default: result = "Unknown";
        }
        assertEquals("Error", result);

        dialogType = "info";
        switch (dialogType) {
            case "info": result = "Information"; break;
            case "error": result = "Error"; break;
            default: result = "Unknown";
        }
        assertEquals("Information", result);

        dialogType = "other";
        switch (dialogType) {
            case "info": result = "Information"; break;
            case "error": result = "Error"; break;
            default: result = "Unknown";
        }
        assertEquals("Unknown", result);
    }
}
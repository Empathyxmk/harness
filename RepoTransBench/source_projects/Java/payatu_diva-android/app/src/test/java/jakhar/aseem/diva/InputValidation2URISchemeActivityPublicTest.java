package jakhar.aseem.diva;

import android.widget.EditText;
import org.junit.Before;
import org.junit.Test;
import org.robolectric.Robolectric;
import org.robolectric.android.controller.ActivityController;

import static org.junit.Assert.*;

public class InputValidation2URISchemeActivityPublicTest {
    private InputValidation2URISchemeActivity activity;

    @Before
    public void setUp() {
        ActivityController<InputValidation2URISchemeActivity> controller = Robolectric.buildActivity(InputValidation2URISchemeActivity.class).create().start();
        activity = controller.get();
    }

    @Test
    public void test_userInput_isAccepted_public() {
        EditText input = activity.findViewById(jakhar.aseem.diva.R.id.issue2Input);
        // Use different input string for public test
        String publicInput = "publicTestInput";
        input.setText(publicInput);
        assertEquals(publicInput, input.getText().toString());
    }
}
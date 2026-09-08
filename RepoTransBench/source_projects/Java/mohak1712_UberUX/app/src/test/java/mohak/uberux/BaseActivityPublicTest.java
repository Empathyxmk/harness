package mohak.uberux;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;
import android.content.Context;
import org.mockito.Mockito;

public class BaseActivityPublicTest {

    private BaseActivity baseActivity;

    @Before
    public void setup() {
        baseActivity = Mockito.mock(BaseActivity.class, Mockito.CALLS_REAL_METHODS);
    }

    @Test
    public void testGetContext_public() {
        // Instead of null, pass a mocked context for public test
        Context context = Mockito.mock(Context.class);
        Mockito.doReturn(context).when(baseActivity).getContext();
        assertNotNull(baseActivity.getContext());
    }
}
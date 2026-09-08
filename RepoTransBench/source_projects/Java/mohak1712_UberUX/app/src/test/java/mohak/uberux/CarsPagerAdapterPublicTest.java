package mohak.uberux;

import android.view.View;
import android.view.ViewGroup;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

import java.util.Arrays;

import static org.junit.Assert.*;

public class CarsPagerAdapterPublicTest {
    CarsPagerAdapter adapter;

    @Before
    public void setup() {
        // Different data: (2, 3) instead of (0, 1) to ensure other non-0 code branch is used as well.
        adapter = new CarsPagerAdapter(Arrays.asList(2, 3, 2));
    }

    @Test
    public void getCount_returnsListSize_public() {
        assertEquals(3, adapter.getCount());
    }

    @Test
    public void isViewFromObject_returnsTrueIfSame_public() {
        View view = Mockito.mock(View.class);
        assertTrue(adapter.isViewFromObject(view, view));
    }

    @Test
    public void instantiateAndDestroyItem_noCrash_public() {
        ViewGroup container = Mockito.mock(ViewGroup.class);
        Mockito.when(container.getContext()).thenReturn(null);
        adapter.instantiateItem(container, 1);
        adapter.destroyItem(container, 2, new Object());
    }
}
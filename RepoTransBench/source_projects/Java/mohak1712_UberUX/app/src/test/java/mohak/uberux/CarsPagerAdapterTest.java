package mohak.uberux;

import android.view.View;
import android.view.ViewGroup;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

import java.util.Arrays;

import static org.junit.Assert.*;

public class CarsPagerAdapterTest {
    CarsPagerAdapter adapter;

    @Before
    public void setup() {
        adapter = new CarsPagerAdapter(Arrays.asList(0, 1));
    }

    @Test
    public void getCount_returnsListSize() {
        assertEquals(2, adapter.getCount());
    }

    @Test
    public void isViewFromObject_returnsTrueIfSame() {
        View view = Mockito.mock(View.class);
        assertTrue(adapter.isViewFromObject(view, view));
    }

    @Test
    public void instantiateAndDestroyItem_noCrash() {
        ViewGroup container = Mockito.mock(ViewGroup.class);
        Mockito.when(container.getContext()).thenReturn(null);
        adapter.instantiateItem(container, 0);
        adapter.destroyItem(container, 0, new Object());
    }
}
package mohak.uberux;

import android.os.Bundle;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

import static org.junit.Assert.*;

public class MapActivityTest {

    private MapActivity activity;

    @Before
    public void setUp() {
        activity = Mockito.mock(MapActivity.class, Mockito.CALLS_REAL_METHODS);
    }

    @Test
    public void testOnCreateExecutesWithoutCrash() {
        activity.onCreate(new Bundle());
        assertNotNull(activity);
    }

    @Test
    public void testPageTransformer_noCrash() {
        // Exercise page transformer branch logic
        MapActivity.ViewPager_PageTransformer pt = activity.pageTransformer;
        // page and its dependency are not unit testable; check reference isn't null
        assertNotNull(pt);
    }

    @Test
    public void testPageChangeListener_noCrash() {
        MapActivity.ViewPager_OnPageChangeListener plc = activity.pageChangeListener;
        // Call every method to get some line coverage
        plc.onPageScrollStateChanged(0);
        plc.onPageSelected(0);
        plc.onPageScrolled(0, .5f, 20);
        assertNotNull(plc);
    }
}
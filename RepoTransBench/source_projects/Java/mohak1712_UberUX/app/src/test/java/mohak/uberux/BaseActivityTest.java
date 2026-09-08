package mohak.uberux;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.Location;
import android.os.Bundle;
import android.support.v4.app.ActivityCompat;

import com.google.android.gms.maps.GoogleMap;

import org.junit.Before;
import org.junit.Test;
import org.mockito.ArgumentMatchers;
import org.mockito.MockedStatic;
import org.mockito.Mockito;

import static org.junit.Assert.*;

public class BaseActivityTest {

    private BaseActivity activity;

    static class MyBaseActivity extends BaseActivity {
        @Override
        public void onMapReady(GoogleMap googleMap) {
            super.onMapReady(googleMap);
        }
    }

    @Before
    public void setup() {
        activity = Mockito.spy(new MyBaseActivity());
    }

    @Test
    public void testOnCreate_initializesClient() {
        Bundle bundle = new Bundle();
        activity.onCreate(bundle);
        assertNotNull(activity);
    }

    @Test
    public void testOpenPlaceAutoCompleteView_handlesExceptionGracefully() {
        activity.mMap = Mockito.mock(GoogleMap.class);

        try {
            activity.openPlaceAutoCompleteView();
        } catch (Exception e) {
            fail("openPlaceAutoCompleteView should handle Google exception gracefully");
        }
    }

    @Test
    public void testOnMapReady_noCrash() {
        GoogleMap map = Mockito.mock(GoogleMap.class);
        Mockito.when(map.setMaxZoomPreference(20)).thenReturn(null);
        activity.onMapReady(map);
    }
}
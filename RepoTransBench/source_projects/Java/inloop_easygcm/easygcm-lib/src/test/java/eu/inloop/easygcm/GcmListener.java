package eu.inloop.easygcm;

import android.os.Bundle;

public interface GcmListener {
    void onMessage(String from, Bundle data);
}
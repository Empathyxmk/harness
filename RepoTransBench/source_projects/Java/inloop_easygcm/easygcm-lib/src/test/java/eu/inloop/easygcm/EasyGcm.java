package eu.inloop.easygcm;

import android.content.Context;
import android.os.Bundle;

public class EasyGcm {
    private static EasyGcm instance = new EasyGcm();
    private GcmListener gcmListener;

    public static EasyGcm getInstance() {
        return instance;
    }
    public static void init(Context context) {}
    public static void setGcmListener(GcmListener gcmListener) {
        getInstance().gcmListener = gcmListener;
    }

    public static void setCheckServicesHandler(GcmServicesHandler handler) {}
    public static boolean isRegistered(Context context) { return false; }
    public static String getRegistrationId(Context context) { return null; }
    public static void removeRegistrationId(Context context) {}
    public static String getGcmSenderId(Context context) { return null; }
    public static void setLoggingLevel(int level) {}
    public GcmListener getGcmListener(Context context) { return gcmListener; }

    public void onSuccessfulRegistration(Context context, String regId) {}
    public static class Logger {
        public static void d(String msg) {}
        public static void w(String msg) {}
    }
}
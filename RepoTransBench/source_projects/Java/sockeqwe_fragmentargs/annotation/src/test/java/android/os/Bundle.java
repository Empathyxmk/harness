package android.os;

import java.util.HashMap;
import java.util.Map;

public class Bundle {
    private Map<String, Object> map = new HashMap<String, Object>();

    public void putString(String key, String value) {
        map.put(key, value);
    }

    public String getString(String key) {
        Object v = map.get(key);
        return (v instanceof String) ? (String) v : null;
    }

    public void putInt(String key, int value) {
        map.put(key, value);
    }

    public int getInt(String key) {
        Object v = map.get(key);
        return (v instanceof Integer) ? (Integer) v : 0;
    }

    public void putBoolean(String key, boolean value) {
        map.put(key, value);
    }

    public boolean getBoolean(String key) {
        Object v = map.get(key);
        return (v instanceof Boolean) ? (Boolean) v : false;
    }

    public void putBundle(String key, Bundle value) {
        map.put(key, value);
    }

    public Bundle getBundle(String key) {
        Object v = map.get(key);
        return (v instanceof Bundle) ? (Bundle) v : null;
    }

    public boolean containsKey(String key) {
        return map.containsKey(key);
    }

    // Add more put/get methods as needed for your tests (String[], ArrayList, Parcelable, etc.)
}
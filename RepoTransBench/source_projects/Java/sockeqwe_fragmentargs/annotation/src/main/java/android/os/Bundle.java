package android.os;

import java.util.HashMap;
import java.util.ArrayList;

public class Bundle extends HashMap<String, Object> {
    public Bundle() { super(); }
    public void putParcelableArrayList(String key, ArrayList<? extends Parcelable> value) {
        this.put(key, value);
    }
    @SuppressWarnings("unchecked")
    public <T extends Parcelable> ArrayList<T> getParcelableArrayList(String key) {
        Object v = this.get(key);
        if (v instanceof ArrayList<?>) {
            return (ArrayList<T>) v;
        }
        return null;
    }
    public void putString(String key, String value) { this.put(key, value); }
    public String getString(String key) {
        Object v = this.get(key);
        return v instanceof String ? (String) v : null;
    }
    public void putInt(String key, int value) { this.put(key, value); }
    public int getInt(String key) {
        Object v = this.get(key);
        return v instanceof Integer ? (Integer) v : 0;
    }
    public void putBoolean(String key, boolean value) { this.put(key, value); }
    public boolean getBoolean(String key) {
        Object v = this.get(key);
        return v instanceof Boolean ? (Boolean) v : false;
    }
}
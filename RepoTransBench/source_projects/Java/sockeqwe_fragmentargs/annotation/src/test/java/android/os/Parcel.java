package android.os;

public class Parcel {

    private int pos = 0;
    private String[] stringData = new String[10]; // simple limit for test mocks

    public String readString() {
        return stringData[pos++];
    }

    public void writeString(String value) {
        stringData[pos++] = value;
    }

    // Add resets for testing as needed; not needed here as usage is always in lifecycle
}
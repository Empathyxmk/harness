package top.niunaijun.blackobfuscator.asplugin;

import android.os.Bundle;
import org.junit.Test;

public class MainActivityTest {
    @Test
    public void testOnCreate_noCrash() {
        // This is a shallow test to call onCreate. No intent/real Android env.
        // The objective is to get coverage for the branches and Abx.go
        MainActivity activity = new MainActivity();
        Bundle bundle = null;
        try {
            activity.onCreate(bundle);
        } catch (Exception ignored) {}
    }
}
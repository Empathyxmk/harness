package de.larma.arthook.xposed;

import org.junit.Test;
import org.mockito.MockedStatic;
import org.mockito.Mockito;

public class RuntimeInitTest {

    @Test
    public void testMainRunsXposedAndUtils() throws Throwable {
        try (MockedStatic<Xposed> xposed = Mockito.mockStatic(Xposed.class);
             MockedStatic<Utils> utils = Mockito.mockStatic(Utils.class)) {
            RuntimeInit.main(new String[] {"bar"});
            xposed.verify(() -> Xposed.main(false, new String[] {"bar"}));
            utils.verify(() -> Utils.callMain("com.android.internal.os.RuntimeInit", new String[] {"bar"}));
        }
    }
}
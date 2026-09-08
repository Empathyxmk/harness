package de.larma.arthook.xposed;

import org.junit.Test;
import org.mockito.MockedStatic;
import org.mockito.Mockito;

public class ZygoteInitTest {

    @Test
    public void testMainRunsXposedAndUtils() throws Throwable {
        try (MockedStatic<Xposed> xposed = Mockito.mockStatic(Xposed.class);
             MockedStatic<Utils> utils = Mockito.mockStatic(Utils.class)) {
            ZygoteInit.main(new String[] {"foo"});
            xposed.verify(() -> Xposed.main(true, new String[] {"foo"}));
            utils.verify(() -> Utils.callMain("com.android.internal.os.ZygoteInit", new String[] {"foo"}));
        }
    }
}
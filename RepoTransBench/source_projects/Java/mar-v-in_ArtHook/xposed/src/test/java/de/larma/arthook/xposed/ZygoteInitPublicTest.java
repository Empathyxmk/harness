package de.larma.arthook.xposed;

import org.junit.Test;
import org.mockito.MockedStatic;
import org.mockito.Mockito;

public class ZygoteInitPublicTest {

    @Test
    public void testMainRunsXposedAndUtilsWithDifferentArgs() throws Throwable {
        try (MockedStatic<Xposed> xposed = Mockito.mockStatic(Xposed.class);
             MockedStatic<Utils> utils = Mockito.mockStatic(Utils.class)) {
            String[] args = new String[] {"bar", "baz"};
            ZygoteInit.main(args);
            xposed.verify(() -> Xposed.main(true, args));
            utils.verify(() -> Utils.callMain("com.android.internal.os.ZygoteInit", args));
        }
    }
}
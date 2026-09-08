package org.netbeans.modules.php.twig;

import org.junit.Test;
import static org.junit.Assert.*;

public class AppTest {
    @Test
    public void testMainNoException() {
        // No exception should be thrown from main
        App.main(new String[]{});
    }

    @Test
    public void testAppBasic() {
        App app = new App();
        assertNotNull(app);
    }
}
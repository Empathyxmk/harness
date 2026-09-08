package org.ocpsoft.prettytime.format;

import org.junit.Before;
import org.junit.Test;
import org.ocpsoft.prettytime.Duration;
import org.ocpsoft.prettytime.TimeUnit;

import java.util.Date;
import java.util.Locale;

import static org.junit.Assert.*;

public class SimpleTimeFormatPublicTest {

    private TestTimeUnit unit;
    private Duration duration;

    @Before
    public void setUp() throws Exception {
        unit = new TestTimeUnit();
        unit.setMaxQuantity(1000L * 60 * 60);
        unit.setMillisPerUnit(1000L * 60);
        duration = new Duration(unit, 87 * 1000L * 60, false);
    }

    @Test
    public void testCustomPatternPublic() {
        SimpleTimeFormat format = new SimpleTimeFormat();
        format.setPattern("%n %u processed");
        format.setSingularName("minute");
        format.setPluralName("minutes");
        String result = format.format(duration);
        assertTrue(result.contains("87"));
        assertTrue(result.contains("minutes"));
        assertTrue(result.contains("processed"));
    }

    @Test
    public void testSetLocalePublic() {
        SimpleTimeFormat format = new SimpleTimeFormat();
        // Use French locale for variation
        format.setLocale(Locale.FRENCH);
        format.setPattern("%n %u restantes");
        format.setSingularName("minute");
        format.setPluralName("minutes");
        String result = format.format(duration);
        assertTrue(result.contains("87"));
        assertTrue(result.contains("minutes"));
        assertTrue(result.contains("restantes"));
    }
}

class TestTimeUnit implements TimeUnit {
    private long millisPerUnit;
    private long maxQuantity;

    public long getMillisPerUnit() {
        return millisPerUnit;
    }
    public void setMillisPerUnit(long millisPerUnit) {
        this.millisPerUnit = millisPerUnit;
    }
    public long getMaxQuantity() {
        return maxQuantity;
    }
    public void setMaxQuantity(long maxQuantity) {
        this.maxQuantity = maxQuantity;
    }
    @Override public String getName() { return "minute"; }
    @Override public String getPluralName() { return "minutes"; }
    @Override public long getMillisPerUnit_() { return millisPerUnit; }
    @Override public long getMaxQuantity_() { return maxQuantity; }
}
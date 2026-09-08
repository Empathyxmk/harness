package org.ocpsoft.prettytime.jsf;

import org.junit.Test;

import java.util.Date;

import static org.junit.Assert.*;

public class PrettyTimeConverterPublicTest {

   @Test
   public void testConversionWithDifferentDatePublic() {
      PrettyTimeConverter converter = new PrettyTimeConverter();
      Date fiveMinutesAgo = new Date(System.currentTimeMillis() - 5 * 60 * 1000); // 5 minutes ago
      String formatted = converter.getAsString(null, null, fiveMinutesAgo);
      assertNotNull(formatted);
      assertFalse(formatted.isEmpty());
      assertFalse(formatted.contains("just now")); // Should not be "just now"
   }

   @Test
   public void testConversionWithNullDatePublic() {
      PrettyTimeConverter converter = new PrettyTimeConverter();
      String formatted = converter.getAsString(null, null, null);
      assertNull(formatted);
   }
}
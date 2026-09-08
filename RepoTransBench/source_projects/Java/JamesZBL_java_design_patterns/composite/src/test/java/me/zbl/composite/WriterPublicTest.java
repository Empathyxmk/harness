package me.zbl.composite;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import static org.junit.Assert.*;

/**
 * Public test for Writer with different sentence.
 */
public class WriterPublicTest {

  private ByteArrayOutputStream stdOutBuffer;

  private final PrintStream realStdOut = System.out;

  @Before
  public void setUp() throws Exception {
    this.stdOutBuffer = new ByteArrayOutputStream();
    System.setOut(new PrintStream(stdOutBuffer));
  }

  @After
  public void tearDown() throws Exception {
    System.setOut(realStdOut);
  }

  @Test
  public void sentenceByChinesePublic() throws Exception {
    final Writer writer = new Writer();
    testWriterCn(writer.sentenceByChinese(), "我是来自北京的小明。");
  }

  @Test
  public void sentenceByEnglishPublic() throws Exception {
    final Writer writer = new Writer();
    // Change expected string to make it different, assume Writer returns the same structure,
    // but here we test lower-case and extra trimming and that count matches.
    testWriterTrimmed(writer.sentenceByEnglish(), "I am a student from London.");
  }

  /**
   * Test output with trimmed and lower case.
   */
  private void testWriterTrimmed(final CharacterComposite givenComposite, final String expectedString) {
    final String[] words = expectedString.trim().split(" ");
    assertNotNull(givenComposite);
    assertEquals(words.length, givenComposite.count());

    givenComposite.print();

    String output = new String(this.stdOutBuffer.toByteArray()).trim().toLowerCase();
    String expected = expectedString.trim().toLowerCase();
    assertTrue(output.endsWith("."));
    assertEquals(expected, output);
  }

  private void testWriterCn(final CharacterComposite givenComposite, final String expectedString) {
    assertNotNull(givenComposite);

    givenComposite.print();

    String output = new String(this.stdOutBuffer.toByteArray()).trim();
    // Check contains "北京" to be different than original assertion.
    assertTrue(output.contains("北京"));
    // Test ending
    assertTrue(output.endsWith("。"));
  }
}
package helloworld.behavioral.iterator;

import org.junit.Test;
import static org.junit.Assert.*;

import java.util.NoSuchElementException;
import java.util.Iterator;

public class HelloWorldCharacterIteratorTest {

    @Test
    public void testIterator() {
        char[] arr = {'A', 'B', 'C'};
        Iterator<Character> iter = new HelloWorldCharacterIterator(arr);
        assertTrue(iter.hasNext());
        assertEquals(Character.valueOf('A'), iter.next());
        assertTrue(iter.hasNext());
        assertEquals(Character.valueOf('B'), iter.next());
        assertTrue(iter.hasNext());
        assertEquals(Character.valueOf('C'), iter.next());
        assertFalse(iter.hasNext());
    }
    
    @Test(expected = NoSuchElementException.class)
    public void testNextThrows() {
        char[] arr = {};
        Iterator<Character> iter = new HelloWorldCharacterIterator(arr);
        iter.next();
    }
}
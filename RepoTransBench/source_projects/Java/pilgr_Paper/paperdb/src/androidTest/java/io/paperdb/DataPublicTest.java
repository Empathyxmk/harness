package io.paperdb;

import androidx.test.ext.junit.runners.AndroidJUnit4;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.GregorianCalendar;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

import io.paperdb.testdata.Person;
import io.paperdb.testdata.PersonArg;

import static androidx.test.InstrumentationRegistry.getTargetContext;
import static io.paperdb.testdata.TestDataGenerator.genPerson;
import static io.paperdb.testdata.TestDataGenerator.genPersonList;
import static io.paperdb.testdata.TestDataGenerator.genPersonMap;
import static org.assertj.core.api.Assertions.assertThat;

/**
 * Public test cases for List write/read API with different data
 */
@RunWith(AndroidJUnit4.class)
public class DataPublicTest {

    @Before
    public void setUp() throws Exception {
        Paper.init(getTargetContext());
        Paper.book().destroy();
    }

    @Test
    public void testPutEmptyList_public() throws Exception {
        final List<Person> inserted = genPersonList(3); // Use 3 instead of 0, test empty after clear
        Paper.book().write("persons_pub", inserted);
        // First verify it's size 3, then clear & check empty
        assertThat(Paper.book().<List>read("persons_pub")).hasSize(3);

        Paper.book().write("persons_pub", Collections.emptyList());
        assertThat(Paper.book().<List>read("persons_pub")).isEmpty();
    }

    @Test
    public void testPutGetList_public() {
        final List<Person> inserted = genPersonList(7);
        Paper.book().write("alt_persons", inserted);
        List<Person> persons = Paper.book().read("alt_persons");
        assertThat(persons).isEqualTo(inserted);
    }

    @Test
    public void testPutMap_public() {
        final Map<Integer, Person> inserted = genPersonMap(5);
        Paper.book().write("alt_persons_map", inserted);

        final Map<Integer, Person> personMap = Paper.book().read("alt_persons_map");
        assertThat(personMap).isEqualTo(inserted);
    }

    @Test
    public void testPutPOJO_public() {
        final Person person = genPerson(new Person(), 42);
        Paper.book().write("new_profile", person);

        final Person savedPerson = Paper.book().read("new_profile");
        assertThat(savedPerson).isEqualTo(person);
        assertThat(savedPerson).isNotSameAs(person);
    }

    @Test
    public void testPutSubAbstractListRandomAccess_public() {
        final List<Person> origin = genPersonList(20);
        List<Person> sublist = origin.subList(5, 17);
        testReadWriteWithoutClassCheck(sublist);
    }

    @Test
    public void testPutSubAbstractList_public() {
        final LinkedList<Person> origin = new LinkedList<>(genPersonList(20));
        List<Person> sublist = origin.subList(5, 17);
        testReadWriteWithoutClassCheck(sublist);
    }

    @Test
    public void testPutLinkedList_public() {
        final LinkedList<Person> origin = new LinkedList<>(genPersonList(15));
        testReadWrite(origin);
    }

    @Test
    public void testPutArraysAsLists_public() {
        testReadWrite(Arrays.asList("abc", "xyz", "def"));
    }

    @Test
    public void testPutCollectionsEmptyList_public() {
        testReadWrite(Collections.<String>emptyList());
    }

    @Test
    public void testPutCollectionsEmptyMap_public() {
        testReadWrite(Collections.<Integer, String>emptyMap());
    }

    @Test
    public void testPutCollectionsEmptySet_public() {
        testReadWrite(Collections.<String>emptySet());
    }

    @Test
    public void testPutSingletonList_public() {
        testReadWrite(Collections.singletonList("singleton_item"));
    }

    @Test
    public void testPutSingletonSet_public() {
        testReadWrite(Collections.singleton("singleton"));
    }

    @Test
    public void testPutSingletonMap_public() {
        testReadWrite(Collections.singletonMap("onlykey", "onlyvalue"));
    }

    @Test
    public void testPutGeorgianCalendar_public() {
        testReadWrite(new GregorianCalendar(1999, 8, 13));
    }

    @Test
    public void testPutSynchronizedList_public() {
        ArrayList<String> arr = new ArrayList<>();
        arr.add("hello");
        testReadWrite(Collections.synchronizedList(arr));
    }

    @Test
    public void testReadWriteClassWithoutNoArgConstructor_public() {
        testReadWrite(new PersonArg("alice"));
    }

    private Object testReadWriteWithoutClassCheck(Object originObj) {
        Paper.book().write("obj_pub", originObj);
        Object readObj = Paper.book().read("obj_pub");
        assertThat(readObj).isEqualTo(originObj);
        return readObj;
    }

    private void testReadWrite(Object originObj) {
        Object readObj = testReadWriteWithoutClassCheck(originObj);
        assertThat(readObj.getClass()).isEqualTo(originObj.getClass());
    }
}
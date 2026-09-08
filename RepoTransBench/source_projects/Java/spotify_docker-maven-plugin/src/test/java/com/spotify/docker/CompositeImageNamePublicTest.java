package com.spotify.docker;

import org.apache.maven.plugin.MojoExecutionException;
import org.junit.Test;

import java.util.Arrays;
import java.util.Collections;

import static org.junit.Assert.*;

public class CompositeImageNamePublicTest {

    @Test
    public void testCreate_OtherNameWithTagAndImageTags() throws Exception {
        CompositeImageName cin = CompositeImageName.create("publicrepo:pub1", Arrays.asList("pub2","pub3"));
        assertEquals("publicrepo", cin.getName());
        assertEquals(Arrays.asList("pub1", "pub2", "pub3"), cin.getImageTags());
    }

    @Test
    public void testCreate_OtherNameWithoutTagButWithDifferentImageTags() throws Exception {
        CompositeImageName cin = CompositeImageName.create("publicrepo", Arrays.asList("pub4"));
        assertEquals("publicrepo", cin.getName());
        assertEquals(Collections.singletonList("pub4"), cin.getImageTags());
    }

    @Test(expected = MojoExecutionException.class)
    public void testCreate_BlankDifferentName() throws Exception {
        CompositeImageName.create("   ", Collections.singletonList("otherTag"));
    }

    @Test(expected = MojoExecutionException.class)
    public void testCreate_NullTagsAndNoImageTagAgain() throws Exception {
        CompositeImageName.create("anotherrepo", null);
    }

    @Test(expected = MojoExecutionException.class)
    public void testCreate_InvalidColonName() throws Exception {
        CompositeImageName.create(":/", Arrays.asList("pubTag"));
    }

    @Test
    public void testCreate_NameWithTagNoImageTags_Other() throws Exception {
        CompositeImageName cin = CompositeImageName.create("otherrepo:bar", null);
        assertEquals("otherrepo", cin.getName());
        assertEquals(Collections.singletonList("bar"), cin.getImageTags());
    }

    @Test
    public void testContainsTag_ColonSlashDifferentLogic() {
        // imageName with registry and tag
        assertTrue(CompositeImageName.containsTag("registry2/publicorigin:mytag"));
        // colon as port not tag
        assertFalse(CompositeImageName.containsTag("registry2:8080/publicorigin"));
        // only tag
        assertTrue(CompositeImageName.containsTag("custom:latest"));
        // only name
        assertFalse(CompositeImageName.containsTag("custom"));
    }

    @Test
    public void testCreate_AnotherTagWithSlashAndColon() throws Exception {
        CompositeImageName cin = CompositeImageName.create("myreg/pubimg:release", Arrays.asList("stable"));
        assertEquals("myreg/pubimg", cin.getName());
        assertEquals(Arrays.asList("release", "stable"), cin.getImageTags());
    }
}
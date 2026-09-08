package com.spotify.docker;

import org.apache.maven.plugin.MojoExecutionException;
import org.junit.Test;

import java.util.Arrays;
import java.util.Collections;

import static org.junit.Assert.*;

public class CompositeImageNameTest {

    @Test
    public void testCreate_NameWithTagAndImageTags() throws Exception {
        CompositeImageName cin = CompositeImageName.create("repo:tag1", Arrays.asList("tag2","tag3"));
        assertEquals("repo", cin.getName());
        assertEquals(Arrays.asList("tag1", "tag2", "tag3"), cin.getImageTags());
    }

    @Test
    public void testCreate_NameWithoutTagButWithImageTags() throws Exception {
        CompositeImageName cin = CompositeImageName.create("repo", Arrays.asList("tag2"));
        assertEquals("repo", cin.getName());
        assertEquals(Collections.singletonList("tag2"), cin.getImageTags());
    }

    @Test(expected = MojoExecutionException.class)
    public void testCreate_BlankName() throws Exception {
        CompositeImageName.create("", Collections.singletonList("atag"));
    }

    @Test(expected = MojoExecutionException.class)
    public void testCreate_NullTagsAndNoImageTag() throws Exception {
        CompositeImageName.create("repo", null);
    }

    @Test(expected = MojoExecutionException.class)
    public void testCreate_OnlyColon() throws Exception {
        CompositeImageName.create(":", Arrays.asList("someTag"));
    }

    @Test
    public void testCreate_NameWithTagNoImageTags() throws Exception {
        CompositeImageName cin = CompositeImageName.create("repo:foo", null);
        assertEquals("repo", cin.getName());
        assertEquals(Collections.singletonList("foo"), cin.getImageTags());
    }

    @Test
    public void testContainsTag_ColonSlashLogic() {
        // imageName with registry and tag
        assertTrue(CompositeImageName.containsTag("myregistry/origin:tag1"));
        // colon as port not tag
        assertFalse(CompositeImageName.containsTag("myregistry:5000/origin"));
        // only tag
        assertTrue(CompositeImageName.containsTag("image:tag"));
        // only name
        assertFalse(CompositeImageName.containsTag("image"));
    }

    @Test
    public void testCreate_TagWithSlashAndColon() throws Exception {
        CompositeImageName cin = CompositeImageName.create("reg/some:image", Arrays.asList("more"));
        assertEquals("reg/some", cin.getName());
        assertEquals(Arrays.asList("image", "more"), cin.getImageTags());
    }
}
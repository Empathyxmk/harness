package com.spotify.docker;

import org.junit.Test;
import java.io.File;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.Assert.*;

public class UtilsPublicTest {

    @Test
    public void testParseImageNameForAnotherFormat() {
        String input = "registry.example.com/newrepo/sample:mytag";
        String[] result = Utils.parseImageName(input);
        assertEquals("registry.example.com/newrepo/sample", result[0]);
        assertEquals("mytag", result[1]);
    }

    @Test
    public void testParseImageName_WhenNoTagProvided() {
        String input = "ubuntu";
        String[] result = Utils.parseImageName(input);
        assertArrayEquals(new String[]{"ubuntu", null}, result);
    }

    @Test
    public void testPushImageNoPush() throws Exception {
        // Just checks that pushImage can be called without exceptions when pushImage is false.
        File pom = new File("not/actually/used/public");
        Utils.pushImage(null, false, "image:tag", null, pom, null, null, null);
        // No assertion as public test - but just makes sure invocation does not throw
    }

    @Test
    public void testWriteImageInfoFile() throws Exception {
        // This will write to target/image_info.json
        Utils.writeImageInfoFile("image:pub", "imagetag", "target/image_pub_info.json");
        File f = new File("target/image_pub_info.json");
        assertThat(f.exists()).isTrue();
        f.delete();
    }
}
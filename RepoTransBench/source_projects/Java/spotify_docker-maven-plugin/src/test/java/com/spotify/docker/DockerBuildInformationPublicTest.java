package com.spotify.docker;

import org.junit.Test;

import java.util.Arrays;

import static org.junit.Assert.*;

public class DockerBuildInformationPublicTest {

    @Test
    public void testBuildInfoSetterGetterPublic() {
        DockerBuildInformation info = new DockerBuildInformation();
        info.setImageId("publicId2");
        info.setImageName("publicName2");
        info.setTags(Arrays.asList("publicTag1","publicTag2"));

        assertEquals("publicId2", info.getImageId());
        assertEquals("publicName2", info.getImageName());
        assertEquals(Arrays.asList("publicTag1","publicTag2"), info.getTags());
    }
}
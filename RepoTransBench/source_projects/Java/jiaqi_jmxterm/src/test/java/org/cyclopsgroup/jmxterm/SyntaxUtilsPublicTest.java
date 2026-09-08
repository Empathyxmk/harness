package org.cyclopsgroup.jmxterm;

import org.junit.Test;

import javax.management.ObjectName;
import javax.management.remote.JMXServiceURL;

import java.io.IOException;
import java.net.MalformedURLException;

import static org.junit.Assert.*;

public class SyntaxUtilsPublicTest {
    @Test
    public void testParseUrl_public() throws MalformedURLException {
        // Use a different valid URL string from the original test
        JMXServiceURL url = SyntaxUtils.parseUrl("service:jmx:rmi:///jndi/rmi://example.com:4044/jmxrmi");
        assertEquals("service:jmx:rmi:///jndi/rmi://example.com:4044/jmxrmi", url.toString());
    }

    @Test(expected = MalformedURLException.class)
    public void testParseUrl_invalid_public() throws MalformedURLException {
        SyntaxUtils.parseUrl("not_a_valid_url_at_all");
    }

    @Test
    public void testToObjectName_public() throws Exception {
        // Use a different object name than any seen in the original test
        ObjectName name = SyntaxUtils.toObjectName("mydomain:type=testBean,name=newValue");
        assertEquals("mydomain:type=testBean,name=newValue", name.toString());
    }

    @Test(expected = javax.management.MalformedObjectNameException.class)
    public void testToObjectName_invalid_public() throws Exception {
        SyntaxUtils.toObjectName("invalid_object_name!#");
    }
}
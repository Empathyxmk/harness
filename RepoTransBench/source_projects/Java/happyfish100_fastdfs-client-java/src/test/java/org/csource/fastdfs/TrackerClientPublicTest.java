package org.csource.fastdfs;

import org.csource.common.MyException;
import org.csource.fastdfs.pool.Connection;
import org.junit.Test;

import java.io.IOException;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class TrackerClientPublicTest {

    @Test
    public void testConstructorsAndGetErrorCodePublic() {
        TrackerGroup group = mock(TrackerGroup.class);
        TrackerClient client = new TrackerClient(group);

        assertSame(group, client.tracker_group);

        TrackerClient client2 = new TrackerClient();
        assertNotNull(client2.tracker_group);

        // set and get error code, using a nonzero public value
        client.errno = 10;
        assertEquals(10, client.getErrorCode());
    }

    @Test
    public void testGetTrackerServerPublic() throws IOException, MyException {
        TrackerGroup group = mock(TrackerGroup.class);
        TrackerServer server = mock(TrackerServer.class);
        when(group.getTrackerServer()).thenReturn(server);

        TrackerClient client = new TrackerClient(group);
        TrackerServer result = client.getTrackerServer();
        assertSame(server, result);
    }

    @Test
    public void testGetConnectionFailoverPublic() throws IOException, MyException {
        TrackerGroup group = mock(TrackerGroup.class);
        TrackerServer[] servers = new TrackerServer[2];
        servers[0] = mock(TrackerServer.class);
        servers[1] = mock(TrackerServer.class);
        Connection connection1 = mock(Connection.class);
        when(group.tracker_servers).thenReturn(servers);
        when(group.getTrackerServer()).thenReturn(servers[0]);
        when(servers[0].getConnection()).thenThrow(new IOException("fail1"));
        when(servers[0].getIndex()).thenReturn(0);
        when(group.getTrackerServer(1)).thenReturn(servers[1]);
        when(servers[1].getConnection()).thenReturn(connection1);

        TrackerClient client = new TrackerClient(group);
        Connection result = client.getConnection(null);
        assertSame(connection1, result);
    }
}
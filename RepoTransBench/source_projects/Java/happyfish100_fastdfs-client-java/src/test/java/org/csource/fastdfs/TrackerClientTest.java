package org.csource.fastdfs;

import org.csource.common.MyException;
import org.csource.fastdfs.pool.Connection;
import org.junit.Test;

import java.io.IOException;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class TrackerClientTest {

    @Test
    public void testConstructorsAndGetErrorCode() {
        TrackerGroup group = mock(TrackerGroup.class);
        TrackerClient client = new TrackerClient(group);

        assertSame(group, client.tracker_group);

        TrackerClient defaultClient = new TrackerClient();
        // just ensure no exception, cannot cover much without env
        defaultClient.getErrorCode();
    }

    @Test
    public void testGetTrackerServer() throws IOException {
        TrackerGroup group = mock(TrackerGroup.class);
        TrackerServer srv = mock(TrackerServer.class);
        when(group.getTrackerServer()).thenReturn(srv);
        TrackerClient client = new TrackerClient(group);

        assertSame(srv, client.getTrackerServer());
    }

    @Test
    public void testGetConnectionSuccess() throws Exception {
        TrackerGroup group = mock(TrackerGroup.class);
        TrackerServer server = mock(TrackerServer.class);
        Connection conn = mock(Connection.class);
        TrackerClient client = new TrackerClient(group);

        when(server.getConnection()).thenReturn(conn);
        when(group.tracker_servers).thenReturn(new TrackerServer[]{server});
        assertSame(conn, client.getConnection(server));
    }

    @Test
    public void testGetConnectionWithFailover() throws Exception {
        TrackerGroup group = mock(TrackerGroup.class);
        TrackerServer server1 = mock(TrackerServer.class);
        TrackerServer server2 = mock(TrackerServer.class);
        Connection conn2 = mock(Connection.class);

        TrackerClient client = new TrackerClient(group);

        when(group.tracker_servers).thenReturn(new TrackerServer[]{server1, server2});
        // first call throws, second returns conn2
        when(server1.getConnection()).thenThrow(new IOException("fail!"));
        when(server1.getIndex()).thenReturn(0);
        when(group.getTrackerServer()).thenReturn(server1);
        when(group.getTrackerServer(1)).thenReturn(server2);
        when(server2.getConnection()).thenReturn(conn2);

        Connection conn = client.getConnection(null);
        assertSame(conn2, conn);
    }
}
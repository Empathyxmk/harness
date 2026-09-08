package com.distributed.sequence.zk;

import com.distributed.sequence.DistributedSequence;
import org.apache.curator.framework.CuratorFramework;
import org.apache.curator.framework.setData.SetDataBuilder;
import org.junit.Before;
import org.junit.Test;

import static org.mockito.Mockito.*;
import static org.junit.Assert.*;

public class ZkDistributedSequenceUnitTest {

    private CuratorFramework clientMock;
    private ZkDistributedSequence zkSequence;

    @Before
    public void setUp() {
        clientMock = mock(CuratorFramework.class);
        zkSequence = new ZkDistributedSequence("localhost") {
            {
                this.client = clientMock;
            }
        };
    }

    @Test
    public void testGetSetMaxRetries() {
        assertEquals(3, zkSequence.getMaxRetries());
        zkSequence.setMaxRetries(9);
        assertEquals(9, zkSequence.getMaxRetries());
    }

    @Test
    public void testGetBaseSleepTimeMs() {
        assertEquals(1000, zkSequence.getBaseSleepTimeMs());
    }

    @Test
    public void testSequenceReturnsValue() throws Exception {
        SetDataBuilder setDataBuilder = mock(SetDataBuilder.class);
        SetDataBuilder setDataBuilderWithVersion = mock(SetDataBuilder.class);
        when(clientMock.setData()).thenReturn(setDataBuilder);
        when(setDataBuilder.withVersion(-1)).thenReturn(setDataBuilderWithVersion);
        when(setDataBuilderWithVersion.forPath(anyString(), any())).thenReturn(new org.apache.curator.framework.api.CuratorEvent() {
            public int getVersion() { return 123; }
        });

        // But real code expects forPath() returns a stat with getVersion()
        org.apache.zookeeper.data.Stat fakeStat = new org.apache.zookeeper.data.Stat();
        fakeStat.setVersion(17);
        when(setDataBuilderWithVersion.forPath(anyString(), any())).thenReturn(fakeStat);

        Long result = zkSequence.sequence("abc");
        assertNotNull(result);
        assertEquals(Long.valueOf(17), result);
    }

    @Test
    public void testSequenceHandlesException() throws Exception {
        SetDataBuilder setDataBuilder = mock(SetDataBuilder.class);
        SetDataBuilder setDataBuilderWithVersion = mock(SetDataBuilder.class);
        when(clientMock.setData()).thenReturn(setDataBuilder);
        when(setDataBuilder.withVersion(-1)).thenReturn(setDataBuilderWithVersion);
        when(setDataBuilderWithVersion.forPath(anyString(), any())).thenThrow(new RuntimeException("fail!"));

        Long result = zkSequence.sequence("failcase");
        assertNull(result);
    }
}
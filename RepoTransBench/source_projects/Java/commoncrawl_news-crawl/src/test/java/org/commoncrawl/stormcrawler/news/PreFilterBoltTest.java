package org.commoncrawl.stormcrawler.news;

import com.digitalpebble.stormcrawler.Metadata;
import com.digitalpebble.stormcrawler.persistence.Status;
import com.digitalpebble.stormcrawler.filtering.URLFilters;
import org.apache.storm.task.OutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.tuple.Tuple;
import org.apache.storm.tuple.Values;
import org.junit.Before;
import org.junit.Test;
import org.mockito.ArgumentCaptor;
import org.mockito.Mockito;

import java.io.IOException;
import java.util.Collections;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class PreFilterBoltTest {

    PreFilterBolt bolt;
    OutputCollector collector;

    @Before
    public void setup() {
        bolt = new PreFilterBolt(null) {
            {
                this.urlFilters = mock(URLFilters.class);
            }
        };
        collector = mock(OutputCollector.class);
        TopologyContext context = mock(TopologyContext.class);
        bolt.prepare(Collections.emptyMap(), context, collector);
    }

    private Tuple tupleWithUrlAndMetadata(String url, Metadata md) {
        Tuple tuple = mock(Tuple.class);
        when(tuple.getStringByField("url")).thenReturn(url);
        when(tuple.getValueByField("metadata")).thenReturn(md);
        return tuple;
    }

    @Test
    public void testUrlRejected() {
        when(bolt.urlFilters.filter(isNull(), isNull(), anyString())).thenReturn(null);
        Metadata md = new Metadata();
        Tuple input = tupleWithUrlAndMetadata("http://reject.me", md);
        bolt.execute(input);

        verify(collector).emit(eq(com.digitalpebble.stormcrawler.Constants.StatusStreamName), eq(input), any(Values.class));
        verify(collector).ack(input);
        assertEquals("Filtered", md.getValues("error.cause").get(0));
    }

    @Test
    public void testUrlAccepted() {
        when(bolt.urlFilters.filter(isNull(), isNull(), anyString())).thenReturn("http://accept.me");
        Metadata md = new Metadata();
        Tuple input = tupleWithUrlAndMetadata("http://accept.me", md);
        bolt.execute(input);

        verify(collector).emit(eq(input), any(Values.class));
        verify(collector, never()).emit(eq(com.digitalpebble.stormcrawler.Constants.StatusStreamName), any(), any());
        verify(collector).ack(input);
    }
}
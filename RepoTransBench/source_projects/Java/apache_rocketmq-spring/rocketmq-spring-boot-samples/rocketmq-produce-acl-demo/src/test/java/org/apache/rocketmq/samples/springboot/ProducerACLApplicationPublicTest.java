package org.apache.rocketmq.samples.springboot;

import org.apache.rocketmq.client.producer.SendResult;
import org.apache.rocketmq.spring.core.RocketMQTemplate;
import org.apache.rocketmq.spring.support.RocketMQHeaders;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.messaging.Message;
import org.springframework.messaging.support.MessageBuilder;
import org.springframework.test.util.ReflectionTestUtils;

import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

public class ProducerACLApplicationPublicTest {

    private RocketMQTemplate rocketMQTemplate;
    private ProducerACLApplication producerACLApplication;

    @BeforeEach
    public void setup() {
        rocketMQTemplate = mock(RocketMQTemplate.class);
        producerACLApplication = new ProducerACLApplication();
        ReflectionTestUtils.setField(producerACLApplication, "rocketMQTemplate", rocketMQTemplate);
        // Use different topic names for public test
        ReflectionTestUtils.setField(producerACLApplication, "springTransTopic", "publicTransTopic");
        ReflectionTestUtils.setField(producerACLApplication, "springTopic", "publicTopic");

        SendResult mockResult = mock(SendResult.class);
        when(rocketMQTemplate.syncSend(anyString(), any())).thenReturn(mockResult);
        when(rocketMQTemplate.syncSend(anyString(), any(Message.class))).thenReturn(mockResult);
        when(rocketMQTemplate.sendMessageInTransaction(anyString(), any(Message.class), any())).thenReturn(mockResult);
    }

    @Test
    public void testRun() throws Exception {
        // The method will attempt to call syncSend and sendMessageInTransaction with new topics and tags
        producerACLApplication.run();
        verify(rocketMQTemplate, atLeastOnce()).syncSend(anyString(), any());
        verify(rocketMQTemplate, atLeastOnce()).syncSend(anyString(), any(Message.class));
        verify(rocketMQTemplate, atLeastOnce()).sendMessageInTransaction(anyString(), any(Message.class), any());
    }

    @Test
    public void testTransactionListenerImpl_executeLocalTransaction_commit() {
        ProducerACLApplication.TransactionListenerImpl listener = producerACLApplication.new TransactionListenerImpl();
        // Use different payload and transaction id for public
        Message msg = MessageBuilder.withPayload("publicTxMsg")
                .setHeader(RocketMQHeaders.TRANSACTION_ID, "public_tx_1").build();
        listener.transactionIndex = new AtomicInteger(0);
        assertEquals(org.apache.rocketmq.spring.core.RocketMQLocalTransactionState.COMMIT,
                     listener.executeLocalTransaction(msg, null));
        assertEquals(org.apache.rocketmq.spring.core.RocketMQLocalTransactionState.ROLLBACK,
                     listener.executeLocalTransaction(msg, null));
        assertEquals(org.apache.rocketmq.spring.core.RocketMQLocalTransactionState.UNKNOWN,
                     listener.executeLocalTransaction(msg, null));
    }

    @Test
    public void testTransactionListenerImpl_checkLocalTransaction_allcases() {
        ProducerACLApplication.TransactionListenerImpl listener = producerACLApplication.new TransactionListenerImpl();
        String transId = "public_txId";
        ReflectionTestUtils.setField(listener, "localTrans", new ConcurrentHashMap<String, Integer>());
        listener.localTrans.put(transId, 0);
        Message msg = MessageBuilder.withPayload("anotherTxMsg")
                .setHeader(RocketMQHeaders.TRANSACTION_ID, transId).build();
        // state 0 = commit
        assertEquals(org.apache.rocketmq.spring.core.RocketMQLocalTransactionState.COMMIT,
                listener.checkLocalTransaction(msg));
        // state 1 = rollback
        listener.localTrans.put(transId, 1);
        assertEquals(org.apache.rocketmq.spring.core.RocketMQLocalTransactionState.ROLLBACK,
                listener.checkLocalTransaction(msg));
        // state else = unknown
        listener.localTrans.put(transId, 2);
        assertEquals(org.apache.rocketmq.spring.core.RocketMQLocalTransactionState.UNKNOWN,
                listener.checkLocalTransaction(msg));
        // not found
        listener.localTrans.remove(transId);
        assertEquals(org.apache.rocketmq.spring.core.RocketMQLocalTransactionState.UNKNOWN,
                listener.checkLocalTransaction(msg));
    }

    @Test
    public void testMain() {
        String[] args = new String[] { "public" };
        ProducerACLApplication.main(args);
    }
}
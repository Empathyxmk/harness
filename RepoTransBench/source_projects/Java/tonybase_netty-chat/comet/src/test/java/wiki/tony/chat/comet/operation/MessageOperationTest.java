package wiki.tony.chat.comet.operation;

import io.netty.channel.Channel;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
import wiki.tony.chat.base.bean.Constants;
import wiki.tony.chat.base.bean.Proto;
import wiki.tony.chat.base.service.MsgService;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class MessageOperationTest {

    private MessageOperation messageOperation;
    private MsgService msgService;
    private Channel channel;

    @BeforeEach
    void setUp() {
        messageOperation = new MessageOperation();
        msgService = mock(MsgService.class);
        channel = mock(Channel.class);

        // inject msgService via reflection (field is private)
        try {
            var f = MessageOperation.class.getDeclaredField("msgService");
            f.setAccessible(true);
            f.set(messageOperation, msgService);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    @Test
    void testOp() {
        assertEquals(Constants.OP_MESSAGE, messageOperation.op());
    }

    @Test
    void testAction_WritesReply() throws Exception {
        Proto proto = mock(Proto.class);
        // Make checkAuth do nothing (no throw)
        MessageOperation spy = spy(messageOperation);
        doNothing().when(spy).checkAuth(any());

        spy.action(channel, proto);

        verify(msgService, times(1)).receive(proto);
        verify(proto).setOperation(Constants.OP_MESSAGE_REPLY);
        verify(proto).setBody(null);
        verify(channel).writeAndFlush(proto);
    }
}
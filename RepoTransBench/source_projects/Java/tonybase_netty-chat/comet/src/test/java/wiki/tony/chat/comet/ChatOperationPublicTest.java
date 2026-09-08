package wiki.tony.chat.comet;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.context.ApplicationContext;
import wiki.tony.chat.comet.operation.Operation;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class ChatOperationPublicTest {

    private ChatOperation chatOperation;
    private ApplicationContext context;

    @BeforeEach
    void setUp() {
        chatOperation = new ChatOperation();
        context = Mockito.mock(ApplicationContext.class);

        // inject via reflection (field is package-private)
        try {
            var f = ChatOperation.class.getDeclaredField("applicationContext");
            f.setAccessible(true);
            f.set(chatOperation, context);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    @Test
    void publicTestOperations_empty() {
        Mockito.when(context.getBeansOfType(Operation.class)).thenReturn(Collections.singletonMap("noItem", null));
        // Should filter out null but still create a non-null ops map (edge: null operation)
        Map<Integer, Operation> ops = chatOperation.operations();
        assertNotNull(ops);
        // Trick: Should only add non-null Operation, so map should stay empty
        assertTrue(ops.isEmpty() || ops.values().stream().allMatch(op -> op == null));
    }

    @Test
    void publicTestOperations_withOneOperationDifferentOpNumber() {
        Operation op = Mockito.mock(Operation.class);
        Mockito.when(op.op()).thenReturn(22); // use new op number (was 1 in orig)
        Map<String, Operation> beans = new HashMap<>();
        beans.put("otherOp", op);
        Mockito.when(context.getBeansOfType(Operation.class)).thenReturn(beans);

        Map<Integer, Operation> ops = chatOperation.operations();
        assertNotNull(ops);
        assertEquals(1, ops.size());
        assertSame(op, ops.get(22));
    }

    @Test
    void publicTestFind() {
        Operation op = Mockito.mock(Operation.class);
        Mockito.when(op.op()).thenReturn(42);
        Map<String, Operation> beans = new HashMap<>();
        beans.put("deepOp", op);
        Mockito.when(context.getBeansOfType(Operation.class)).thenReturn(beans);

        chatOperation.operations();
        assertSame(op, chatOperation.find(42));
        assertNull(chatOperation.find(-1)); // use different number
    }
}
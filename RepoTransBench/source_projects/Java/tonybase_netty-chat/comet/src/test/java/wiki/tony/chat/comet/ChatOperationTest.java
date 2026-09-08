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

class ChatOperationTest {

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
    void testOperations_empty() {
        Mockito.when(context.getBeansOfType(Operation.class)).thenReturn(Collections.emptyMap());
        Map<Integer, Operation> ops = chatOperation.operations();
        assertNotNull(ops);
        assertTrue(ops.isEmpty());
    }

    @Test
    void testOperations_withOneOperation() {
        Operation op = Mockito.mock(Operation.class);
        Mockito.when(op.op()).thenReturn(1);
        Map<String, Operation> beans = new HashMap<>();
        beans.put("myOp", op);
        Mockito.when(context.getBeansOfType(Operation.class)).thenReturn(beans);

        Map<Integer, Operation> ops = chatOperation.operations();
        assertNotNull(ops);
        assertEquals(1, ops.size());
        assertSame(op, ops.get(1));
    }

    @Test
    void testFind() {
        Operation op = Mockito.mock(Operation.class);
        Mockito.when(op.op()).thenReturn(5);
        Map<String, Operation> beans = new HashMap<>();
        beans.put("myOp", op);
        Mockito.when(context.getBeansOfType(Operation.class)).thenReturn(beans);

        chatOperation.operations();
        assertSame(op, chatOperation.find(5));
        assertNull(chatOperation.find(99));
    }
}
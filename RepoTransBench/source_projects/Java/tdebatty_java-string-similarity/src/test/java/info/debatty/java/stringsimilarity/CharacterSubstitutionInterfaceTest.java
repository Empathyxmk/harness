package info.debatty.java.stringsimilarity;

import org.junit.Test;
import static org.junit.Assert.*;

public class CharacterSubstitutionInterfaceTest {
    @Test
    public void testExampleImplementation() {
        CharacterSubstitutionInterface csi = new CharacterSubstitutionInterface() {
            @Override
            public double cost(char c1, char c2) {
                if (c1 == c2) return 0.0;
                if ((c1 == 'a' && c2 == 'b') || (c1 == 'b' && c2 == 'a')) return 0.5;
                return 1.0;
            }
        };

        assertEquals(0.0, csi.cost('a', 'a'), 1e-9);
        assertEquals(0.5, csi.cost('a', 'b'), 1e-9);
        assertEquals(0.5, csi.cost('b', 'a'), 1e-9);
        assertEquals(1.0, csi.cost('a', 'z'), 1e-9);
    }
}
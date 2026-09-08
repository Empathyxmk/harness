import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// MATCHES FUNCTIONALITY of src/DifferenceBetweenDaysInYearTest.java, but with different test data.
class DifferenceBetweenDaysInYearPublicTest {

    @Test
    public void publicTest1_predicate1() {
        int output = DifferenceBetweenDaysInYear.cal(5, 2, 4, 2, 2024);
        assertEquals(28, output);
    }
    @Test
    public void publicTest2_predicate1() {
        int output = DifferenceBetweenDaysInYear.cal(12, 11, 5, 23, 2018);
        assertEquals(171, output);
    }
    @Test
    public void publicTest3_predicate2() {
        int output = DifferenceBetweenDaysInYear.cal(10, 1, 12, 22, 1998);
        assertEquals(21, output);
    }
    @Test
    public void publicTest4_predicate2() {
        int output = DifferenceBetweenDaysInYear.cal(3, 7, 9, 15, 105);
        assertEquals(8, output);
    }
    @Test
    public void publicTest5_predicate2() {
        int output = DifferenceBetweenDaysInYear.cal(11, 5, 12, 1, 1300);
        assertEquals(170, output);
    }
}
package guru.springframework.spring5webapp;

public class SampleBranchingService {
    public String categorizeNumber(int n) {
        if (n < 0) {
            return "negative";
        } else if (n == 0) {
            return "zero";
        } else if (n > 0 && n <= 10) {
            return "small";
        } else {
            return "large";
        }
    }

    public boolean isEven(int n) {
        return n % 2 == 0;
    }
}
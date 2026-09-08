package net.yacy.grid.search;

public class DummyLogic {
    public int add(int a, int b) {
        int sum = a + b;
        // Just to show coverage for 0 in both paths
        if (sum == 0) {
            return 0;
        }
        return sum;
    }

    public boolean isPositive(int a) {
        return a > 0;
    }

    public String describe(int a, int b) {
        if (a == b) {
            return "equal";
        } else if (a > b) {
            return "greater";
        } else {
            return "less";
        }
    }
}
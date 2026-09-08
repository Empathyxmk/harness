// Add a package for proper usage and import compatibility
package gabrieldim_JUnitCACC;

public class DifferenceBetweenDaysInYear {
    // Keep the original method as static for test invocation compatibility
    public static int differenceBetweenDaysInYear(int year1, int month1, int day1,
                                                  int year2, int month2, int day2) {
        if (!isValidDate(year1, month1, day1) || !isValidDate(year2, month2, day2)) {
            throw new IllegalArgumentException("Invalid date input");
        }
        if (year1 != year2) {
            throw new IllegalArgumentException("Years must be the same");
        }
        int days1 = daysSinceStartOfYear(year1, month1, day1);
        int days2 = daysSinceStartOfYear(year2, month2, day2);
        return days2 - days1;
    }

    private static boolean isValidDate(int year, int month, int day) {
        if (month < 1 || month > 12) return false;
        int[] daysInMonth = {31, isLeapYear(year) ? 29 : 28, 31, 30, 31, 30,
                             31, 31, 30, 31, 30, 31};
        return day >= 1 && day <= daysInMonth[month - 1];
    }

    private static boolean isLeapYear(int year) {
        return (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);
    }

    private static int daysSinceStartOfYear(int year, int month, int day) {
        int[] daysInMonth = {31, isLeapYear(year) ? 29 : 28, 31, 30, 31, 30,
                             31, 31, 30, 31, 30, 31};
        int days = 0;
        for (int i = 0; i < month - 1; i++) {
            days += daysInMonth[i];
        }
        days += day - 1;
        return days;
    }
}
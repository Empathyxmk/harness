package company;

// Use commons-lang3 StringUtils (org.apache.commons.lang3)
import org.apache.commons.lang3.StringUtils;

public class Main {
    public static void main(String[] args) {
        String input = args.length > 0 ? args[0] : "";
        System.out.println("Reversed: " + reverseIfNotBlank(input));
        System.out.println("Is all digits: " + isAllDigits(input));
        System.out.println("Random string: " + RandomUtil.randomString(8));
    }

    public static String reverseIfNotBlank(String input) {
        if (StringUtils.isBlank(input)) {
            return input;
        }
        return StringUtils.reverse(input);
    }

    public static boolean isAllDigits(String input) {
        if (StringUtils.isBlank(input)) {
            return false;
        }
        return StringUtils.isNumeric(input);
    }
}
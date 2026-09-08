package com.example.colorama.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Translation of colorama/tests/ansi_test.py (core Fore/Back/Style attribute tests)
 */
public class AnsiTest {

    static class Fore {
        static final String BLACK = "\033[30m";
        static final String RED = "\033[31m";
        static final String GREEN = "\033[32m";
        static final String YELLOW = "\033[33m";
        static final String BLUE = "\033[34m";
        static final String MAGENTA = "\033[35m";
        static final String CYAN = "\033[36m";
        static final String WHITE = "\033[37m";
        static final String RESET = "\033[39m";
        static final String LIGHTBLACK_EX = "\033[90m";
        static final String LIGHTRED_EX = "\033[91m";
        static final String LIGHTGREEN_EX = "\033[92m";
        static final String LIGHTYELLOW_EX = "\033[93m";
        static final String LIGHTBLUE_EX = "\033[94m";
        static final String LIGHTMAGENTA_EX = "\033[95m";
        static final String LIGHTCYAN_EX = "\033[96m";
        static final String LIGHTWHITE_EX = "\033[97m";
    }

    static class Back {
        static final String BLACK = "\033[40m";
        static final String RED = "\033[41m";
        static final String GREEN = "\033[42m";
        static final String YELLOW = "\033[43m";
        static final String BLUE = "\033[44m";
        static final String MAGENTA = "\033[45m";
        static final String CYAN = "\033[46m";
        static final String WHITE = "\033[47m";
        static final String RESET = "\033[49m";
        static final String LIGHTBLACK_EX = "\033[100m";
        static final String LIGHTRED_EX = "\033[101m";
        static final String LIGHTGREEN_EX = "\033[102m";
        static final String LIGHTYELLOW_EX = "\033[103m";
        static final String LIGHTBLUE_EX = "\033[104m";
        static final String LIGHTMAGENTA_EX = "\033[105m";
        static final String LIGHTCYAN_EX = "\033[106m";
        static final String LIGHTWHITE_EX = "\033[107m";
    }

    static class Style {
        static final String DIM = "\033[2m";
        static final String NORMAL = "\033[22m";
        static final String BRIGHT = "\033[1m";
    }

    @Test
    public void testForeAttributes() {
        assertEquals("\033[30m", Fore.BLACK);
        assertEquals("\033[31m", Fore.RED);
        assertEquals("\033[32m", Fore.GREEN);
        assertEquals("\033[33m", Fore.YELLOW);
        assertEquals("\033[34m", Fore.BLUE);
        assertEquals("\033[35m", Fore.MAGENTA);
        assertEquals("\033[36m", Fore.CYAN);
        assertEquals("\033[37m", Fore.WHITE);
        assertEquals("\033[39m", Fore.RESET);

        assertEquals("\033[90m", Fore.LIGHTBLACK_EX);
        assertEquals("\033[91m", Fore.LIGHTRED_EX);
        assertEquals("\033[92m", Fore.LIGHTGREEN_EX);
        assertEquals("\033[93m", Fore.LIGHTYELLOW_EX);
        assertEquals("\033[94m", Fore.LIGHTBLUE_EX);
        assertEquals("\033[95m", Fore.LIGHTMAGENTA_EX);
        assertEquals("\033[96m", Fore.LIGHTCYAN_EX);
        assertEquals("\033[97m", Fore.LIGHTWHITE_EX);
    }

    @Test
    public void testBackAttributes() {
        assertEquals("\033[40m", Back.BLACK);
        assertEquals("\033[41m", Back.RED);
        assertEquals("\033[42m", Back.GREEN);
        assertEquals("\033[43m", Back.YELLOW);
        assertEquals("\033[44m", Back.BLUE);
        assertEquals("\033[45m", Back.MAGENTA);
        assertEquals("\033[46m", Back.CYAN);
        assertEquals("\033[47m", Back.WHITE);
        assertEquals("\033[49m", Back.RESET);

        assertEquals("\033[100m", Back.LIGHTBLACK_EX);
        assertEquals("\033[101m", Back.LIGHTRED_EX);
        assertEquals("\033[102m", Back.LIGHTGREEN_EX);
        assertEquals("\033[103m", Back.LIGHTYELLOW_EX);
        assertEquals("\033[104m", Back.LIGHTBLUE_EX);
        assertEquals("\033[105m", Back.LIGHTMAGENTA_EX);
        assertEquals("\033[106m", Back.LIGHTCYAN_EX);
        assertEquals("\033[107m", Back.LIGHTWHITE_EX);
    }

    @Test
    public void testStyleAttributes() {
        assertEquals("\033[2m", Style.DIM);
        assertEquals("\033[22m", Style.NORMAL);
        assertEquals("\033[1m", Style.BRIGHT);
    }
}
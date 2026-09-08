//! This file simulates loading the run-tests.php test harness as a test

#[cfg(test)]
mod tests {
    #[test]
    fn test_run_tests_harness_documentation_header() {
        // The file starts with a documentation header.
        let header = r#"
        +----------------------------------------------------------------------+
        | Copyright (c) The PHP Group                                          |
        +----------------------------------------------------------------------+
        | This source file is subject to version 3.01 of the PHP license,      |
        | that is bundled with this package in the file LICENSE, and is        |
        | available through the world-wide-web at the following url:           |
        | https://php.net/license/3_01.txt                                     |
        | If you did not receive a copy of the PHP license and are unable to   |
        | obtain it through the world-wide-web, please send a note to          |
        | license@php.net so we can mail you a copy immediately.               |
        +----------------------------------------------------------------------+
        "#;
        assert!(header.contains("PHP Group"));
        assert!(header.contains("php.net/license/3_01.txt"));
    }

    #[test]
    fn test_expected_command_line_options() {
        // The file documents command line options; let's check a sample list exists
        let opts = [
            "-j<workers>",
            "-l <file>",
            "-r <file>",
            "-w <file>",
            "-c <file>",
            "--set-timeout [n]",
            "--show-[all|php|skip|clean|exp|diff|out|mem]",
            "--help",
        ];
        // Emulate documentation text (would extract from the usage/help section)
        let doc = r#"
            php run-tests.php [options] [files] [directories]

            Options:
                -j<workers> Run up to <workers> simultaneous testing processes ...
                -l <file>   Read the testfiles to be executed from <file> ...
                -r <file>   Read the testfiles to be executed from <file> ...
                -w <file>   Write a list of all failed tests to <file>.
                -c <file>   Look for php.ini in directory <file> or use <file> as ini.
                --set-timeout [n]  Set timeout for individual tests, where [n] is ...
                --show-[all|php|skip|clean|exp|diff|out|mem]
                --help
        "#;
        for o in opts {
            assert!(doc.contains(o));
        }
    }
}
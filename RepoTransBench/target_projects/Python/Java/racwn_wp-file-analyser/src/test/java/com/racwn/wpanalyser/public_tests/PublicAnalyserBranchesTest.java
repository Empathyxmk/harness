package com.racwn.wpanalyser.public_tests;

import com.racwn.wpanalyser.analyser.Analyser;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class PublicAnalyserBranchesTest {

    @Test
    void testDifferentBranchCount() {
        String fileContent = "<?php\nif(1){echo 'a';}else{echo 'b';}\nif(2){echo 'c';}\n";
        int result = Analyser.countBranches(fileContent);
        assertEquals(2, result);
    }

    @Test
    void testSwitchCaseBranch() {
        String fileContent = "<?php\nswitch($var){case 2: break; case 3: break; default: break;}\n";
        int result = Analyser.countBranches(fileContent);
        assertEquals(1, result);
    }

    @Test
    void testMultipleElseIfBranch() {
        String fileContent = "<?php\nif($a==2){echo 2;}elseif($a==3){echo 3;}elseif($a==4){echo 4;}\n";
        int result = Analyser.countBranches(fileContent);
        assertEquals(1, result);
    }

    @Test
    void testNestedIfElseBranch() {
        String fileContent = "<?php\nif($a){if($b){echo 1;}else{echo 2;}}\n";
        int result = Analyser.countBranches(fileContent);
        assertEquals(2, result);
    }

    @Test
    void testTryCatchCount() {
        String fileContent = "<?php\ntry{ risky(); } catch(Exception $e) {} catch(Error $e) {}\n";
        int result = Analyser.countBranches(fileContent);
        assertEquals(1, result);
    }
}
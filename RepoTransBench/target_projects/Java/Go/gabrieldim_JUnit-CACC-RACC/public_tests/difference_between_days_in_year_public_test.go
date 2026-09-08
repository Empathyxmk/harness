package public_tests

import (
	"testing"
	"difference"
	"strings"
)

func TestPublicTest1_Predicate1(t *testing.T) {
	out, err := difference.Cal(5, 2, 4, 2, 2024)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != 28 {
		t.Errorf("Expected 28, got %d", out)
	}
}

func TestPublicTest2_Predicate1(t *testing.T) {
	out, err := difference.Cal(12, 11, 5, 23, 2018)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != 171 {
		t.Errorf("Expected 171, got %d", out)
	}
}

func TestPublicTest3_Predicate2(t *testing.T) {
	out, err := difference.Cal(10, 1, 12, 22, 1998)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != 21 {
		t.Errorf("Expected 21, got %d", out)
	}
}

func TestPublicTest4_Predicate2(t *testing.T) {
	out, err := difference.Cal(3, 7, 9, 15, 105)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != 8 {
		t.Errorf("Expected 8, got %d", out)
	}
}

func TestPublicTest5_Predicate2(t *testing.T) {
	out, err := difference.Cal(11, 5, 12, 1, 1300)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != 170 {
		t.Errorf("Expected 170, got %d", out)
	}
}

func TestPublicTestSameDay(t *testing.T) {
	out, err := difference.DifferenceBetweenDaysInYear(2022,5,20,2022,5,20)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != 0 {
		t.Errorf("Expected 0 for same day, got %d", out)
	}
}

func TestPublicTestNonLeapYearNormalDates(t *testing.T) {
	out, err := difference.DifferenceBetweenDaysInYear(2022,3,15,2022,11,27)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != 257 {
		t.Errorf("Expected 257, got %d", out)
	}
	out2, err := difference.DifferenceBetweenDaysInYear(2022,11,27,2022,3,15)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out2 != -257 {
		t.Errorf("Expected -257, got %d", out2)
	}
}

func TestPublicTestLeapYearFebDates(t *testing.T) {
	out, err := difference.DifferenceBetweenDaysInYear(2016,2,27,2016,2,28)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != 1 {
		t.Errorf("Expected 1, got %d", out)
	}
	out2, err := difference.DifferenceBetweenDaysInYear(2016,3,1,2016,2,28)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out2 != -2 {
		t.Errorf("Expected -2, got %d", out2)
	}
}

func TestPublicTestInvalidMonth(t *testing.T) {
	_, err := difference.DifferenceBetweenDaysInYear(2022,0,4,2022,6,9)
	if err == nil {
		t.Errorf("Expected error for invalid month 0")
	} else if !strings.Contains(err.Error(), "Invalid") {
		t.Errorf("Expected error containing 'Invalid', got %v", err)
	}
	_, err2 := difference.DifferenceBetweenDaysInYear(2022,3,14,2022,15,7)
	if err2 == nil {
		t.Errorf("Expected error for invalid month 15")
	} else if !strings.Contains(err2.Error(), "Invalid") {
		t.Errorf("Expected error containing 'Invalid', got %v", err2)
	}
}

func TestPublicTestInvalidDay(t *testing.T) {
	_, err := difference.DifferenceBetweenDaysInYear(2023,2,30,2023,2,1)
	if err == nil {
		t.Errorf("Expected error for Feb 30 non-leap year")
	} else if !strings.Contains(err.Error(), "Invalid") {
		t.Errorf("Expected error containing 'Invalid', got %v", err)
	}
	_, err2 := difference.DifferenceBetweenDaysInYear(1999,6,31,1999,3,1)
	if err2 == nil {
		t.Errorf("Expected error for Jun 31")
	} else if !strings.Contains(err2.Error(), "Invalid") {
		t.Errorf("Expected error containing 'Invalid', got %v", err2)
	}
}

func TestPublicTestDifferentYears(t *testing.T) {
	_, err := difference.DifferenceBetweenDaysInYear(2021,4,10,2020,5,10)
	if err == nil {
		t.Errorf("Expected error for different years")
	} else if !strings.Contains(err.Error(), "Years must be the same") {
		t.Errorf("Expected error about years, got %v", err)
	}
}

func TestPublicTestLeapYearRecognition(t *testing.T) {
	out, err := difference.DifferenceBetweenDaysInYear(2012,1,1,2012,3,1)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != 60 {
		t.Errorf("Expected 60, got %d", out)
	}
	out, err = difference.DifferenceBetweenDaysInYear(2104,1,1,2104,3,1)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != 59 {
		t.Errorf("Expected 59, got %d", out)
	}
	out, err = difference.DifferenceBetweenDaysInYear(1800,1,1,1800,3,1)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != 59 {
		t.Errorf("Expected 59, got %d", out)
	}
	out, err = difference.DifferenceBetweenDaysInYear(2400,1,1,2400,3,1)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != 60 {
		t.Errorf("Expected 60, got %d", out)
	}
}

func TestPublicTestFirstAndLastDaysOfMonth(t *testing.T) {
	out, err := difference.DifferenceBetweenDaysInYear(2022,4,1,2022,4,28)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != 27 {
		t.Errorf("Expected 27, got %d", out)
	}
	out, err = difference.DifferenceBetweenDaysInYear(2022,4,28,2022,4,1)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != -27 {
		t.Errorf("Expected -27, got %d", out)
	}
}

func TestPublicTestMinimumValidDayAndMonth(t *testing.T) {
	out, err := difference.DifferenceBetweenDaysInYear(2023,2,1,2023,2,2)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != 1 {
		t.Errorf("Expected 1, got %d", out)
	}
	out, err = difference.DifferenceBetweenDaysInYear(2023,2,2,2023,2,1)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != -1 {
		t.Errorf("Expected -1, got %d", out)
	}
}

func TestPublicTestMaximumValidDayAndMonth(t *testing.T) {
	out, err := difference.DifferenceBetweenDaysInYear(2023,11,29,2023,11,30)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != 1 {
		t.Errorf("Expected 1, got %d", out)
	}
}

func TestPublicTestIsValidDatePrivateMethodViaInvalidInput(t *testing.T) {
	_, err := difference.DifferenceBetweenDaysInYear(2023,2,29,2023,2,28)
	if err == nil {
		t.Errorf("Expected error for Feb 29 on non-leap year (2023)")
	} else if !strings.Contains(err.Error(), "Invalid") {
		t.Errorf("Expected error including 'Invalid', got %v", err)
	}
	_, err2 := difference.DifferenceBetweenDaysInYear(2024,2,30,2024,2,28)
	if err2 == nil {
		t.Errorf("Expected error for Feb 30 on leap year (2024)")
	} else if !strings.Contains(err2.Error(), "Invalid") {
		t.Errorf("Expected error including 'Invalid', got %v", err2)
	}
}
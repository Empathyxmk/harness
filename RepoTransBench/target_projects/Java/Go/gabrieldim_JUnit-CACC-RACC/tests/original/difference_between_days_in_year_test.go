package original

import (
	"testing"
	"difference"
	"strings"
)

func Test1_Predicate1(t *testing.T) {
	out, err := difference.Cal(7, 1, 6, 1, 2021)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != 31 {
		t.Errorf("Expected 31, got %d", out)
	}
}

func Test2_Predicate1(t *testing.T) {
	out, err := difference.Cal(1, 3, 4, 15, 2019)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != 102 {
		t.Errorf("Expected 102, got %d", out)
	}
}

func Test3_Predicate2(t *testing.T) {
	out, err := difference.Cal(2, 5, 4, 27, 2000)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != 82 {
		t.Errorf("Expected 82, got %d", out)
	}
}

func Test4_Predicate2(t *testing.T) {
	out, err := difference.Cal(5, 6, 4, 28, 65)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != 53 {
		t.Errorf("Expected 53, got %d", out)
	}
}

func Test5_Predicate2(t *testing.T) {
	out, err := difference.Cal(9, 9, 4, 11, 1200)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != 32 {
		t.Errorf("Expected 32, got %d", out)
	}
}

// Additional tests matching src/test/java/DifferenceBetweenDaysInYearTest.java:

func TestSameDay(t *testing.T) {
	out, err := difference.DifferenceBetweenDaysInYear(2023,1,1,2023,1,1)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != 0 {
		t.Errorf("Expected 0 for same day, got %d", out)
	}
}

func TestNonLeapYearNormalDates(t *testing.T) {
	out, err := difference.DifferenceBetweenDaysInYear(2023,1,1,2023,12,31)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != 364 {
		t.Errorf("Expected 364, got %d", out)
	}
	out2, err := difference.DifferenceBetweenDaysInYear(2023,12,31,2023,1,1)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out2 != -364 {
		t.Errorf("Expected -364, got %d", out2)
	}
}

func TestLeapYearFebDates(t *testing.T) {
	out, err := difference.DifferenceBetweenDaysInYear(2020,2,28,2020,2,29)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != 1 {
		t.Errorf("Expected 1, got %d", out)
	}
	out2, err := difference.DifferenceBetweenDaysInYear(2020,3,1,2020,2,29)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out2 != -1 {
		t.Errorf("Expected -1, got %d", out2)
	}
}

func TestInvalidMonth(t *testing.T) {
	_, err := difference.DifferenceBetweenDaysInYear(2023,0,10,2023,1,1)
	if err == nil {
		t.Errorf("Expected error for invalid month 0")
	} else if !strings.Contains(err.Error(), "Invalid") {
		t.Errorf("Expected error about Invalid, got %v", err)
	}
	_, err2 := difference.DifferenceBetweenDaysInYear(2023,1,1,2023,13,1)
	if err2 == nil {
		t.Errorf("Expected error for invalid month 13")
	} else if !strings.Contains(err2.Error(), "Invalid") {
		t.Errorf("Expected error about Invalid, got %v", err2)
	}
}

func TestInvalidDay(t *testing.T) {
	_, err := difference.DifferenceBetweenDaysInYear(2021,2,30,2021,2,1)
	if err == nil {
		t.Errorf("Expected error for invalid day (Feb 30, non-leap year)")
	} else if !strings.Contains(err.Error(), "Invalid") {
		t.Errorf("Expected error about Invalid, got %v", err)
	}
	_, err2 := difference.DifferenceBetweenDaysInYear(2022,4,31,2022,2,1)
	if err2 == nil {
		t.Errorf("Expected error for invalid day (Apr 31)")
	} else if !strings.Contains(err2.Error(), "Invalid") {
		t.Errorf("Expected error about Invalid, got %v", err2)
	}
}

func TestDifferentYears(t *testing.T) {
	_, err := difference.DifferenceBetweenDaysInYear(2022,1,1,2021,1,1)
	if err == nil {
		t.Errorf("Expected error for differing years")
	} else if !strings.Contains(err.Error(), "Years must be the same") {
		t.Errorf("Expected error about years, got %v", err)
	}
}

func TestLeapYearRecognition(t *testing.T) {
	out, err := difference.DifferenceBetweenDaysInYear(2000,1,1,2000,3,1)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != 60 {
		t.Errorf("Expected 60, got %d", out)
	}
	out, err = difference.DifferenceBetweenDaysInYear(2016,1,1,2016,3,1)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != 60 {
		t.Errorf("Expected 60, got %d", out)
	}
	out, err = difference.DifferenceBetweenDaysInYear(2100,1,1,2100,3,1)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != 59 {
		t.Errorf("Expected 59, got %d", out)
	}
	out, err = difference.DifferenceBetweenDaysInYear(1900,1,1,1900,3,1)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != 59 {
		t.Errorf("Expected 59, got %d", out)
	}
}

func TestFirstAndLastDaysOfMonth(t *testing.T) {
	out, err := difference.DifferenceBetweenDaysInYear(2024,1,1,2024,1,31)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != 30 {
		t.Errorf("Expected 30, got %d", out)
	}
	out, err = difference.DifferenceBetweenDaysInYear(2024,1,31,2024,1,1)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != -30 {
		t.Errorf("Expected -30, got %d", out)
	}
}

func TestMinimumValidDayAndMonth(t *testing.T) {
	out, err := difference.DifferenceBetweenDaysInYear(2024,1,1,2024,1,2)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != 1 {
		t.Errorf("Expected 1, got %d", out)
	}
	out, err = difference.DifferenceBetweenDaysInYear(2024,1,2,2024,1,1)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != -1 {
		t.Errorf("Expected -1, got %d", out)
	}
}

func TestMaximumValidDayAndMonth(t *testing.T) {
	out, err := difference.DifferenceBetweenDaysInYear(2024,12,30,2024,12,31)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if out != 1 {
		t.Errorf("Expected 1, got %d", out)
	}
}

func TestIsValidDatePrivateMethodViaInvalidInput(t *testing.T) {
	_, err := difference.DifferenceBetweenDaysInYear(2021,2,29,2021,2,28)
	if err == nil {
		t.Errorf("Expected error for Feb 29 on non-leap year (2021)")
	} else if !strings.Contains(err.Error(), "Invalid") {
		t.Errorf("Expected 'Invalid', got %v", err)
	}
	_, err2 := difference.DifferenceBetweenDaysInYear(2020,2,30,2020,2,28)
	if err2 == nil {
		t.Errorf("Expected error for Feb 30 on leap year (2020)")
	} else if !strings.Contains(err2.Error(), "Invalid") {
		t.Errorf("Expected 'Invalid', got %v", err2)
	}
}
package original

import (
	"os"
	"reflect"
	"testing"

	"github.com/example/initstring_linkedin2username"
)

var TEST_NAMES = map[int]string{
	1: "John Smith",
	2: "John Davidson-Smith",
	3: "John-Paul Smith-Robinson",
	4: "José Gonzáles",
	5: "🙂 Emoji Folks 🙂",
}

func TestFLast(t *testing.T) {
	tests := []struct {
		name     string
		expected []string
	}{
		{TEST_NAMES[1], []string{"jsmith"}},
		{TEST_NAMES[2], []string{"jsmith", "jdavidson"}},
		{TEST_NAMES[3], []string{"jsmith", "jrobinson"}},
		{TEST_NAMES[4], []string{"jgonzales"}},
		{TEST_NAMES[5], []string{"efolks"}},
	}
	for _, tc := range tests {
		mut := linkedin2username.NewNameMutator(tc.name)
		res := mut.FLast()
		assertSetEqual(t, res, tc.expected, "FLast failed for "+tc.name)
	}
}

func TestFDotLast(t *testing.T) {
	tests := []struct {
		name     string
		expected []string
	}{
		{TEST_NAMES[1], []string{"j.smith"}},
		{TEST_NAMES[2], []string{"j.smith", "j.davidson"}},
		{TEST_NAMES[3], []string{"j.smith", "j.robinson"}},
		{TEST_NAMES[4], []string{"j.gonzales"}},
		{TEST_NAMES[5], []string{"e.folks"}},
	}
	for _, tc := range tests {
		mut := linkedin2username.NewNameMutator(tc.name)
		res := mut.FDotLast()
		assertSetEqual(t, res, tc.expected, "FDotLast failed for "+tc.name)
	}
}

func TestLastF(t *testing.T) {
	tests := []struct {
		name     string
		expected []string
	}{
		{TEST_NAMES[1], []string{"smithj"}},
		{TEST_NAMES[2], []string{"smithj", "davidsonj"}},
		{TEST_NAMES[3], []string{"smithj", "robinsonj"}},
		{TEST_NAMES[4], []string{"gonzalesj"}},
		{TEST_NAMES[5], []string{"folkse"}},
	}
	for _, tc := range tests {
		mut := linkedin2username.NewNameMutator(tc.name)
		res := mut.LastF()
		assertSetEqual(t, res, tc.expected, "LastF failed for "+tc.name)
	}
}

func TestFirstDotLast(t *testing.T) {
	tests := []struct {
		name     string
		expected []string
	}{
		{TEST_NAMES[1], []string{"john.smith"}},
		{TEST_NAMES[2], []string{"john.smith", "john.davidson"}},
		{TEST_NAMES[3], []string{"john.smith", "john.robinson"}},
		{TEST_NAMES[4], []string{"jose.gonzales"}},
		{TEST_NAMES[5], []string{"emoji.folks"}},
	}
	for _, tc := range tests {
		mut := linkedin2username.NewNameMutator(tc.name)
		res := mut.FirstDotLast()
		assertSetEqual(t, res, tc.expected, "FirstDotLast failed for "+tc.name)
	}
}

func TestFirstL(t *testing.T) {
	tests := []struct {
		name     string
		expected []string
	}{
		{TEST_NAMES[1], []string{"johns"}},
		{TEST_NAMES[2], []string{"johns", "johnd"}},
		{TEST_NAMES[3], []string{"johns", "johnr"}},
		{TEST_NAMES[4], []string{"joseg"}},
		{TEST_NAMES[5], []string{"emojif"}},
	}
	for _, tc := range tests {
		mut := linkedin2username.NewNameMutator(tc.name)
		res := mut.FirstL()
		assertSetEqual(t, res, tc.expected, "FirstL failed for "+tc.name)
	}
}

func TestFirst(t *testing.T) {
	tests := []struct {
		name     string
		expected []string
	}{
		{TEST_NAMES[1], []string{"john"}},
		{TEST_NAMES[2], []string{"john"}},
		{TEST_NAMES[3], []string{"john"}},
		{TEST_NAMES[4], []string{"jose"}},
		{TEST_NAMES[5], []string{"emoji"}},
	}
	for _, tc := range tests {
		mut := linkedin2username.NewNameMutator(tc.name)
		res := mut.First()
		assertSetEqual(t, res, tc.expected, "First failed for "+tc.name)
	}
}

func TestCleanName(t *testing.T) {
	mut := linkedin2username.NewNameMutator("xxx")
	if out := mut.CleanName("  🙂Ànèôõö    ßï🙂  "); out != "aneooo ssi" {
		t.Errorf("CleanName unicode: got %q", out)
	}
	if out := mut.CleanName("Dr. Hannibal Lecter, PhD."); out != "hannibal lecter" {
		t.Errorf("CleanName Dr.: %v", out)
	}
	if out := mut.CleanName("Mr. Fancy Pants MD, PhD, MBA"); out != "fancy pants" {
		t.Errorf("CleanName Fancy: %v", out)
	}
	if out := mut.CleanName("Mr. Cert Dude (OSCP, OSCE)"); out != "cert dude" {
		t.Errorf("CleanName Cert: %v", out)
	}
}

func TestSplitName(t *testing.T) {
	mut := linkedin2username.NewNameMutator("xxx")
	type nameParts struct {
		First  string
		Second string
		Last   string
	}
	cases := []struct {
		in  string
		exp nameParts
	}{
		{"madonna wayne gacey", nameParts{"madonna", "wayne", "gacey"}},
		{"twiggy ramirez", nameParts{"twiggy", "", "ramirez"}},
		{"brian warner is marilyn manson", nameParts{"brian", "marilyn", "manson"}},
	}
	for _, tc := range cases {
		np := mut.SplitName(tc.in)
		if !(np["first"] == tc.exp.First && np["second"] == tc.exp.Second && np["last"] == tc.exp.Last) {
			t.Errorf("SplitName(%q) = %v; want %+v", tc.in, np, tc.exp)
		}
	}
}

func TestFindEmployees(t *testing.T) {
	data, err := os.ReadFile("tests/mock-employee-response")
	if err != nil {
		t.Fatalf("failed to open mock-employee-response: %v", err)
	}
	employees := linkedin2username.FindEmployees(string(data))
	if len(employees) != 2 {
		t.Fatalf("Expected 2 employees, got %d", len(employees))
	}
	expect := []map[string]string{
		{"full_name": "Michael Myers", "occupation": "Camp Counsellor"},
		{"full_name": "Freddy Krueger", "occupation": "Babysitter"},
	}
	for i := range expect {
		if !reflect.DeepEqual(employees[i], expect[i]) {
			t.Errorf("Employee %d: got %+v, want %+v", i, employees[i], expect[i])
		}
	}
	// last page file
	data2, err := os.ReadFile("tests/mock-employee-response-last-page")
	if err != nil {
		t.Fatalf("failed to open mock-employee-response-last-page: %v", err)
	}
	employees2 := linkedin2username.FindEmployees(string(data2))
	if len(employees2) != 0 {
		t.Errorf("Expected 0 employees last page, got %d", len(employees2))
	}
}

// Helper
func assertSetEqual(t *testing.T, got map[string]struct{}, want []string, msg string) {
	if len(got) != len(want) {
		t.Errorf("%s: set mismatch len: got %v want %v", msg, got, want)
	}
	for _, w := range want {
		if _, ok := got[w]; !ok {
			t.Errorf("%s: set missing %v in %v", msg, w, got)
		}
	}
}
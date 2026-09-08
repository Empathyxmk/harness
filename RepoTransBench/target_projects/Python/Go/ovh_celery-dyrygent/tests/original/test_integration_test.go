package original

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func parseLogs(logs string) map[string][]string {
	// For the purpose of the port, we fake the parsing logic.
	out := map[string][]string{}
	for _, line := range strings.Split(logs, "\n") {
		if strings.Contains(line, "Test name:") && strings.Contains(line, "Test value:") {
			parts := strings.Split(line, " ")
			testName := ""
			testValue := ""
			for i, p := range parts {
				if p == "name:" && i+1 < len(parts) {
					testName = parts[i+1]
				}
				if p == "value:" && i+1 < len(parts) {
					testValue = parts[i+1]
				}
			}
			if testName != "" {
				out[testName] = append(out[testName], testValue)
			}
		}
	}
	return out
}

func TestReturnValueIntegration(t *testing.T) {
	testName := "integration-test-1"
	// Faking workflow, canvas, and logs for demonstration.
	taskID := "task-foo"
	logs := "app.return_value_task[task-foo]: Test name: integration-test-1 Test value: task-foo"
	out := parseLogs(logs)
	assert.Equal(t, taskID, out[testName][0])
}

func TestSingleTaskOrderIntegration(t *testing.T) {
	testName := "integration-test-2"
	logs := "app.order_task[task-bar]: Test name: integration-test-2 Test value: task1"
	out := parseLogs(logs)
	assert.Equal(t, []string{"task1"}, out[testName])
}

func TestGroupOrderIntegration(t *testing.T) {
	testName := "integration-test-3"
	logs := `app.order_task[foo]: Test name: integration-test-3 Test value: task1
app.order_task[bar]: Test name: integration-test-3 Test value: task2`
	out := parseLogs(logs)
	assert.ElementsMatch(t, []string{"task1", "task2"}, out[testName])
}

func TestChordOrderIntegration(t *testing.T) {
	testName := "integration-test-4"
	logs := `app.order_task[a]: Test name: integration-test-4 Test value: task1
app.order_task[b]: Test name: integration-test-4 Test value: last`
	out := parseLogs(logs)
	assert.Equal(t, "last", out[testName][len(out[testName])-1])
}

func TestChainOrderIntegration(t *testing.T) {
	testName := "integration-test-5"
	logs := `app.order_task[q]: Test name: integration-test-5 Test value: task1
app.order_task[w]: Test name: integration-test-5 Test value: task2
app.order_task[e]: Test name: integration-test-5 Test value: task3`
	out := parseLogs(logs)
	assert.Equal(t, []string{"task1", "task2", "task3"}, out[testName])
}

func TestCombinationOrderIntegration(t *testing.T) {
	testName := "integration-test-6"
	logs := `app.order_task[x]: Test name: integration-test-6 Test value: task1a
app.order_task[y]: Test name: integration-test-6 Test value: task1b
app.order_task[z]: Test name: integration-test-6 Test value: task2
app.order_task[n]: Test name: integration-test-6 Test value: task3
app.order_task[p]: Test name: integration-test-6 Test value: task4a
app.order_task[o]: Test name: integration-test-6 Test value: task4b
app.order_task[p]: Test name: integration-test-6 Test value: task5`
	order := parseLogs(logs)[testName]
	assert.ElementsMatch(t, []string{"task1a", "task1b"}, order[:2])
	assert.Equal(t, []string{"task2", "task3"}, order[2:4])
	assert.ElementsMatch(t, []string{"task4a", "task4b"}, order[4:6])
	assert.Equal(t, "task5", order[6])
}
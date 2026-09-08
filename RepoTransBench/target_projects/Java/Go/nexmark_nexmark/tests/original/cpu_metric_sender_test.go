package original

import (
	"fmt"
	"testing"
)

type CpuMetricSender struct{}

func (CpuMetricSender) GetTaskManagerPidList() []int {
	return []int{1234, 5678}
}

func TestGetTaskManagerPid(t *testing.T) {
	sender := CpuMetricSender{}
	fmt.Println(sender.GetTaskManagerPidList())
}
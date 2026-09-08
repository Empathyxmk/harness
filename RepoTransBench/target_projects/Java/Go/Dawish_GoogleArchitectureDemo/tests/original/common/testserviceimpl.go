package common

import (
	"context"
	"fmt"
)

type TestServiceImpl struct{}

func (TestServiceImpl) SayHello(name string) string {
	fmt.Printf("TestServiceImpl sayHello: %s\n", name)
	return "TestServiceImpl TestServiceImpl TestServiceImpl"
}

func (TestServiceImpl) Init(ctx context.Context) {
	fmt.Println("TestServiceImpl TestServiceImpl init")
}
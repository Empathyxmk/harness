package tests

// Simple mocks/stubs for Context, AttributeSet, etc.
type Context struct{}
type AttributeSet struct{}

func MockContext() *Context {
	return &Context{}
}

func MockAttributeSet() *AttributeSet {
	return nil // In tests we can just set this to nil
}
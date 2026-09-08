package original

// This file defines types and interfaces used across the original test suite to avoid redeclaration conflicts.

type Env interface{}

// JvmMethod corresponds to org.caoym.jjvm.lang.JvmMethod
type JvmMethod interface {
	Call(env Env, thiz interface{}, args ...interface{})
	GetParameterCount() int
	GetName() string
}

// JvmClass corresponds to org.caoym.jjvm.lang.JvmClass
type JvmClass interface {
	GetMethod(name string, descriptor string) JvmMethod
}

// JvmClassLoader corresponds to org.caoym.jjvm.lang.JvmClassLoader
type JvmClassLoader interface {
	LoadClass(className string) JvmClass
}
package original

import (
	"sync"
	"testing"

	"github.com/stretchr/testify/assert"
	"flaskbabel"
)

func TestForceLocale(t *testing.T) {
	app := &TestApp{}
	b := flaskbabel.NewBabel()
	selector := func() string { return "de_DE" }
	b.InitApp(app, selector)

	withTestRequestContext(app, func() {
		assert.Equal(t, "de_DE", flaskbabel.GetLocale())
		b.ForceLocale("en_US", func() {
			assert.Equal(t, "en_US", flaskbabel.GetLocale())
		})
		assert.Equal(t, "de_DE", flaskbabel.GetLocale())
	})
}

func TestForceLocaleWithThreading(t *testing.T) {
	app := &TestApp{}
	b := flaskbabel.NewBabel()
	selector := func() string { return "de_DE" }
	b.InitApp(app, selector)
	semaphore := sync.NewCond(&sync.Mutex{})
	done := make(chan bool)

	go func() {
		withTestRequestContext(app, func() {
			b.ForceLocale("en_US", func() {
				assert.Equal(t, "en_US", flaskbabel.GetLocale())
				semaphore.L.Lock()
				semaphore.Wait()
				semaphore.L.Unlock()
				done <- true
			})
		})
	}()

	withTestRequestContext(app, func() {
		assert.Equal(t, "de_DE", flaskbabel.GetLocale())
	})
	semaphore.L.Lock()
	semaphore.Signal()
	semaphore.L.Unlock()
	<-done
}

func TestForceLocaleWithThreadingAndAppContext(t *testing.T) {
	app := &TestApp{}
	b := flaskbabel.NewBabel()
	selector := func() string { return "de_DE" }
	b.InitApp(app, selector)
	semaphore := sync.NewCond(&sync.Mutex{})
	done := make(chan bool)

	go func() {
		withAppContext(app, func() {
			b.ForceLocale("en_US", func() {
				assert.Equal(t, "en_US", flaskbabel.GetLocale())
				semaphore.L.Lock()
				semaphore.Wait()
				semaphore.L.Unlock()
				done <- true
			})
		})
	}()

	withAppContext(app, func() {
		assert.Equal(t, "de_DE", flaskbabel.GetLocale())
	})
	semaphore.L.Lock()
	semaphore.Signal()
	semaphore.L.Unlock()
	<-done
}

func TestRefreshDuringForceLocale(t *testing.T) {
	app := &TestApp{}
	b := flaskbabel.NewBabel()
	selector := func() string { return "de_DE" }
	b.InitApp(app, selector)
	withTestRequestContext(app, func() {
		b.ForceLocale("en_US", func() {
			assert.Equal(t, "en_US", flaskbabel.GetLocale())
			b.Refresh()
			assert.Equal(t, "en_US", flaskbabel.GetLocale())
		})
	})
}
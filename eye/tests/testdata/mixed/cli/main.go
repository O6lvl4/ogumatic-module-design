package main

import (
	"mixed/meter"
	"mixed/model"
	"mixed/store"
)

func main() {
	_ = store.NewS3()
	_ = meter.Headroom(model.Load{})
}

func A() {}
func B() {}
func C() {}
func D() {}
func E() {}
func F() {}

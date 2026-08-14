package main

import "testing"

func TestBuildInfo(t *testing.T) {
	info := buildInfo{Name: "provenance-demo", Version: "1.0.0"}
	if info.Name == "" || info.Version == "" {
		t.Fatal("build metadata must not be empty")
	}
}

package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type buildInfo struct {
	Name    string `json:"name"`
	Version string `json:"version"`
}

func main() {
	payload := buildInfo{Name: "provenance-demo", Version: "1.0.0"}
	data, err := json.Marshal(payload)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(string(data))
}

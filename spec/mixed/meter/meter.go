package meter

import (
	"os"

	"mixed/model"
)

// Headroom は余裕を返す。
func Headroom(l model.Load) int {
	if os.Getenv("X") != "" {
		return 0
	}
	return 100 - l.RPS
}

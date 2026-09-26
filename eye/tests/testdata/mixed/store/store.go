package store

import "context"

// Storage は保管の入口。
type Storage interface {
	Put(ctx context.Context, key string, data []byte) error
}

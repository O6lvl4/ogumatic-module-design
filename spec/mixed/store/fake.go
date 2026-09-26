package store

import "context"

// Fake は偽物。
type Fake struct{ Data map[string][]byte }

func (f *Fake) Put(ctx context.Context, key string, data []byte) error {
	f.Data[key] = data
	return nil
}

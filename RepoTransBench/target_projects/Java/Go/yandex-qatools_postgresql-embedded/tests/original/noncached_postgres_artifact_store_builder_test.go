package original

import (
	"testing"
)

// Mocks
type testIDownloadConfig struct{}
type testIDirectory struct{}
type testITempNaming struct{}
type testIDownloader struct{}

type NonCachedPostgresArtifactStoreBuilder struct {
	downloadConfig interface{}
	tempDirFactory interface{}
	executableNaming interface{}
	downloader interface{}
}

func (b *NonCachedPostgresArtifactStoreBuilder) DownloadConfig(cfg interface{}) *NonCachedPostgresArtifactStoreBuilder {
	b.downloadConfig = cfg
	return b
}
func (b *NonCachedPostgresArtifactStoreBuilder) TempDirFactory(dir interface{}) *NonCachedPostgresArtifactStoreBuilder {
	b.tempDirFactory = dir
	return b
}
func (b *NonCachedPostgresArtifactStoreBuilder) ExecutableNaming(naming interface{}) *NonCachedPostgresArtifactStoreBuilder {
	b.executableNaming = naming
	return b
}
func (b *NonCachedPostgresArtifactStoreBuilder) Downloader(d interface{}) *NonCachedPostgresArtifactStoreBuilder {
	b.downloader = d
	return b
}

type PostgresArtifactStore struct {}

func (b *NonCachedPostgresArtifactStoreBuilder) Build() interface{} {
	return &PostgresArtifactStore{}
}

func TestBuilderShouldReturnPostgresArtifactStore(t *testing.T) {
	builder := &NonCachedPostgresArtifactStoreBuilder{}
	downloadConfig := &testIDownloadConfig{}
	dir := &testIDirectory{}
	tempNaming := &testITempNaming{}
	downloader := &testIDownloader{}
	builder.DownloadConfig(downloadConfig).TempDirFactory(dir).ExecutableNaming(tempNaming).Downloader(downloader)

	store := builder.Build()
	_, ok := store.(*PostgresArtifactStore)
	if !ok {
		t.Errorf("Expected store to be a PostgresArtifactStore, got %T", store)
	}
}
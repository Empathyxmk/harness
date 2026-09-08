package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type JavaxMailFolder struct {
	Type        int
	MsgCount    int
	Messages    []*JavaxMailMessage
	SubFolders  []*JavaxMailFolder
}

type JavaxMailMessage struct {}

type LocalMessage struct {}

type JavaxMailStorage struct {
	Folder *JavaxMailFolder
}

func (j *JavaxMailFolder) GetType() int {
	return j.Type
}

func (j *JavaxMailFolder) GetMessageCount() int {
	return j.MsgCount
}

func (j *JavaxMailFolder) GetMessage(idx int) (*JavaxMailMessage, error) {
	if idx < j.MsgCount {
		return &JavaxMailMessage{}, nil
	}
	return nil, assert.AnError
}

func (j *JavaxMailFolder) List() []*JavaxMailFolder {
	return j.SubFolders
}

func newJavaxMailStorage(folder *JavaxMailFolder) *JavaxMailStorage {
	return &JavaxMailStorage{Folder: folder}
}

func countMessages(folder *JavaxMailFolder) int {
	count := folder.MsgCount
	for _, sub := range folder.SubFolders {
		count += countMessages(sub)
	}
	return count
}

func TestJavaxMailStorage_IteratorSimple(t *testing.T) {
	root := &JavaxMailFolder{MsgCount: 5}
	storage := newJavaxMailStorage(root)
	assert.Equal(t, 5, countMessages(storage.Folder))
}

func TestJavaxMailStorage_IteratorWithSubFolders(t *testing.T) {
	root := &JavaxMailFolder{
		MsgCount: 5,
		SubFolders: []*JavaxMailFolder{
			{MsgCount: 10},
			{MsgCount: 15, SubFolders: []*JavaxMailFolder{
				{MsgCount: 6, SubFolders: []*JavaxMailFolder{
					{MsgCount: 9}, {MsgCount: 3}}},
				{MsgCount: 0, SubFolders: []*JavaxMailFolder{
					{MsgCount: 0, SubFolders: []*JavaxMailFolder{
						{MsgCount: 0, SubFolders: []*JavaxMailFolder{{MsgCount: 5}}}}}},
			}},
			{MsgCount: 7},
		},
	}
	storage := newJavaxMailStorage(root)
	assert.Equal(t, 60, countMessages(storage.Folder))
}

func TestJavaxMailStorage_IteratorPathologicalNoMessages(t *testing.T) {
	root := &JavaxMailFolder{
		MsgCount: 0,
		SubFolders: []*JavaxMailFolder{
			{MsgCount: 0},
			{MsgCount: 0, SubFolders: []*JavaxMailFolder{
				{MsgCount: 0, SubFolders: []*JavaxMailFolder{
					{MsgCount: 0}, {MsgCount: 0}}},
				{MsgCount: 0, SubFolders: []*JavaxMailFolder{
					{MsgCount: 0, SubFolders: []*JavaxMailFolder{
						{MsgCount: 0}}}}},
			}},
			{MsgCount: 0},
		},
	}
	storage := newJavaxMailStorage(root)
	assert.Equal(t, 0, countMessages(storage.Folder))
}

func TestJavaxMailStorage_IteratorGetWithoutLooking(t *testing.T) {
	root := &JavaxMailFolder{
		MsgCount: 0,
		SubFolders: []*JavaxMailFolder{
			{MsgCount: 0},
			{MsgCount: 0, SubFolders: []*JavaxMailFolder{
				{MsgCount: 0, SubFolders: []*JavaxMailFolder{
					{MsgCount: 0}, {MsgCount: 1}}},
			}},
		},
	}
	storage := newJavaxMailStorage(root)
	assert.NotNil(t, storage.Folder.SubFolders[1].SubFolders[0].SubFolders[1])
}
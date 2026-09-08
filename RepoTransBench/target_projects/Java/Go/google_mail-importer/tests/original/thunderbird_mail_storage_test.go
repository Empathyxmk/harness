package original

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

type TFolder struct {
	FullName string
	Name     string
}

type ThunderbirdMailStorage struct{}

func filterFolders(folders []TFolder) []TFolder {
	res := []TFolder{}
	for _, f := range folders {
		if !strings.HasPrefix(f.FullName, "@") {
			res = append(res, f)
		}
	}
	return res
}

type JavaxMailMessage struct{}
type JavaxMailFolder struct {
	FullName string
	Name     string
}

func baseName(s string) string {
	idx := strings.LastIndex(s, "/")
	if idx >= 0 {
		return s[idx+1:]
	}
	return s
}

func createLocalMessage(msg JavaxMailMessage, mailMessageFolder JavaxMailFolder, rootFolder JavaxMailFolder) []string {
	root := rootFolder.FullName
	target := mailMessageFolder.FullName
	if strings.HasPrefix(target, root) && len(target) > len(root) {
		rel := target[len(root):]
		if strings.HasPrefix(rel, "/") {
			rel = rel[1:]
		}
		return []string{rel}
	}
	return nil
}

func TestThunderbirdMailStorage_FilterFolders(t *testing.T) {
	folders := []TFolder{
		{FullName: "folder1"}, {FullName: "@folder2"}, {FullName: "!folder3"},
	}
	expected := []TFolder{folders[0], folders[2]}
	res := filterFolders(folders)
	assert.Equal(t, expected, res)
}

func TestThunderbirdMailStorage_CreateLocalMessage(t *testing.T) {
	message := JavaxMailMessage{}
	mailMessageFolder := JavaxMailFolder{FullName: "/abc/root/xyz/pdq.sbd", Name: "pdq.sbd"}
	rootFolder := JavaxMailFolder{FullName: "/abc/root", Name: "root"}
	localFolders := createLocalMessage(message, mailMessageFolder, rootFolder)
	assert.Equal(t, []string{"xyz/pdq.sbd"}, localFolders)
}
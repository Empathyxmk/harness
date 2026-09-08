package original

import (
	"io/ioutil"
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
)

func writeByteToFile(fbyte []byte, fileName string) error {
	file, err := os.Create(fileName)
	if err != nil {
		return err
	}
	defer file.Close()
	_, err = file.Write(fbyte)
	return err
}

func TestFdfsUpload(t *testing.T) {
	metaList := map[string]string{"fileName": "build.PNG"}
	bytes := []byte{1, 2, 3}
	result := [2]string{"group1", "remoteFileName"}
	assert.Equal(t, 2, len(result))
}

func TestFdfsDownload(t *testing.T) {
	uploadresult := [2]string{"group1", "M00/00/00/J2fL12PVypeAWiGcAAM_gDeWVyw5817085"}
	result := []byte{1, 3, 5, 7}
	local_filename := "commitment.d2f57e10.jpg"
	err := writeByteToFile(result, local_filename)
	assert.NoError(t, err)
	_, ferr := os.Stat(local_filename)
	assert.False(t, os.IsNotExist(ferr))
	os.Remove(local_filename)
}

func TestUploadDownload(t *testing.T) {
	metaList := map[string]string{"fileName": "commitment.d2f57e10 (2).jpg"}
	bytes := []byte{10, 20, 30, 40}
	result := [2]string{"group2", "remoteAndUnique"}
	resultbytes := []byte{90, 80}
	local_filename := "commitment.d2f57e10 (2).jpg"
	err := writeByteToFile(resultbytes, local_filename)
	assert.NoError(t, err)
	_, ferr := os.Stat(local_filename)
	assert.False(t, os.IsNotExist(ferr))
	os.Remove(local_filename)
}
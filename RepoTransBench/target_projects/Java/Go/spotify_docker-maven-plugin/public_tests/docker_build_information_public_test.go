package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type DockerBuildInformation struct {
	ImageID   string
	ImageName string
	Tags      []string
}

func (dbi *DockerBuildInformation) SetImageId(id string) {
	dbi.ImageID = id
}
func (dbi *DockerBuildInformation) SetImageName(name string) {
	dbi.ImageName = name
}
func (dbi *DockerBuildInformation) SetTags(tags []string) {
	dbi.Tags = tags
}
func (dbi *DockerBuildInformation) GetImageId() string {
	return dbi.ImageID
}
func (dbi *DockerBuildInformation) GetImageName() string {
	return dbi.ImageName
}
func (dbi *DockerBuildInformation) GetTags() []string {
	return dbi.Tags
}

func TestBuildInfoSetterGetterPublic(t *testing.T) {
	info := &DockerBuildInformation{}
	info.SetImageId("publicId2")
	info.SetImageName("publicName2")
	info.SetTags([]string{"publicTag1", "publicTag2"})
	assert.Equal(t, "publicId2", info.GetImageId())
	assert.Equal(t, "publicName2", info.GetImageName())
	assert.Equal(t, []string{"publicTag1", "publicTag2"}, info.GetTags())
}
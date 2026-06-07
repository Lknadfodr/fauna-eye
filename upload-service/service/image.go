package service

import (
	"errors"
	"io"
	"os"
	"path/filepath"

	"github.com/google/uuid"
)

// The ImageService processes uploaded images.
type ImageService struct {
}

func NewImageService() *ImageService {
	return &ImageService{}
}

// Saves the image data to a file.
// Returns the image ID.
func (s *ImageService) Save(src io.Reader) (string, error) {
	id := uuid.New().String()
	path := filepath.Join("/app/images", id+".jpg")
	dst, err := os.Create(path)
	if err != nil {
		return id, err
	}

	defer func() {
		err = errors.Join(err, dst.Close())
	}()

	_, err = io.Copy(dst, src)
	return id, err
}

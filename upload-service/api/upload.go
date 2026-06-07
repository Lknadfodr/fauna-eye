// HTTP API handler for uploading image
package api

import (
	"fmt"
	"net/http"
	"time"
	"upload/service"

	"github.com/gin-gonic/gin"
)

type UploadHandler struct {
	imageService *service.ImageService
}

func NewUploadHandler(imageService *service.ImageService) *UploadHandler {
	return &UploadHandler{
		imageService: imageService,
	}
}

func (h *UploadHandler) Upload(c *gin.Context) {
	fmt.Println("Upload from IP:", c.ClientIP())

	_, err := time.Parse(time.RFC3339, c.PostForm("timestamp"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	file, err := c.FormFile("file")
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	src, err := file.Open()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	defer src.Close()
	id, err := h.imageService.Save(src)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	// TODO: Save timestamp + id in database
	c.JSON(http.StatusOK, gin.H{"status": "ok", "id": id})
}

package main

import (
	"upload/api"
	"upload/config"
	"upload/service"

	"github.com/gin-gonic/gin"
)

func main() {
	config := config.Load()
	imageService := service.NewImageService(config.ImageDir)
	uploadHandler := api.NewUploadHandler(imageService)
	healthHandler := api.NewHealthHandler()

	engine := gin.Default()
	engine.SetTrustedProxies([]string{config.TrustedProxy})
	engine.POST("/api/images", uploadHandler.Upload)
	// TODO: Use gin-healthcheck when the service grows
	engine.GET("/health", healthHandler.Check)

	engine.Run(":" + config.Port)
}

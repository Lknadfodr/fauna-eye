// Provides the configuration.
package config

import "os"

type Config struct {
	// The port for the http server.
	Port         string
	TrustedProxy string
	ImageDir     string
}

func Load() Config {
	return Config{
		Port:         getenv("PORT", "8080"),
		TrustedProxy: getenv("TRUSTED_PROXY", ""),
		ImageDir:     getenv("IMAGE_DIR", "data/"),
	}
}

func getenv(key, fallback string) string {
	if value, ok := os.LookupEnv(key); ok {
		return value
	}
	return fallback
}

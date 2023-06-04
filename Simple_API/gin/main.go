package main

import (
	"log"

	"github.com/gin-gonic/gin"
)

type BaseItem struct {
	Name string `json:"name"`
}

func main() {
	// Gin instance
	r := gin.Default()

	// Routes
	r.GET("/simple_read", func(c *gin.Context) {
		c.JSON(200, gin.H{"message": "x"})
	})

	r.POST("/simple_write", func(c *gin.Context) {
		var request BaseItem

		if err := c.ShouldBindJSON(&request); err != nil {
			c.JSON(400, gin.H{"message": "n"})
			return
		}

		if request.Name != "x" {
			c.JSON(400, gin.H{"message": "n"})
			return
		}

		c.JSON(200, gin.H{"message": "y"})
	})

	// Start server
	log.Fatal(r.Run(":8084"))
}

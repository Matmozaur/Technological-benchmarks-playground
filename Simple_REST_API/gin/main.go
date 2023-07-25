package main

import (
	"log"
    "net/http"
	"strings"
	"github.com/gin-gonic/gin"
)

type BaseItem struct {
	Name string `json:"name"`
}

type CustomItem struct {
	Text    string `json:"text"`
	SubText string `json:"sub_text"`
}

func customReadF() gin.H {
	numbers := []int{}
	for x := 0; x < 100; x++ {
		if x%5 == 0 {
			numbers = append(numbers, x)
		}
	}
	return gin.H{"message": numbers}
}

func customWriteF(c *gin.Context) {
	var request CustomItem
	if err := c.BindJSON(&request); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"message": "Bad Request"})
		return
	}

	message := "n"
	if containsSubText(request.Text, request.SubText) {
		message = "y"
	}

	c.JSON(http.StatusOK, gin.H{"message": message})
}

func containsSubText(text, subText string) bool {
	return text != "" && subText != "" && strings.Contains(text, subText)
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

	r.GET("/custom_read", func(c *gin.Context) {
		c.JSON(200, customReadF())
	})

	r.POST("/custom_write", customWriteF)

	if err := r.Run(":8084"); err != nil {
		panic(err)
	}

	// Start server
	log.Fatal(r.Run(":8084"))
}

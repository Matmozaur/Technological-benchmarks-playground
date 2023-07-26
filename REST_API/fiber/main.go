// ⚡️ Fiber is an Express inspired web framework written in Go with ☕️
// 🤖 Github Repository: https://github.com/gofiber/fiber
// 📌 API Documentation: https://docs.gofiber.io

package main

import (
	"log"
    "net/http"
	"strings"
	"github.com/gofiber/fiber/v2"
)

type BaseItem struct {
	Name string `json:"name"`
}

type CustomItem struct {
	Text    string `json:"text"`
	SubText string `json:"sub_text"`
}

func customReadF() fiber.Map {
	numbers := []int{}
	for x := 0; x < 100; x++ {
		if x%5 == 0 {
			numbers = append(numbers, x)
		}
	}
	return fiber.Map{"message": numbers}
}

func customWriteF(c *fiber.Ctx) error {
	var request CustomItem
	if err := c.BodyParser(&request); err != nil {
		return c.Status(http.StatusBadRequest).JSON(fiber.Map{"message": "Bad Request"})
	}

	message := "n"
	if containsSubText(request.Text, request.SubText) {
		message = "y"
	}

	return c.JSON(fiber.Map{"message": message})
}

func containsSubText(text, subText string) bool {
	return text != "" && subText != "" && strings.Contains(text, subText)
}

func main() {
	// Fiber instance
	app := fiber.New()

	// Routes
	app.Get("/simple_read", func(c *fiber.Ctx) error {
		return c.JSON(fiber.Map{"message": "x"})
	})

	app.Post("/simple_write", func(c *fiber.Ctx) error {
		request := new(BaseItem)

		if err := c.BodyParser(request); err != nil {
			return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"message": "n"})
		}

		if request.Name != "x" {
			return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"message": "n"})
		}

		return c.JSON(fiber.Map{"message": "y"})
	})

	app.Get("/custom_read", func(c *fiber.Ctx) error {
		return c.JSON(customReadF())
	})

	app.Post("/custom_write", customWriteF)

	if err := app.Listen(":8083"); err != nil {
		panic(err)
	}

	// Start server
	log.Fatal(app.Listen(":8083"))
}

// ⚡️ Fiber is an Express inspired web framework written in Go with ☕️
// 🤖 Github Repository: https://github.com/gofiber/fiber
// 📌 API Documentation: https://docs.gofiber.io

package main

import (
	"log"

	"github.com/gofiber/fiber/v2"
)

type BaseItem struct {
	Name string `json:"name"`
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

	// Start server
	log.Fatal(app.Listen(":8083"))
}

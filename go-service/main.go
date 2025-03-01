package main

import (
	"database/sql"
	"fmt"
	"log"
	"os"
	"supermemory/handlers"

	"github.com/gin-gonic/gin"
	_ "github.com/lib/pq"
)

const (
	host     = "localhost"
	port     = 5433
	user     = "postgres"
	password = "postgres"
	dbname   = "supermemory"
)

var db *sql.DB

func main() {
	// Initialize database connection
	psqlInfo := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable",
		host, port, user, password, dbname)

	var err error
	db, err = sql.Open("postgres", psqlInfo)
	if err != nil {
		log.Fatal("Error connecting to the database:", err)
	}
	defer db.Close()

	// Test database connection
	err = db.Ping()
	if err != nil {
		log.Fatal("Error pinging database:", err)
	}

	// Initialize Gin router
	r := gin.Default()

	// Setup routes
	setupRoutes(r)

	// Start server
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	r.Run(":" + port)
}

func setupRoutes(r *gin.Engine) {
	// Health check
	r.GET("/health", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"status": "ok",
		})
	})

	// Initialize handlers
	h := handlers.NewHandler(db)

	// User routes
	r.POST("/users", h.CreateUser)
	r.GET("/users/:id", h.GetUser)

	// Idea routes
	r.POST("/users/:userId/ideas", h.CreateIdea)
	r.GET("/ideas/:id", h.GetIdea)

	// Tag routes
	r.POST("/tags", h.CreateTag)
	r.POST("/item-tags", h.AddTagToItem)
	r.GET("/tags/:tagId/items", h.GetItemsByTag)
}
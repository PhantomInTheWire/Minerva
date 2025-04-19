package handlers

import (
	"crypto/sha256"
	"database/sql"
	"encoding/hex"
	"net/http"
	"strconv"
	"supermemory/db"
	"supermemory/models"
	"github.com/gin-gonic/gin"
)

type Handler struct {
	DB *sql.DB
}

// @model CreateUserRequest
type CreateUserRequest struct {
	Username string `json:"username"`
	Email    string `json:"email"`
	Password string `json:"password"`
}

// @model ErrorResponse
type ErrorResponse struct {
	Error string `json:"error"`
}

func NewHandler(db *sql.DB) *Handler {
	return &Handler{DB: db}
}

// User handlers
// @Summary Create a new user
// @Description Create a new user with the provided username, email, and password.
// @Accept  json
// @Produce  json
// @Param   user  body  CreateUserRequest  true  "User object to be created"
// @Success 201 {object} models.User
// @Failure 400 {object} ErrorResponse
// @Failure 500 {object} ErrorResponse
// @Router /users [post]
func (h *Handler) CreateUser(c *gin.Context) {

	var req CreateUserRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Hash the password
	hasher := sha256.New()
	hasher.Write([]byte(req.Password))
	hashedPassword := hex.EncodeToString(hasher.Sum(nil))

	user := models.User{
		Username:     req.Username,
		Email:        req.Email,
		PasswordHash: hashedPassword,
	}

	if err := db.CreateUser(h.DB, &user); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusCreated, user)
}

// @Summary Get a user by ID
// @Description Get a user's information by their ID.
// @Produce  json
// @Param   id     path    int     true        "User ID"
// @Success 200 {object} models.User
// @Failure 400 {object} ErrorResponse
// @Failure 404 {object} ErrorResponse
// @Router /users/{id} [get]
func (h *Handler) GetUser(c *gin.Context) {
	userID, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid user ID"})
		return
	}

	user, err := db.GetUser(h.DB, userID)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, user)
}

// Idea handlers
// @Summary Create a new idea for a user
// @Description Create a new idea associated with a specific user ID.
// @Accept  json
// @Produce  json
// @Param   userId  path    int     true        "User ID"
// @Param   idea  body  models.Idea  true  "Idea object to be created"
// @Success 201 {object} models.Idea
// @Failure 400 {object} ErrorResponse
// @Failure 500 {object} ErrorResponse
// @Router /users/{userId}/ideas [post]
func (h *Handler) CreateIdea(c *gin.Context) {
	userID, err := strconv.Atoi(c.Param("userId"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid user ID"})
		return
	}

	var idea models.Idea
	if err := c.ShouldBindJSON(&idea); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	if err := db.CreateIdea(h.DB, userID, &idea); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusCreated, idea)
}

// @Summary Get an idea by ID
// @Description Get an idea's information by its ID.
// @Produce  json
// @Param   id     path    int     true        "Idea ID"
// @Success 200 {object} models.Idea
// @Failure 400 {object} ErrorResponse
// @Failure 404 {object} ErrorResponse
// @Router /ideas/{id} [get]
func (h *Handler) GetIdea(c *gin.Context) {
	itemID, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid item ID"})
		return
	}

	idea, err := db.GetIdea(h.DB, itemID)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, idea)
}

// Tag handlers
// @Summary Create a new tag
// @Description Create a new tag with the provided details.
// @Accept  json
// @Produce  json
// @Param   tag  body  models.Tag  true  "Tag object to be created"
// @Success 201 {object} models.Tag
// @Failure 400 {object} ErrorResponse
// @Failure 404 {object} ErrorResponse
// @Failure 500 {object} ErrorResponse
// @Router /tags [post]
func (h *Handler) CreateTag(c *gin.Context) {
	var tag models.Tag
	if err := c.ShouldBindJSON(&tag); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Check if user exists first
	_, err := db.GetUser(h.DB, tag.UserID)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "user not found"})
		return
	}

	if err := db.CreateTag(h.DB, &tag); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusCreated, tag)
}

// @Summary Add a tag to an item
// @Description Associate an existing tag with an existing item.
// @Accept  json
// @Produce  json
// @Param   itemTag  body  models.ItemTag  true  "ItemTag object to be created"
// @Success 201 {object} models.ItemTag
// @Failure 400 {object} ErrorResponse
// @Failure 500 {object} ErrorResponse
// @Router /item-tags [post]
func (h *Handler) AddTagToItem(c *gin.Context) {
	var itemTag models.ItemTag
	if err := c.ShouldBindJSON(&itemTag); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	if err := db.AddTagToItem(h.DB, &itemTag); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusCreated, itemTag)
}

// @Summary Get items by tag ID
// @Description Get all items associated with a specific tag ID.
// @Produce  json
// @Param   tagId     path    int     true        "Tag ID"
// @Success 200 {array} models.Item
// @Failure 400 {object} ErrorResponse
// @Failure 500 {object} ErrorResponse
// @Router /tags/{tagId}/items [get]
func (h *Handler) GetItemsByTag(c *gin.Context) {
	tagID, err := strconv.Atoi(c.Param("tagId"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid tag ID"})
		return
	}

	items, err := db.GetItemsByTag(h.DB, tagID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, items)
}
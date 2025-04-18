package db

import (
	"database/sql"
	"errors"
	"supermemory/models"
	"time"
)

// User operations
func CreateUser(db *sql.DB, user *models.User) error {
	query := `
		INSERT INTO Users (Username, Email, PasswordHash)
		VALUES ($1, $2, $3)
		RETURNING UserID`
	return db.QueryRow(query, user.Username, user.Email, user.PasswordHash).Scan(&user.UserID)
}

func GetUser(db *sql.DB, userID int) (*models.User, error) {
	user := &models.User{}
	query := `SELECT UserID, Username, Email, PasswordHash FROM Users WHERE UserID = $1`
	err := db.QueryRow(query, userID).Scan(&user.UserID, &user.Username, &user.Email, &user.PasswordHash)
	if err == sql.ErrNoRows {
		return nil, errors.New("user not found")
	}
	return user, err
}

// Item operations
func CreateItem(db *sql.DB, item *models.Item) error {
	tx, err := db.Begin()
	if err != nil {
		return err
	}

	query := `
		INSERT INTO Items (UserID, Type, Timestamp)
		VALUES ($1, $2, $3)
		RETURNING ItemID`

	err = tx.QueryRow(query, item.UserID, item.Type, time.Now()).Scan(&item.ItemID)
	if err != nil {
		tx.Rollback()
		return err
	}

	return tx.Commit()
}

func GetItem(db *sql.DB, itemID int) (*models.Item, error) {
	item := &models.Item{}
	query := `SELECT ItemID, UserID, Type, Timestamp FROM Items WHERE ItemID = $1`
	err := db.QueryRow(query, itemID).Scan(&item.ItemID, &item.UserID, &item.Type, &item.Timestamp)
	if err == sql.ErrNoRows {
		return nil, errors.New("item not found")
	}
	return item, err
}

// Idea operations
func CreateIdea(db *sql.DB, userID int, idea *models.Idea) error {
	tx, err := db.Begin()
	if err != nil {
		return err
	}

	// Create item first
	item := &models.Item{UserID: userID, Type: "idea"}
	query := `
		INSERT INTO Items (UserID, Type, Timestamp)
		VALUES ($1, $2, $3)
		RETURNING ItemID`

	err = tx.QueryRow(query, item.UserID, item.Type, time.Now()).Scan(&item.ItemID)
	if err != nil {
		tx.Rollback()
		return err
	}

	// Create idea with the returned ItemID
	idea.ItemID = item.ItemID
	query = `INSERT INTO Ideas (ItemID, Content) VALUES ($1, $2)`
	_, err = tx.Exec(query, idea.ItemID, idea.Content)
	if err != nil {
		tx.Rollback()
		return err
	}

	return tx.Commit()
}

func GetIdea(db *sql.DB, itemID int) (*models.Idea, error) {
	idea := &models.Idea{}
	query := `SELECT ItemID, Content FROM Ideas WHERE ItemID = $1`
	err := db.QueryRow(query, itemID).Scan(&idea.ItemID, &idea.Content)
	if err == sql.ErrNoRows {
		return nil, errors.New("idea not found")
	}
	return idea, err
}

// Tag operations
func CreateTag(db *sql.DB, tag *models.Tag) error {
	tx, err := db.Begin()
	if err != nil {
		return err
	}
	defer func() {
		if err != nil {
			tx.Rollback()
		}
	}()

	// Verify user exists within the transaction
	query := `SELECT UserID FROM Users WHERE UserID = $1`
	var userID int
	err = tx.QueryRow(query, tag.UserID).Scan(&userID)
	if err == sql.ErrNoRows {
		return errors.New("user not found")
	} else if err != nil {
		return err
	}

	// Check if tag name already exists for this user
	query = `SELECT TagID FROM Tags WHERE UserID = $1 AND Name = $2`
	var existingTagID int
	err = tx.QueryRow(query, tag.UserID, tag.Name).Scan(&existingTagID)
	if err != sql.ErrNoRows {
		if err == nil {
			return errors.New("tag name already exists for this user")
		}
		return err
	}

	// Create the tag
	query = `
		INSERT INTO Tags (UserID, Name)
		VALUES ($1, $2)
		RETURNING TagID`
	err = tx.QueryRow(query, tag.UserID, tag.Name).Scan(&tag.TagID)
	if err != nil {
		return err
	}

	return tx.Commit()
}

func AddTagToItem(db *sql.DB, itemTag *models.ItemTag) error {
	query := `INSERT INTO ItemTags (ItemID, TagID) VALUES ($1, $2)`
	_, err := db.Exec(query, itemTag.ItemID, itemTag.TagID)
	return err
}

// GetItemsByTag retrieves all items with a specific tag
func GetItemsByTag(db *sql.DB, tagID int) ([]models.Item, error) {
	var items []models.Item
	query := `
		SELECT i.ItemID, i.UserID, i.Type, i.Timestamp
		FROM Items i
		JOIN ItemTags it ON i.ItemID = it.ItemID
		WHERE it.TagID = $1`

	rows, err := db.Query(query, tagID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	for rows.Next() {
		var item models.Item
		err := rows.Scan(&item.ItemID, &item.UserID, &item.Type, &item.Timestamp)
		if err != nil {
			return nil, err
		}
		items = append(items, item)
	}

	return items, nil
}
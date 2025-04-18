package models

import "time"

type User struct {
	UserID       int    `json:"user_id"`
	Username     string `json:"username"`
	Email        string `json:"email"`
	PasswordHash string `json:"password_hash"`
}

type Item struct {
	ItemID    int       `json:"item_id"`
	UserID    int       `json:"user_id"`
	Type      string    `json:"type"`
	Timestamp time.Time `json:"timestamp"`
}

type Idea struct {
	ItemID  int    `json:"item_id"`
	Content string `json:"content"`
}

type Bookmark struct {
	ItemID      int    `json:"item_id"`
	URL         string `json:"url"`
	Title       string `json:"title"`
	Description string `json:"description"`
	Source      string `json:"source"`
	Content     string `json:"content"`
}

type Contact struct {
	ItemID int    `json:"item_id"`
	Name   string `json:"name"`
	Email  string `json:"email"`
	Notes  string `json:"notes"`
}

type Document struct {
	ItemID  int    `json:"item_id"`
	Title   string `json:"title"`
	Content string `json:"content"`
}

type Tag struct {
	TagID  int    `json:"tag_id"`
	UserID int    `json:"user_id"`
	Name   string `json:"name"`
}

type ItemTag struct {
	ItemID int `json:"item_id"`
	TagID  int `json:"tag_id"`
}

type ChatSession struct {
	SessionID int       `json:"session_id"`
	UserID    int       `json:"user_id"`
	ItemID    *int      `json:"item_id"`
	StartTime time.Time `json:"start_time"`
}

type ChatMessage struct {
	MessageID int       `json:"message_id"`
	SessionID int       `json:"session_id"`
	Timestamp time.Time `json:"timestamp"`
	Sender    string    `json:"sender"`
	Content   string    `json:"content"`
}
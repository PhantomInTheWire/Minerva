package main

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"github.com/fatih/color"
	"github.com/spf13/cobra"
)

const baseURL = "http://localhost:8080"

var rootCmd = &cobra.Command{
	Use:   "supermemory-cli",
	Short: "CLI tool for testing Supermemory API endpoints",
}

var createUserCmd = &cobra.Command{
	Use:   "create-user",
	Short: "Create a new user",
	Run: func(cmd *cobra.Command, args []string) {
		username, _ := cmd.Flags().GetString("username")
		email, _ := cmd.Flags().GetString("email")
		password, _ := cmd.Flags().GetString("password")

		// Hash the password using SHA-256
		hasher := sha256.New()
		hasher.Write([]byte(password))
		hashedPassword := hex.EncodeToString(hasher.Sum(nil))

		payload := map[string]string{
			"username":     username,
			"email":        email,
			"passwordHash": hashedPassword,
		}

		makeRequest("POST", "/users", payload)
	},
}

var getUserCmd = &cobra.Command{
	Use:   "get-user",
	Short: "Get user by ID",
	Run: func(cmd *cobra.Command, args []string) {
		id, _ := cmd.Flags().GetInt("id")
		makeRequest("GET", fmt.Sprintf("/users/%d", id), nil)
	},
}

var createIdeaCmd = &cobra.Command{
	Use:   "create-idea",
	Short: "Create a new idea",
	Run: func(cmd *cobra.Command, args []string) {
		userID, _ := cmd.Flags().GetInt("user-id")
		content, _ := cmd.Flags().GetString("content")

		payload := map[string]string{
			"content": content,
		}

		makeRequest("POST", fmt.Sprintf("/users/%d/ideas", userID), payload)
	},
}

var getIdeaCmd = &cobra.Command{
	Use:   "get-idea",
	Short: "Get idea by ID",
	Run: func(cmd *cobra.Command, args []string) {
		id, _ := cmd.Flags().GetInt("id")
		makeRequest("GET", fmt.Sprintf("/ideas/%d", id), nil)
	},
}

var createTagCmd = &cobra.Command{
	Use:   "create-tag",
	Short: "Create a new tag",
	Run: func(cmd *cobra.Command, args []string) {
		userID, _ := cmd.Flags().GetInt("user-id")
		name, _ := cmd.Flags().GetString("name")

		payload := map[string]interface{}{
			"userID": userID,
			"name":   name,
		}

		makeRequest("POST", "/tags", payload)
	},
}

var addTagToItemCmd = &cobra.Command{
	Use:   "add-tag",
	Short: "Add tag to an item",
	Run: func(cmd *cobra.Command, args []string) {
		itemID, _ := cmd.Flags().GetInt("item-id")
		tagID, _ := cmd.Flags().GetInt("tag-id")

		payload := map[string]interface{}{
			"itemID": itemID,
			"tagID":  tagID,
		}

		makeRequest("POST", "/item-tags", payload)
	},
}

var getItemsByTagCmd = &cobra.Command{
	Use:   "get-items-by-tag",
	Short: "Get items by tag ID",
	Run: func(cmd *cobra.Command, args []string) {
		tagID, _ := cmd.Flags().GetInt("tag-id")
		makeRequest("GET", fmt.Sprintf("/tags/%d/items", tagID), nil)
	},
}

func makeRequest(method, endpoint string, payload interface{}) {
	url := baseURL + endpoint
	var req *http.Request
	var err error

	if payload != nil {
		jsonData, _ := json.Marshal(payload)
		req, err = http.NewRequest(method, url, bytes.NewBuffer(jsonData))
	} else {
		req, err = http.NewRequest(method, url, nil)
	}

	if err != nil {
		color.Red("Error creating request: %v", err)
		return
	}

	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		color.Red("Error making request: %v", err)
		return
	}
	defer resp.Body.Close()

	body, _ := ioutil.ReadAll(resp.Body)

	if resp.StatusCode >= 200 && resp.StatusCode < 300 {
		color.Green("Success! Status: %s", resp.Status)
		var prettyJSON bytes.Buffer
		json.Indent(&prettyJSON, body, "", "  ")
		fmt.Println(prettyJSON.String())
	} else {
		color.Red("Error! Status: %s\nResponse: %s", resp.Status, string(body))
	}
}

func init() {
	createUserCmd.Flags().String("username", "", "Username for the new user")
	createUserCmd.Flags().String("email", "", "Email for the new user")
	createUserCmd.Flags().String("password", "", "Password for the new user")
	createUserCmd.MarkFlagRequired("username")
	createUserCmd.MarkFlagRequired("email")
	createUserCmd.MarkFlagRequired("password")

	getUserCmd.Flags().Int("id", 0, "User ID")
	getUserCmd.MarkFlagRequired("id")

	createIdeaCmd.Flags().Int("user-id", 0, "User ID")
	createIdeaCmd.Flags().String("content", "", "Idea content")
	createIdeaCmd.MarkFlagRequired("user-id")
	createIdeaCmd.MarkFlagRequired("content")

	getIdeaCmd.Flags().Int("id", 0, "Idea ID")
	getIdeaCmd.MarkFlagRequired("id")

	createTagCmd.Flags().Int("user-id", 0, "User ID")
	createTagCmd.Flags().String("name", "", "Tag name")
	createTagCmd.MarkFlagRequired("user-id")
	createTagCmd.MarkFlagRequired("name")

	addTagToItemCmd.Flags().Int("item-id", 0, "Item ID")
	addTagToItemCmd.Flags().Int("tag-id", 0, "Tag ID")
	addTagToItemCmd.MarkFlagRequired("item-id")
	addTagToItemCmd.MarkFlagRequired("tag-id")

	getItemsByTagCmd.Flags().Int("tag-id", 0, "Tag ID")
	getItemsByTagCmd.MarkFlagRequired("tag-id")

	rootCmd.AddCommand(createUserCmd)
	rootCmd.AddCommand(getUserCmd)
	rootCmd.AddCommand(createIdeaCmd)
	rootCmd.AddCommand(getIdeaCmd)
	rootCmd.AddCommand(createTagCmd)
	rootCmd.AddCommand(addTagToItemCmd)
	rootCmd.AddCommand(getItemsByTagCmd)
}

func main() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
// Package docs Code generated by swaggo/swag. DO NOT EDIT
package docs

import "github.com/swaggo/swag"

const docTemplate = `{
    "schemes": {{ marshal .Schemes }},
    "swagger": "2.0",
    "info": {
        "description": "{{escape .Description}}",
        "title": "{{.Title}}",
        "contact": {},
        "version": "{{.Version}}"
    },
    "host": "{{.Host}}",
    "basePath": "{{.BasePath}}",
    "paths": {
        "/ideas/{id}": {
            "get": {
                "description": "Get an idea's information by its ID.",
                "produces": [
                    "application/json"
                ],
                "summary": "Get an idea by ID",
                "parameters": [
                    {
                        "type": "integer",
                        "description": "Idea ID",
                        "name": "id",
                        "in": "path",
                        "required": true
                    }
                ],
                "responses": {
                    "200": {
                        "description": "OK",
                        "schema": {
                            "$ref": "#/definitions/models.Idea"
                        }
                    },
                    "400": {
                        "description": "Bad Request",
                        "schema": {
                            "$ref": "#/definitions/handlers.ErrorResponse"
                        }
                    },
                    "404": {
                        "description": "Not Found",
                        "schema": {
                            "$ref": "#/definitions/handlers.ErrorResponse"
                        }
                    }
                }
            }
        },
        "/item-tags": {
            "post": {
                "description": "Associate an existing tag with an existing item.",
                "consumes": [
                    "application/json"
                ],
                "produces": [
                    "application/json"
                ],
                "summary": "Add a tag to an item",
                "parameters": [
                    {
                        "description": "ItemTag object to be created",
                        "name": "itemTag",
                        "in": "body",
                        "required": true,
                        "schema": {
                            "$ref": "#/definitions/models.ItemTag"
                        }
                    }
                ],
                "responses": {
                    "201": {
                        "description": "Created",
                        "schema": {
                            "$ref": "#/definitions/models.ItemTag"
                        }
                    },
                    "400": {
                        "description": "Bad Request",
                        "schema": {
                            "$ref": "#/definitions/handlers.ErrorResponse"
                        }
                    },
                    "500": {
                        "description": "Internal Server Error",
                        "schema": {
                            "$ref": "#/definitions/handlers.ErrorResponse"
                        }
                    }
                }
            }
        },
        "/tags": {
            "post": {
                "description": "Create a new tag with the provided details.",
                "consumes": [
                    "application/json"
                ],
                "produces": [
                    "application/json"
                ],
                "summary": "Create a new tag",
                "parameters": [
                    {
                        "description": "Tag object to be created",
                        "name": "tag",
                        "in": "body",
                        "required": true,
                        "schema": {
                            "$ref": "#/definitions/models.Tag"
                        }
                    }
                ],
                "responses": {
                    "201": {
                        "description": "Created",
                        "schema": {
                            "$ref": "#/definitions/models.Tag"
                        }
                    },
                    "400": {
                        "description": "Bad Request",
                        "schema": {
                            "$ref": "#/definitions/handlers.ErrorResponse"
                        }
                    },
                    "404": {
                        "description": "Not Found",
                        "schema": {
                            "$ref": "#/definitions/handlers.ErrorResponse"
                        }
                    },
                    "500": {
                        "description": "Internal Server Error",
                        "schema": {
                            "$ref": "#/definitions/handlers.ErrorResponse"
                        }
                    }
                }
            }
        },
        "/tags/{tagId}/items": {
            "get": {
                "description": "Get all items associated with a specific tag ID.",
                "produces": [
                    "application/json"
                ],
                "summary": "Get items by tag ID",
                "parameters": [
                    {
                        "type": "integer",
                        "description": "Tag ID",
                        "name": "tagId",
                        "in": "path",
                        "required": true
                    }
                ],
                "responses": {
                    "200": {
                        "description": "OK",
                        "schema": {
                            "type": "array",
                            "items": {
                                "$ref": "#/definitions/models.Item"
                            }
                        }
                    },
                    "400": {
                        "description": "Bad Request",
                        "schema": {
                            "$ref": "#/definitions/handlers.ErrorResponse"
                        }
                    },
                    "500": {
                        "description": "Internal Server Error",
                        "schema": {
                            "$ref": "#/definitions/handlers.ErrorResponse"
                        }
                    }
                }
            }
        },
        "/users": {
            "post": {
                "description": "Create a new user with the provided username, email, and password.",
                "consumes": [
                    "application/json"
                ],
                "produces": [
                    "application/json"
                ],
                "summary": "Create a new user",
                "parameters": [
                    {
                        "description": "User object to be created",
                        "name": "user",
                        "in": "body",
                        "required": true,
                        "schema": {
                            "$ref": "#/definitions/handlers.CreateUserRequest"
                        }
                    }
                ],
                "responses": {
                    "201": {
                        "description": "Created",
                        "schema": {
                            "$ref": "#/definitions/models.User"
                        }
                    },
                    "400": {
                        "description": "Bad Request",
                        "schema": {
                            "$ref": "#/definitions/handlers.ErrorResponse"
                        }
                    },
                    "500": {
                        "description": "Internal Server Error",
                        "schema": {
                            "$ref": "#/definitions/handlers.ErrorResponse"
                        }
                    }
                }
            }
        },
        "/users/{id}": {
            "get": {
                "description": "Get a user's information by their ID.",
                "produces": [
                    "application/json"
                ],
                "summary": "Get a user by ID",
                "parameters": [
                    {
                        "type": "integer",
                        "description": "User ID",
                        "name": "id",
                        "in": "path",
                        "required": true
                    }
                ],
                "responses": {
                    "200": {
                        "description": "OK",
                        "schema": {
                            "$ref": "#/definitions/models.User"
                        }
                    },
                    "400": {
                        "description": "Bad Request",
                        "schema": {
                            "$ref": "#/definitions/handlers.ErrorResponse"
                        }
                    },
                    "404": {
                        "description": "Not Found",
                        "schema": {
                            "$ref": "#/definitions/handlers.ErrorResponse"
                        }
                    }
                }
            }
        },
        "/users/{userId}/ideas": {
            "post": {
                "description": "Create a new idea associated with a specific user ID.",
                "consumes": [
                    "application/json"
                ],
                "produces": [
                    "application/json"
                ],
                "summary": "Create a new idea for a user",
                "parameters": [
                    {
                        "type": "integer",
                        "description": "User ID",
                        "name": "userId",
                        "in": "path",
                        "required": true
                    },
                    {
                        "description": "Idea object to be created",
                        "name": "idea",
                        "in": "body",
                        "required": true,
                        "schema": {
                            "$ref": "#/definitions/models.Idea"
                        }
                    }
                ],
                "responses": {
                    "201": {
                        "description": "Created",
                        "schema": {
                            "$ref": "#/definitions/models.Idea"
                        }
                    },
                    "400": {
                        "description": "Bad Request",
                        "schema": {
                            "$ref": "#/definitions/handlers.ErrorResponse"
                        }
                    },
                    "500": {
                        "description": "Internal Server Error",
                        "schema": {
                            "$ref": "#/definitions/handlers.ErrorResponse"
                        }
                    }
                }
            }
        }
    },
    "definitions": {
        "handlers.CreateUserRequest": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string"
                },
                "password": {
                    "type": "string"
                },
                "username": {
                    "type": "string"
                }
            }
        },
        "handlers.ErrorResponse": {
            "type": "object",
            "properties": {
                "error": {
                    "type": "string"
                }
            }
        },
        "models.Idea": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string"
                },
                "item_id": {
                    "type": "integer"
                }
            }
        },
        "models.Item": {
            "type": "object",
            "properties": {
                "item_id": {
                    "type": "integer"
                },
                "timestamp": {
                    "type": "string"
                },
                "type": {
                    "type": "string"
                },
                "user_id": {
                    "type": "integer"
                }
            }
        },
        "models.ItemTag": {
            "type": "object",
            "properties": {
                "item_id": {
                    "type": "integer"
                },
                "tag_id": {
                    "type": "integer"
                }
            }
        },
        "models.Tag": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string"
                },
                "tag_id": {
                    "type": "integer"
                },
                "user_id": {
                    "type": "integer"
                }
            }
        },
        "models.User": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string"
                },
                "password_hash": {
                    "type": "string"
                },
                "user_id": {
                    "type": "integer"
                },
                "username": {
                    "type": "string"
                }
            }
        }
    }
}`

// SwaggerInfo holds exported Swagger Info so clients can modify it
var SwaggerInfo = &swag.Spec{
	Version:          "1.0",
	Host:             "localhost:8080",
	BasePath:         "/",
	Schemes:          []string{},
	Title:            "Supermemory API",
	Description:      "This is the API for the Supermemory application.",
	InfoInstanceName: "swagger",
	SwaggerTemplate:  docTemplate,
	LeftDelim:        "{{",
	RightDelim:       "}}",
}

func init() {
	swag.Register(SwaggerInfo.InstanceName(), SwaggerInfo)
}

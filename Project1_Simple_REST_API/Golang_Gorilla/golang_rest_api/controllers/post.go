package controllers

import (
	"fmt"
	"golang_restful_api/models"
	"golang_restful_api/utils"
	"net/http"
)

// Create handles POST requests to add new users
func (a *Users) Create(w http.ResponseWriter, r *http.Request) {
	// fetch the user from the context
	fmt.Println("Inside Create")
	acc := r.Context().Value(KeyUser{}).(*models.User)
	err := a.us.CreateUser(acc)
	if err != nil {
		a.l.Println("[ERROR] Something went wrong with user creation", err)
		w.WriteHeader(http.StatusBadRequest)
		utils.Respond(w, &GenericError{Message: "Something went wrong with user creation"})
		return
	}
	w.WriteHeader(http.StatusCreated)
	a.l.Printf("[DEBUG] Inserting user: %#v\n", acc)
}

// Create handles POST requests to add new todos
func (t *Todos) Create(w http.ResponseWriter, r *http.Request) {
	// fetch the user from the context
	todo := r.Context().Value(KeyTodo{}).(*models.Todo)
	// Get the user_id from JWT token and check if that user exists in database
	acc, err := t.getTokenAndUser(w, r)
	todo.UserID = acc.ID
	err = t.ts.AddTodo(todo)
	if err != nil {
		t.l.Println("[ERROR] Something went wrong with todo creation", err)
		w.WriteHeader(http.StatusBadRequest)
		utils.Respond(w, &GenericError{Message: "Something went wrong with todo creation"})
		return
	}
	w.WriteHeader(http.StatusCreated)
	t.l.Printf("[DEBUG] Inserting todo: %#v\n", todo)
	// TODO: return created data
}

package main

import (
	"log"
	"net/http"

	"github.com/identitysec/identity-api-gateway/internal/router"
)

func main() {
	r := router.New()
	log.Println("identity-api-gateway listening on :8080")
	log.Fatal(http.ListenAndServe(":8080", r))
}

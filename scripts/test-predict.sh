#!/usr/bin/env bash
set -e

printf "Should be spam\n"
curl -s -X POST http://localhost:8080/predict -H "Content-Type: application/json" -d '{"subject":"free prize","email_to":"a@b.com","email_from":"c@d.com","message":"click now"}'

printf "\n\nShould be ham\n"
curl -s -X POST http://localhost:8080/predict -H "Content-Type: application/json" -d '{"subject":"follow up","email_to":"a@b.com","email_from":"c@d.com","message":"This is a quick note to follow up on our previous chat."}'
printf "\n"


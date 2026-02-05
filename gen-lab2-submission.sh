#!/usr/bin/env bash
set -e

OUTPUT=lab2-submission.txt

printf "/health result:\n" > $OUTPUT
curl -fs http://localhost:8080/health >> $OUTPUT

printf "\n\n/hello result:\n" >> $OUTPUT
curl -fs http://localhost:8080/hello >> $OUTPUT

printf "\ncompose logs:\n" >> $OUTPUT
docker compose logs api >> $OUTPUT


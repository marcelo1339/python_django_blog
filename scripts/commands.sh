#!/bin/sh

# O shell vai encerrar a execução do script quando um comando falhar
set -e

wait_psql.sh
collectstatic.sh
migrate.sh
runserver.sh
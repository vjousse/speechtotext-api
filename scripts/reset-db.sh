dropdb -U postgres speechtotext_api_dev
createdb -U postgres speechtotext_api_dev
rm -rf migrations/*
aerich init-db

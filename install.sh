#! /bin/bash
mkdir data
echo
echo ">>> build -> postgresql"

sudo docker run --name=pg --rm\
       -e POSTGRES_PASSWORD=postgrespassword \
       -v ./data:/var/lib/postgresql/data \
       -v ./sql/spider.sql:/docker-entrypoint-initdb.d/spider.sql \
       -d -p 5432:5432 postgres:latest

echo
echo ">>> build -> graphql-engine"

sudo docker run --name=ge --net=host -d -p 8080:8080 --rm\
       -e HASURA_GRAPHQL_DATABASE_URL=postgres://postgres:postgrespassword@localhost:5432/postgres \
       -e HASURA_GRAPHQL_ENABLE_CONSOLE=true \
       -e HASURA_GRAPHQL_DEV_MODE=false \
       hasura/graphql-engine:latest 

echo
echo ">>> build -> icejs"
cd ./spider-displayer
echo "如果不需要build 请忽略"
# sudo yarn && yarn build
cd ..

echo
echo ">>> build -> fastapi"
sudo docker run -d --name fa -p 8081:80 --rm\
       -v ./app:/app \
       tiangolo/uvicorn-gunicorn-fastapi:latest

echo
echo "如果需要，请定制域名，否则只能本机访问"
echo ">>> build -> nginx"
sudo docker run -d -p 0.0.0.0:80:80 --name ng --rm\
  --volume ./spider-displayer/build:/usr/share/nginx/html \
  nginx:latest
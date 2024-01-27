# fampaybackendassignemt
# Installation
1. Build a Docker Image
```bash
docker build -t youtubeapi .
```
2. Run the image for running docker container
```bash
docker-compose up -d
```
# APIs
##### A GET API Which Returns The Stored Video Data In A Paginated Response Sorted In Descending Order Of Published Datetime.
##### number of results per page are 20
Query parameter page=page_number
```
127.0.0.1:8000/api/view?page=1
```
##### A Basic Search API To Search The Stored Videos Using Their Title And Description.
Query parameter q=searchQuery
```
127.0.0.1:8000/api/search?q=diljit
```
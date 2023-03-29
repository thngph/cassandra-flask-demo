# Cassandra-Flask Demo
This repository contains a demo for a Cassandra database in a Docker environment. The database is set up with three nodes and a replication factor of three, ensuring that the service remains available as long as at least one node is up.

The demo includes a Flask server that provides access to the data. The data is divided into two keyspaces, one for videos and one for comments. You can use the server to add new video names, add comments to videos, and delete comments.

<p float="left" align="middle">
<img src="https://user-images.githubusercontent.com/67597758/228414776-08abde69-ff15-4fb7-a986-8a516bbcfe81.png" height="100">
<img src="https://user-images.githubusercontent.com/67597758/228415264-3b5104a8-e0e0-4682-83a5-00a371b06196.png" height="100">
<img src="https://user-images.githubusercontent.com/67597758/228415401-facd849e-dcc7-4ca8-9b45-d901c4e594a4.png" height="100">
</p>

## Requirements
To run this demo, you will need:

- Docker
- Docker Compose

## Getting Started
To get started, follow these steps:

- Clone this repository to your local machine.
- Navigate to the root directory of the repository.
- Run `docker-compose up` (or `docker-compose up -d` to run in detached mode) to start the Docker containers for Cassandra and the Flask server.
- Wait for the containers to start up. This may take a few minutes.
- Access the Flask server by navigating to http://localhost:5000 in your web browser.
## Usage
Once you have the Flask server running, you can use it to add new video names, add comments to videos, and delete comments.

## Contributing
If you find a bug or have a feature request, please open an issue in this repository. Pull requests are welcome.
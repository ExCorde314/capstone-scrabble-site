# Capstone Scrabble

This project is for a simple django site that takes a scrabble board and a hand and gives you the best move to make on the board. This app has a single json end point that will take the board and a hand and return the best moves to make.

## Digital Ocean

To run this application on Digital Ocean, run clone this repository in the home directory and run this command:

`docker-compose -f docker-compose.production.yml up -d`

To stop the application, run the following command:

`docker-compose down`

# Capstone Scrabble Tests

1. Add a command to the tests.txt file -> only add the http that needs to be sent out
2. Add the expected output to answers.txt
  - Please sort the answer by the key name

Note: the actual website is tested (scrabblicious.com)



# TODO

1. Scoring the words is currently different -> change to our rules
2. If the word suggested has no connections && is not the first move -> return no solutions
  - look for other less optimal solutions which might be correct
3. Check for connectivity
4. Check for word extension
5. Blank tiles to test -> '?' -> blank tiles on board should be errors and in hand should create words
6. Bingo words -> check score with valid board
7. Creates disconnected words sometimes
8. Website dies if too many requests are made too fast!!

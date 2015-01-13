hwaetbot
========

Twitter bot that generates a new riddle from the word hoard in the Anglo-Saxon poetic style every hour. 

Drawing on the riddles found in the Exeter Book, uses a Markov model with bigrams to generate novel sentences until 140 character limit is reached. Checks ensure unique tweets and that contain no full sentences from the original text.

Code is deployed to Heroku, and uses Heroku Scheduler to run hwaetbot/run.py on an hourly basis. 

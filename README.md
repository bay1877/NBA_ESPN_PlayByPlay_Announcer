# NBA ESPN Play-By-Play Announcer

- required packages
    - pip install gTTS
    - pip install beautifulsoup4
- To run via command line:
    - python run.py [link to ESPN game's play-by-play] [current game quarter]
    
Reads the user new plays as they are received by the url request.
Automatically detects:
- New Plays
- New quarters

Note: Up to the last 15 plays will be read when starting. After that, plays are read as they come in through the request.


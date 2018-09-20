# Botany18 PyCon UK competition
Those are the bots I created for the Botany18 PyCon tournament organized by [@inglesp](https://twitter.com/inglesp?lang=en)

The comments have been added later for clarity. Results for the bots are available [here](http://botany18.pyconuk.org)

For more information of the tournament, see on the [GitHub for Botany](https://github.com/inglesp/botany)

For the names of the Bots, they come from French comic [Le Génie des Alpages](https://fr.wikipedia.org/wiki/Le_Génie_des_alpages) [in english](https://en.wikipedia.org/wiki/Le_Génie_des_alpages) :
- [Athanase](https://fr.wikipedia.org/wiki/Personnages_du_Génie_des_alpages#Athanase_Percevalve): he is the shepherd, rather placid and always wear a beret. He has among others an infinite collection of pullovers and sweaters all more delirious than each other. (directly translated from Wikipedia in French).
- [Romuald](https://fr.wikipedia.org/wiki/Personnages_du_Génie_des_alpages#Romuald): he is a black ram that is practice is the main character from the comic. He claims to be the leader of the flock, but this flock is not one to be lead. (very approximate summary from Wikipedia)

## Athanase serie

This is the logic that was successfull at the beginning of the tournament and relatively simple. Code was (will be) edited to add comments and select better variable names.

### Athanase (athanase.py)
The page for Athanase is [available on the Botany18 server](http://botany18.pyconuk.org/bots/133/) and you can [start play against him](http://botany18.pyconuk.org/play/human/133/) or [play against him letting him start](http://botany18.pyconuk.org/play/133/human/).

Key idea was to select the play that would be part of the most "line of 4", irrelevant of the player that started complete the line of 4.

The results were ordered using the number move needed to complete the "line of 4", meaning a line with a "remaining 1" was a potentially winning "line of 4" and the number of "line of 4" with the same number of "remaining".

Top result will be selected and a position from then was selected.

It was a pure "Gold fish" strategy, not looking ahead, so could fall into obvious traps like allowing the opponent to access a "line of 4" that only need 1 to be completed: [athanase will fall for this trap set up by human player 'X'](http://botany18.pyconuk.org/play/human/133/?moves=3233225655663252263663505000001111).

### athanase_no_traps.py
The page for Athanase "No traps" is [available on the Botany18 server](http://botany18.pyconuk.org/bots/164/) and you can [start play against him](http://botany18.pyconuk.org/play/human/164/) or [play against him letting him start](http://botany18.pyconuk.org/play/164/human/).

To avoid falling into 'traps', an additional search was needed, as we were not looking at "line_of_4" accesible during this turn, but at the "lines of 4" that our move could give access to.

The move that could fall into a trap would be taken out of the moves to select randomly from.

This filtering is done twice, once on the move that have been selected, but if no move is left after the filtering, you redo the filtering but this time out of all available moves.

Once again traps were selected irrelevant to the player ('X' or 'O'). This was to allow preventing your move giving the opportunity to bloc a winning "line_of_4": [athanase_no_traps.py will not fall for this trap set up by human player 'X'](http://botany18.pyconuk.org/play/human/164/?moves=3233225655663252263663505000001111).

### athanase_no_traps_priority.py
The page for Athanase is [available on the Botany18 server](http://botany18.pyconuk.org/bots/257/) and you can [start play against him](http://botany18.pyconuk.org/play/human/257/) or [play against him letting him start](http://botany18.pyconuk.org/play/257/human/).

It turns out all traps are not made equal, at the end of the game you might have to chose to fall into an enemy trap (and lose) or fall into your own trap (and let your opponent prevent you from losing.... for now).

If no move is left at the end of the process as defined previously, you select from any available move but this time only filering out the "deadly move", meaning this traps that would mean you lose the game... 


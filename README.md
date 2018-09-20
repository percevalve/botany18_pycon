# Botany18 PyCon UK competition
Those are the bots I created for the Botany18 PyCon tournament.

The comments have been added later for clarity. Results for the bots are available [here](http://botany18.pyconuk.org)

For credits and more information of the tournament, see on the [GitHub for Botany](https://github.com/inglesp/botany)

## Athanase serie

This is the logic that was successfull at the beginning of the tournament and relatively simple. Code was (will be) edited to add comments and select better variable names.

Key idea was to select the position that was within the most still valid "line of 4", irrelevant of the player that started complete the line of 4.

It was a pure "Gold fish" strategy, not looking ahead, so could fall into obvious traps like allowing the opponent to access a "line of 4" that only need 1 to be completed: this problem was solved with the "no_traps" option.

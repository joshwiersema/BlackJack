# Blackjack

A console blackjack game written in C++. One dealer, as many players as you want at the table, standard 52-card deck, standard rules.

## How it plays

Run it, enter the number of players, and everyone gets dealt in. On your turn you see your hand and its value, then you hit or stand. Dealer reveals after everyone's done and hits until 17. Results print per player. You get asked if you want another round.

The dealer's first card stays hidden until it's their turn, the way it should.

## Rules it follows

- Aces count as 11 when it helps, 1 when 11 would bust you. Handled automatically.
- Face cards are worth 10.
- Bust at 22 or more.
- Dealer hits on anything below 17, stands otherwise.
- Ties are a push.
- The deck reshuffles itself if it runs out mid-round.

## Build

You need a C++ compiler. With g++:

```
g++ -std=c++17 -o blackjack main.cpp BlackjackGame.cpp Card.cpp Deck.cpp Hand.cpp Player.cpp
./blackjack
```

No external dependencies. Standard library only.

## Code layout

| File | What it does |
|------|--------------|
| `main.cpp` | Entry point. Asks for player count, starts the game. |
| `BlackjackGame` | Runs the game loop: deal, turns, dealer play, results, play-again. |
| `Player` | Has a name and a hand. Light wrapper around `Hand`. |
| `Hand` | A collection of cards. Knows its value (with ace logic) and how to print itself. |
| `Deck` | 52 cards, shuffled with `std::mt19937`. Deals one at a time. |
| `Card` | A value (1-13) and a suit. Prints short ("8S") or long ("8 of Spades"). |

Each class sits in its own header/source pair. The split is clean — `Card` doesn't know about `Hand`, `Hand` doesn't know about `Player`, and so on up the chain.

## Possible next steps

- Betting and a chip count
- Splits and double-downs
- Insurance when the dealer shows an ace
- A proper test suite

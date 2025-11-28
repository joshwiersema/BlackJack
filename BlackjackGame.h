// BlackjackGame.h
/**
 * @file BlackjackGame.h
 * @brief Declaration of the BlackjackGame class for multiplayer Blackjack.
 */
#pragma once
#include "Deck.h"
#include "Player.h"
#include <vector>

/**
 * @class BlackjackGame
 * @brief Manages the logic for a multiplayer Blackjack game.
 */
class BlackjackGame {
public:
    /**
     * @brief Constructs a BlackjackGame with a given number of players.
     * @param numPlayers The number of players in the game.
     */
    BlackjackGame(int numPlayers);

    /**
     * @brief Starts and manages the game loop.
     */
    void play();

    /**
     * @brief Handles a single player's turn.
     * @param player The player whose turn it is.
     */
    void playerTurn(Player& player);

    /**
     * @brief Handles the dealer's turn.
     */
    void dealerTurn();

    /**
     * @brief Displays all hands in the game.
     * @param hideDealerFirst Whether to hide the dealer's first card.
     */
    void showHands(bool hideDealerFirst) const;
    
    /**
     * @brief Determines the winner for a given player.
     * @param player The player to check against the dealer.
     * @return A string describing the result.
     */
    std::string determineWinner(const Player& player) const;
private:
    Deck deck;
    Player dealer;
    std::vector<Player> players;
};

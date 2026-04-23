// Deck.h
/**
 * @file Deck.h
 * @brief Declaration of the Deck class for Blackjack.
 */
#pragma once
#include "Card.h"
#include <vector>

/**
 * @class Deck
 * @brief Represents a deck of playing cards for Blackjack.
 */
class Deck {
public:
    /**
     * @brief Constructs a standard 52-card deck and shuffles it.
     */
    Deck();

    /**
     * @brief Shuffles the deck and resets the current index.
     */
    void shuffle();

    /**
     * @brief Deals a card from the deck. Reshuffles if out of cards.
     * @return The next card in the deck.
     */
    Card dealCard();

    /**
     * @brief Checks if the deck is empty.
     * @return True if empty, false otherwise.
     */
    bool isEmpty() const;
    
private:
    std::vector<Card> cards;
    int currentIndex;
};

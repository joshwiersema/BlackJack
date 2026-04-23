// Card.h
/**
 * @file Card.h
 * @brief Declaration of the Card class for Blackjack.
 */
#pragma once
#include <string>

/**
 * @class Card
 * @brief Represents a playing card in Blackjack.
 */
class Card {
public:
    /**
     * @brief The suit of the card.
     */
    enum Suit { Hearts, Diamonds, Clubs, Spades };
    /**
     * @brief Constructs a Card with a value and suit.
     * @param myValue The value of the card (1-13).
     * @param mySuit The suit of the card.
     */
    Card(int myValue, Suit mySuit);
    /**
     * @brief Gets the Blackjack value of the card (face cards are 10, Ace is 1).
     * @return The value as an integer.
     */
    int getValue() const;
    /**
     * @brief Gets a short string representation of the card (e.g., "8S").
     * @return The card as a string.
     */
    std::string toString() const;         // Short format, e.g. "8S"
    /**
     * @brief Gets a full string representation of the card (e.g., "8 of Spades").
     * @return The card as a string.
     */
    std::string toFullString() const;     // Long format, e.g. "8 of Spades"
private:
    int value; // 1-13 (Ace-King)
    Suit suit;
};
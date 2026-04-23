/**
 * @file Card.cpp
 * @brief Implementation of the Card class for Blackjack.
 */
// Card.cpp
#include "Card.h"
#include <sstream>

/**
 * @brief Constructs a Card with a value and suit.
 * @param myValue The value of the card (1-13).
 * @param mySuit The suit of the card.
 */
Card::Card(int myValue, Suit mySuit){
    value = myValue;
    suit = mySuit;
}

/**
 * @brief Gets the Blackjack value of the card (face cards are 10, Ace is 1).
 * @return The value as an integer.
 */
int Card::getValue() const {
    // Face cards are worth 10, Ace is worth 1 or 11 (handled in Hand)
    if (value > 10) return 10;
    return value;
}

/**
 * @brief Gets a short string representation of the card (e.g., "8S").
 * @return The card as a string.
 */
std::string Card::toString() const {
    static const char* valueNames[] = {"", "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"};
    static const char* suitNames[] = {"H", "D", "C", "S"};
    std::ostringstream oss;
    oss << valueNames[value] << suitNames[suit];
    return oss.str();
}

/**
 * @brief Gets a full string representation of the card (e.g., "8 of Spades").
 * @return The card as a string.
 */
std::string Card::toFullString() const {
    static const char* valueNames[] = {"", "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"};
    static const char* suitNames[] = {"Hearts", "Diamonds", "Clubs", "Spades"};
    std::ostringstream oss;
    oss << valueNames[value] << " of " << suitNames[suit];
    return oss.str();
}
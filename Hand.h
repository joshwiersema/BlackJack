// Hand.h
/**
 * @file Hand.h
 * @brief Declaration of the Hand class for Blackjack.
 */
#pragma once
#include "Card.h"
#include <vector>
#include <string>

/**
 * @class Hand
 * @brief Represents a hand of cards in Blackjack.
 */
class Hand {
public:
    /**
     * @brief Adds a card to the hand.
     * @param card The card to add.
     */
    void addCard(const Card& card);
    /**
     * @brief Gets the value of the hand, handling Aces as 1 or 11.
     * @return The hand value as an integer.
     */
    int getValue() const;
    /**
     * @brief Gets a short string representation of the hand.
     * @param hideFirst Whether to hide the first card (for dealer).
     * @return The hand as a string.
     */
    std::string toString(bool hideFirst = false) const;
    /**
     * @brief Gets a full string representation of the hand (e.g., "8 of Spades, King of Hearts").
     * @param hideFirst Whether to hide the first card (for dealer).
     * @return The hand as a string.
     */
    std::string toFullString(bool hideFirst = false) const; // <-- add this
    /**
     * @brief Checks if the hand is bust (value > 21).
     * @return True if bust, false otherwise.
     */
    bool isBust() const;
private:
    std::vector<Card> cards;
};

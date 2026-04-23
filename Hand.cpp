/**
 * @file Hand.cpp
 * @brief Implementation of the Hand class for Blackjack.
 */
// Hand.cpp
#include "Hand.h"
#include <sstream>

/**
 * @brief Adds a card to the hand.
 * @param card The card to add.
 */
void Hand::addCard(const Card& card) {
    cards.push_back(card);
}

/**
 * @brief Gets the value of the hand, handling Aces as 1 or 11.
 * @return The hand value as an integer.
 */
int Hand::getValue() const {
    int total = 0;
    int aces = 0;
    for (const auto& card : cards) {
        int v = card.getValue();
        if (v == 1) aces++;
        total += v;
    }
    // Handle Aces as 11 if it doesn't bust
    while (aces > 0 && total + 10 <= 21) {
        total += 10;
        aces--;
    }
    return total;
}

/**
 * @brief Gets a short string representation of the hand.
 * @param hideFirst Whether to hide the first card (for dealer).
 * @return The hand as a string.
 */
std::string Hand::toString(bool hideFirst) const {
    std::ostringstream oss;
    for (size_t i = 0; i < cards.size(); ++i) {
        if (i == 0 && hideFirst) {
            oss << "??";
        } else {
            oss << cards[i].toString();
        }
        if (i + 1 < cards.size()) oss << " ";
    }
    return oss.str();
}

/**
 * @brief Gets a full string representation of the hand (e.g., "8 of Spades, King of Hearts").
 * @param hideFirst Whether to hide the first card (for dealer).
 * @return The hand as a string.
 */
std::string Hand::toFullString(bool hideFirst) const {
    std::ostringstream oss;
    for (size_t i = 0; i < cards.size(); ++i) {
        if (i == 0 && hideFirst) {
            oss << "??";
        } else {
            oss << cards[i].toFullString();
        }
        if (i + 1 < cards.size()) oss << ", ";
    }
    return oss.str();
}

/**
 * @brief Checks if the hand is bust (value > 21).
 * @return True if bust, false otherwise.
 */
bool Hand::isBust() const {
    return getValue() > 21;
}
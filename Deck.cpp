/**
 * @file Deck.cpp
 * @brief Implementation of the Deck class for Blackjack.
 */
// Deck.cpp
#include "Deck.h"
#include <algorithm>
#include <random>
#include <ctime>

/**
 * @brief Constructs a standard 52-card deck and shuffles it.
 */
Deck::Deck() {
    for (int suit = 0; suit < 4; ++suit) {
        for (int value = 1; value <= 13; ++value) {
            cards.emplace_back(value, static_cast<Card::Suit>(suit));
        }
    }
    shuffle();
    currentIndex = 0;
}

/**
 * @brief Shuffles the deck and resets the current index.
 */
void Deck::shuffle() {
    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(cards.begin(), cards.end(), g);
    currentIndex = 0;
}

/**
 * @brief Deals a card from the deck. Reshuffles if out of cards.
 * @return The next card in the deck.
 */
Card Deck::dealCard() {
    if (currentIndex < cards.size())
        return cards[currentIndex++];
    else{
        // If we run out of cards, reshuffle the deck
        this->shuffle();
        currentIndex = 0;
        return cards[currentIndex++];
    }
}

/**
 * @brief Checks if the deck is empty.
 * @return True if empty, false otherwise.
 */
bool Deck::isEmpty() const {
    return currentIndex >= cards.size();
}

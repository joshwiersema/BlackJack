/**
 * @file Player.cpp
 * @brief Implementation of the Player class for Blackjack.
 */
// Player.cpp
#include "Player.h"

/**
 * @brief Default constructor for Player. Sets name to "aPlayer".
 */
Player::Player(){
    name = "aPlayer";
}

/**
 * @brief Constructs a Player with a given name.
 * @param myName The name of the player.
 */
Player::Player(const std::string& myName){
    name = myName;
}

/**
 * @brief Adds a card to the player's hand.
 * @param card The card to add.
 */
void Player::addCard(const Card& card) {
    hand.addCard(card);
}

/**
 * @brief Gets the value of the player's hand.
 * @return The hand value as an integer.
 */
int Player::getHandValue() const {
    return hand.getValue();
}

/**
 * @brief Gets a string representation of the player's hand.
 * @param hideFirst Whether to hide the first card (for dealer).
 * @return The hand as a string.
 */
std::string Player::getHandString(bool hideFirst) const {
    return hand.toFullString(hideFirst); // <-- use the new method
}

/**
 * @brief Checks if the player is bust (hand value > 21).
 * @return True if bust, false otherwise.
 */
bool Player::isBust() const {
    return hand.isBust();
}

/**
 * @brief Gets the player's name.
 * @return The name as a string.
 */
std::string Player::getName() const {
    return name;
}

/**
 * @brief Resets the player's hand to empty.
 */
void Player::resetHand() {
    hand = Hand();
}
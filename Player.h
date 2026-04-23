// Player.h
/**
 * @file Player.h
 * @brief Declaration of the Player class for Blackjack.
 */
#pragma once
#include "Hand.h"
#include <string>

/**
 * @class Player
 * @brief Represents a player in the Blackjack game.
 */
class Player {
public:
    /**
     * @brief Default constructor.
     */
    Player();
    /**
     * @brief Constructs a Player with a given name.
     * @param myName The name of the player.
     */
    Player(const std::string& myName);
    /**
     * @brief Adds a card to the player's hand.
     * @param card The card to add.
     */
    void addCard(const Card& card);
    /**
     * @brief Gets the value of the player's hand.
     * @return The hand value as an integer.
     */
    int getHandValue() const;

    /**
     * @brief Gets a string representation of the player's hand.
     * @param hideFirst Whether to hide the first card (for dealer).
     * @return The hand as a string.
     */
    std::string getHandString(bool hideFirst = false) const;

    /**
     * @brief Checks if the player is bust (hand value > 21).
     * @return True if bust, false otherwise.
     */
    bool isBust() const;

    /**
     * @brief Gets the player's name.
     * @return The name as a string.
     */
    std::string getName() const;

    /**
     * @brief Resets the player's hand to empty.
     */
    void resetHand();
    
private:
    std::string name;
    Hand hand;
};

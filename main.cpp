/**
 * @file main.cpp
 * @brief Entry point for the Blackjack game. Prompts for number of players and starts the game.
 */
// main.cpp
#include "BlackjackGame.h"
#include <iostream>

/**
 * @brief Main function. Prompts user for number of players and starts the game.
 * @return 0 on successful execution.
 */
int main() {
    int numPlayers;
    std::cout << "Enter number of players: ";
    std::cin >> numPlayers;
    BlackjackGame game(numPlayers);
    game.play();
    return 0;
}

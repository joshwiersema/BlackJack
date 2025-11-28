#include "BlackjackGame.h"
#include <iostream>

BlackjackGame::BlackjackGame(int numPlayers) {
    for (int i = 0; i < numPlayers; ++i) {
        players.push_back(Player("Player " + std::to_string(i + 1)));
    }
}

void BlackjackGame::play() {
    char again = 'y';
    while (again == 'y' || again == 'Y') {
        deck.shuffle();
        // Reset all hands
        for (auto& player : players) {
            player.resetHand();
        }
        dealer.resetHand();
        // Initial deal: two cards to each player and dealer
        for (auto& player : players) {
            player.addCard(deck.dealCard());
        }
        dealer.addCard(deck.dealCard());
        for (auto& player : players) {
            player.addCard(deck.dealCard());
        }
        dealer.addCard(deck.dealCard());

        // Show initial hands
        showHands(true);

        // Each player takes their turn
        for (auto& player : players) {
            std::cout << "\n" << player.getName() << "'s turn:" << std::endl;
            playerTurn(player);
        }

        // If at least one player is not bust, dealer plays
        bool anyNotBust = false;
        for (const auto& player : players) {
            if (!player.isBust()) {
                anyNotBust = true;
                break;
            }
        }
        if (anyNotBust) {
            dealerTurn();
        }

        // Show all hands
        showHands(false);

        // Determine results for each player
        for (const auto& player : players) {
            std::cout << player.getName() << ": ";
            std::cout << determineWinner(player) << std::endl;
        }

        std::cout << "Play again? (y/n): ";
        std::cin >> again;
    }
}

void BlackjackGame::playerTurn(Player& player) {
    while (true) {
        std::cout << player.getName() << "'s hand: " << player.getHandString() << " (" << player.getHandValue() << ")\n";
        if (player.isBust()) {
            std::cout << player.getName() << " busts!\n";
            break;
        }
        std::cout << "Hit or stand? (h/s): ";
        char choice;
        std::cin >> choice;
        if (choice == 'h' || choice == 'H') {
            player.addCard(deck.dealCard());
        } else {
            break;
        }
    }
}

void BlackjackGame::dealerTurn() {
    std::cout << "Dealer's turn...\n";
    while (dealer.getHandValue() < 17) {
        dealer.addCard(deck.dealCard());
        std::cout << "Dealer hits: " << dealer.getHandString() << " (" << dealer.getHandValue() << ")\n";
    }
    if (dealer.isBust()) {
        std::cout << "Dealer busts!\n";
    } else {
        std::cout << "Dealer stands: " << dealer.getHandString() << " (" << dealer.getHandValue() << ")\n";
    }
}

void BlackjackGame::showHands(bool hideDealerFirst) const {
    std::cout << "Dealer's hand: " << dealer.getHandString(hideDealerFirst)
              << (hideDealerFirst ? "" : " (" + std::to_string(dealer.getHandValue()) + ")") << "\n";
    for (const auto& player : players) {
        std::cout << player.getName() << "'s hand: " << player.getHandString() << " (" << player.getHandValue() << ")\n";
    }
}

std::string BlackjackGame::determineWinner(const Player& player) const {
    int playerValue = player.getHandValue();
    int dealerValue = dealer.getHandValue();
    if (player.isBust()) {
        return "Dealer wins!";
    } else if (dealer.isBust()) {
        return "You win!";
    } else if (playerValue > dealerValue) {
        return "You win!";
    } else if (playerValue < dealerValue) {
        return "Dealer wins!";
    } else {
        return "Push! (Tie)";
    }
}

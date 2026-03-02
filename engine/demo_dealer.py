# Quick demo file to verify Dealer and engine setup are working correctly
# It builds the tile set, giving 106
# Deals correctly (15, 14, 14, 14)
# Player hand sizes are printed as well as the remaining draw pile count

from dealer import Dealer

def main():
    dealer = Dealer()
    board = dealer.deal_new_round(['Alice', 'Bob', 'Alex', 'Jane'], starting_player_idx=0)

    print("Player Hands: \n")

    print("-------------------------")
    for i in range(len(board.players)):

        player = board.players[i]
        hand_size = len(player.hand)

        print("Player index:", i)
        print("Name:", player.name)
        print("Number of tiles in hand:", hand_size)
        print("Hand Score:", player.get_hand_score())
        print("-------------------------")

    print("Tiles remaining in draw pile:", board.draw_pile.count())
    

if __name__ == "__main__":
    main()

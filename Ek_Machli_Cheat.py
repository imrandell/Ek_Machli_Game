import random
import string

WORDS = ['Machli', 'Pani me gayi', 'Chhapak']

def generate_random_player():
    name = ''.join(random.choice(string.ascii_uppercase) for _ in range(6))
    out = False  # Default value for is_out is False
    return {'player_name': name, "is_out": out}

def announce_winner(players):
    # Print the winner
    print(f"\nCongratulations, {players[0]['player_name']}! You are the winner!")
    return True

def main(min_iteration):
    num_players = int(input("\nEnter the number of players: "))
    
    enter_player_names= input("\nDo you want to enter player names? (1/0): ")
    
    if enter_player_names == "1":
        players = [{'player_name': input(f"\nEnter the name of player {i+1}: "), 'is_out': False} for i in range(num_players)]
    else:
        players = [generate_random_player() for _ in range(num_players)]
        print(f"\nGenerated random player names: {print([player['player_name'] for player in players])}")
    
    play_or_cheat = input("\nDo you want to Play(1) or Cheat(0)? (1/0): ")

    play_game(players,play_or_cheat,min_iteration)

def play_game(players,play_or_cheat,min_iteration):
    round = 0
    right_answer_number = 1
    expected_answer_loop=1
    word_reduction_required=1
    active_player_count = len([player for player in players if not player['is_out']]) 
    fair_play = play_or_cheat=="1"
    if (not fair_play): #cheat
        my_position = int(input('Enter your position (1,2,3...)'))
        your_name = players[my_position-1]['player_name']
        print(f'Your name is {your_name}')

    while active_player_count> 1 and min_iteration>0:
        round+=1
        print (f'\n---------Round = {round}, Active players = {active_player_count}---------')
        min_iteration-=1
       
        for player in players:
            # current_player_index  = next((i for i, p in enumerate(players) if p == player), None)
            # print (current_player_index)
            current_player_name = player['player_name']
            if player["is_out"]: 
                continue
            
            prefix = str(expected_answer_loop)+" " if right_answer_number == 1 else ""#increase fish count

            if (not fair_play): #cheat
                if (current_player_name == your_name):
                    answer = str(right_answer_number)
                    is_wrong="0"
                    print (f"\n{current_player_name}: Your Choice should be {prefix}{WORDS[right_answer_number-1].upper()}.\n")
                    # print (f", answer_loop = {expected_answer_loop}, word_reduction_required = {word_reduction_required}")
                else:
                    is_wrong = input(f"\t{current_player_name}\'s choice shoud be {prefix}{WORDS[right_answer_number-1].upper()}, Is he/she wrong (1/0)?")
                    is_wrong_int = int(is_wrong) if is_wrong.isdigit() else 0
                    if (is_wrong_int<1):
                        answer = str(right_answer_number) #right answer
                    else:
                        answer = str(right_answer_number+1) #wrong answer`
            else: #fair play
                # Prompt the player for their input
                answer = input(f"{current_player_name}, select your choice (1 for '{expected_answer_loop} Machli', 2 for 'Pani me gayi', 3 for 'Chhapak'): ").strip().capitalize()

            # Check if the player's input matches the expected word or its index
            if answer != str(right_answer_number):
                print(f"Oops! {current_player_name} said the wrong word. right answer is {right_answer_number},  {current_player_name} is out!")
                player["is_out"]=True
                active_player_count -=1
                right_answer_number = 1
                expected_answer_loop=1
                word_reduction_required=1
                # current_player_index = [player['player_name'] for player in players].index(current_player_name) 
                # print(f'Start new roun3d with {active_player_count}, player {players[current_player_index+1]['player_name']} to make first call')
            else:
                if (fair_play): #cheat
                    print (f'Right Answer : {prefix}{WORDS[right_answer_number-1].upper()}')      

                if (word_reduction_required>0):
                    word_reduction_required-=1
                
                if (word_reduction_required==0):
                    right_answer_number += 1
                    word_reduction_required = expected_answer_loop

                if (right_answer_number > len(WORDS)):
                    #print (f"Because {answer_number} > {len(WORDS)}, thus reseting answer_number to 1")
                    right_answer_number = 1
                    # Increase round multiplier after each complete cycle of 'Ek Machli', 'Pani me gayi', and 'Chhapak'
                    expected_answer_loop += 1
                    word_reduction_required=expected_answer_loop
                    #print (f"Repeate word {expected_answer_loop} times")
                
                if (active_player_count<=1):
                    break

    announce_winner(players)
    main(100)

if __name__ == "__main__":
    main(100)

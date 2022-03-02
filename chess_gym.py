from chess_class import chess_class
import numpy as np
import copy
class chess_gym():
    def __init__(self):
        self.chess=chess_class()


        self.state=[{}]
        self.action_size=len(self.chess.moves)
        self.observation_size=np.shape(self.chess._observe_board("white"))

    def _random_white_move(self):
        action=self.chess.choose_random_move("white")
        self._take_action("white",action)
    
    def _take_action(self,player,action):
        self.chess._take_move(player,action)
        self.state.append({})
        if player=="black":
            p="white"
        else: p="black"
        self.state[-1]["player"]=p
        self.state[-1]["turn"]=self.state[-2]["turn"]+1
        self.state[-1]["board"]=copy.deepcopy(self.chess.board)
    def reset(self):
        self.chess.setup_board() 
        self.state=[{}]
        self.state[-1]["player"]="white"
        self.state[-1]["turn"]=0
        self.state[-1]["board"]=copy.deepcopy(self.chess.board)
        # the white pieces take random moves
        self._random_white_move()
        observations=self._get_observations()
        return observations

    def _islegal(self, action):
        return self.chess._is_legal(self.state[-1]["player"],action,self.board)
    
    def _get_observations(self):
        return self.chess._observe_board(self.state[-1]["player"])
    def _calculate_reward(self):
        # Calculates the reward for the black player
        if self.game_status=="Black player made an illegal move":
            reward=-1000
        if self.game_status=="White player made an illegal move":
            reward=-1000
        elif self.game_status=="Black player wins by check mate":
            reward=400
        elif self.game_status=="White player wins by check mate":
            reward=-400
        elif self.game_status=="Game ends in a draw":
            reward=4
        else:
            reward=self.state[-1]["turn"]/200# we reward the advancement of the game 
        return reward

    def render(self):
        board=self.chess.board
        flip_board=[]
        for i in range(8):
            flip_board.append(board[7-i])
        print(np.array(flip_board))




    def step(self,action):
        done=False
        if not self.chess._is_legal("black",action,self.chess.board):
            done=True
            reward=-10
            game_status="Black made an illegal move"
            # Has the game already ended?
        if not done:
            done_b,game_status=self.chess._check_game_end("black")
            done=done_b
            if not done_b:
                # Black takes the action with the Neural Net
                self._take_action("black",action)
                # Has black won with this move?
                done_w,game_status=self.chess._check_game_end("white")
                done=done_w
                if not done_w:
                    # White moves a piece at ranom
                    self._random_white_move()
                    done,game_status=self.chess._check_game_end("black")
            self.game_status=game_status # string with the info about the end game win lose or draw

            reward=self._calculate_reward()
                    
        self.game_status=game_status # string with the info about the end game win lose or draw

        terminal=done
        if self.state[-1]["turn"]>=300:
            # if the game exceeds 300 turns it ends automaticaly
            terminal=True
        
        # Get new observations
        observations = self._get_observations()
        # Information is empty dictionary (used to be compatble with OpenAI Gym)
        info = dict()

        
        return (observations, reward, terminal, info)

        




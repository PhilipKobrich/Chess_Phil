import copy
class chess_class():
    def __init__(self):
        self.empty="   " # Definition of the empty square
        self.setup_board() # sets up the board in the start of a game, it also defines which pieces can be played
        self.moves=self.get_moves() # Creates a list of posible 4672 posible moves a player can make in a game
    def get_moves(self):
        moves=[]
        for col in range(8):
            for row in range(8):
                # Queen Moves
                directions=[[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1]]
                for length in range(7):
                    length=length+1
                    for direction in directions:
                        move_dict={}
                        move_dict["start_position"]=[row,col]
                        move_dict["type"]="Queen Move"
                        row_move=direction[0]*length
                        col_move=direction[1]*length
                        move_dict["end_position"]=[row+row_move,col+col_move]
                        move_dict["length"]=length
                        move_dict["direction"]=direction
                        move_dict["promotion"]="None"
                        move_dict["description"]="queen movement in "+str(direction)+" direction with length "+str(length)
                        moves.append(move_dict)
                # Knight Moves
                directions=[[2,1],[2,-1],[-2,1],[-2,-1],[-1,-2],[1,-2],[-1,2],[1,2]]
                for direction in directions:
                    move_dict={}
                    move_dict["start_position"]=[row,col]
                    move_dict["type"]="Knight Move"
                    row_move=direction[0]
                    col_move=direction[1]
                    move_dict["end_position"]=[row+row_move,col+col_move]
                    
                    move_dict["direction"]=direction
                    move_dict["promotion"]="None"
                    move_dict["description"]="knigth movement in "+str(direction)
                    moves.append(move_dict)
                # Promotion
                directions=[-1,0,1]
                promotions=["knight","bishop","rook"]
                for direction in directions:
                    for promotion in promotions:
                        move_dict={}
                        move_dict["start_position"]=[row,col]
                        
                        move_dict["type"]="Pawn Promotion"
                        move_dict["move_col_direction"]=direction
                        move_dict["promotion"]=promotion
                        
                        move_dict["direction"]=direction
                        move_dict["description"]="pawn promotion in "+str(direction)+" direction into a "+promotion
                        moves.append(move_dict)
        return moves
    def setup_board(self):
        self.board=[]
        for i in range(8):
            self.board.append([self.empty]*8)
        
        self.board[0][0]="b_r"
        self.board[0][1]="b_k"
        self.board[0][2]="b_b"
        self.board[0][3]="b_Q"
        self.board[0][4]="b_K"
        self.board[0][5]="b_b"
        self.board[0][6]="b_k"
        self.board[0][7]="b_r"

        self.board[1][0]="b_p"
        self.board[1][1]="b_p"
        self.board[1][2]="b_p"
        self.board[1][3]="b_p"
        self.board[1][4]="b_p"
        self.board[1][5]="b_p"
        self.board[1][6]="b_p"
        self.board[1][7]="b_p"


        self.board[7][0]="w_r"
        self.board[7][1]="w_k"
        self.board[7][2]="w_b"
        self.board[7][3]="w_Q"
        self.board[7][4]="w_K"
        self.board[7][5]="w_b"
        self.board[7][6]="w_k"
        self.board[7][7]="w_r"

        self.board[6][0]="w_p"
        self.board[6][1]="w_p"
        self.board[6][2]="w_p"
        self.board[6][3]="w_p"
        self.board[6][4]="w_p"
        self.board[6][5]="w_p"
        self.board[6][6]="w_p"
        self.board[6][7]="w_p"
        pieces=[]
        for i in range(8):
            for j in range(8):
                piece=self.board[i][j]
                if piece not in pieces:
                    pieces.append(piece)
        self.pieces=pieces

    def _observe_board(self):
        obs=[]
        for i in range(8):
            for j in range(8):
                obs+=[1 if piece=="   " else 0 for piece in self.pieces]

        return obs
    
    def _is_legal_movement(self,player,action,board):
        # player str: "white" or "black"
        # action int: between 0 and 4671, identifiying the move to take
        # Retuns false if the move is illegal

        take_move=True
        move_dict=self.moves[action]
        row=move_dict["start_position"][0]
        col=move_dict["start_position"][1]
        piece=board[row][col]
        piece_type=piece[-1]
        
        if player[0]!=piece[0]:
            # the piece is not of the current player ("w"!="k") or the space is empty (" "!="w" or " "!="k")
            return False,take_move
        #Queen Type Moves
        if move_dict["type"]=="Queen Move":
            # if it is a queen move
            move_direction=move_dict["direction"]
            move_length=move_dict["length"]
            end_position=move_dict["end_position"]
            start_position=move_dict["start_position"]
            
            if self._position_oob(end_position):
                return False,take_move # if the last position is out of bounds return false
            if self._bool_is_player_piece(player,end_position,board):
                # Cant move over your own pieces
                return False,take_move
            if not(self._legal_path(start_position,move_direction,move_length,board)):
                # The current move path intersects with another piece, then the move is illegal
                return False,take_move
            if piece_type=="r":
                # Rook Movements
                if move_direction in [[1,1],[-1,1],[-1,-1],[1,-1]]:
                    return False,take_move # a rook cant move in diagonal
            elif piece_type=="k":
                # Knignt movement
                # None of the queen moves are valid for the knight
                return False,take_move 
            elif piece_type=="b":
                # Bishop move
                if move_direction in [[1,0],[-1,0],[0,-1],[0,1]]:
                    return False,take_move # a bishop cant move in a horizontal or vertical line
                1
            elif piece_type=="Q":
                # Queen Move
                1
            elif piece_type=="K":
                # King Move
                
                # We should check for castleing
                if move_length>1:
                    return False,take_move
            elif piece_type=="p":
                # Pawn Move
                
                if player=="white":
                    if move_direction not in [[-1,-1],[-1,0],[-1,1]]:
                        #white player's pawns only move up
                        return False,take_move
                    # Take a piece
                    if move_direction in [[-1,-1],[-1,1]]:
                        if move_length>1:
                            # the legnth of the move must be 1
                            return False,take_move
                        if not(self._bool_is_piece(end_position,board)):
                            # There has to be a piece in the end position
                            return False,take_move
                    # move the pawn up
                    if move_direction==[-1,0]:
                        take_move=False
                        if self._bool_is_piece(end_position,board):
                            # Cant move over a piece
                            return False,take_move
                        if start_position[0]==6:
                            if move_length>2 or self._bool_is_piece(end_position,board):
                                # first pawn move can be 2 spaces forward when it doesn't take
                                return False,take_move
                        else:
                            if move_length>1 or self._bool_is_piece(end_position,board):
                                # every other move of the pawn cant exeed 2 spaces and it can't take a piece
                                return False,take_move


                elif player=="black":
                    if move_direction not in [[1,-1],[1,0],[1,1]]:
                        #black player's pawns only move down
                        return False,take_move
                    # Take a piece
                    if move_direction in [[1,-1],[1,1]]:
                        if move_length>1:
                            # the legnth of the move must be 1
                            return False,take_move
                        if not(self._bool_is_piece(end_position,board)):
                            # There has to be a piece in the end position
                            return False,take_move
                    # move the pawn down
                    if move_direction==[1,0]:
                        take_move=False
                        if self._bool_is_piece(end_position,board):
                            # Cant move over a piece
                            return False,take_move
                        if start_position[0]==1:
                            if move_length>2 or self._bool_is_piece(end_position,board):
                                # first pawn move can be 2 spaces forward  when the last position is free we already check travel path for pieces
                                return False,take_move
                        else:
                            if move_length>1 or self._bool_is_piece(end_position,board):
                                # every other move of the pawn cant exeed 2 spaces and it can't take a piece
                                return False,take_move
        elif move_dict["type"]=="Knight Move":
            move_direction=move_dict["direction"]
            end_position=move_dict["end_position"]
            if self._position_oob(end_position):
                return False,take_move # if the last position is out of bounds return false
            if self._bool_is_player_piece(player,end_position,board):
                return False,take_move
            if piece_type!="k":
                # only knights can use this move
                return False,take_move
            
        elif move_dict["type"]=="Pawn Promotion":
            return False,False

        return True,take_move
    def _is_legal(self,player,action,board):
        legal,_=self._is_legal_movement(player,action,board)
        
        if legal:
            # We pre make the move on a test board, this board does not get saved. This si to test for check, a move can't put your own king in check
            test_board=self._test_take_move(action)
            # once the movement is legal we check if it cecks the player
            # If the player is not in check and all the other illegalities are resolved, the move is legal and can be performed
            if not(self._bool_check(player,test_board)):
                return True
            else:
                # The players king is in check, the move is illegal
                return False
        else:
            # if the move does not satisfy the pieces resrictions, it is illegal
            return False
    def _bool_is_check_mate_draw(self,player):

        king_found=False
        for row in range(8):
            for col in range(8):
                piece=self.board[row][col]
                if piece==player[0]+"_K":
                    king_found=True
                    break
            if king_found:
                break
        if not king_found:
            print(player+" king not found ¡It was eaten!")
            return True,False
        # checks if the player is in check mate on the start of their turn
        if self._bool_check(player,self.board):
            # if the player is currently in check we see if there are moves that remove the check
            check_mate=True # initilaize the bollean variable as True, if we find a legal move that removes the check we change it to False

        else:
            check_mate=False
        draw=True # initialize the draw as True, if we find a legal move there is no draw
        for action in(range(len(self.moves))):
            legal=self._is_legal(player,action,self.board)
            if legal:
                check_mate=False
                draw=False
                break
        return check_mate,draw

    def _position_oob(self,end_position):
        # Checks if the position resulting of a move is out of bounds, if it is inbounds returns False
        if end_position[0]<0:
            return True
        elif end_position[0]>7:
            return True
        elif end_position[1]<0:
            return True
        elif end_position[1]>7:
            return True
        else: return False
    def _legal_path(self,start_position,move_direction,move_length,board):
        # checks if there are any pieces in the queens movement path
        current_position=copy.deepcopy(start_position)
        for l in range(move_length):
            if l==0:
                # we skip the first step this means we will check travel fron length 1 to final step -1
                continue
            current_position[0]=current_position[0]+move_direction[0]
            current_position[1]=current_position[1]+move_direction[1]
            current_space_piece=board[current_position[0]][current_position[1]]
            if current_space_piece!=self.empty:
                return False
        return True
    def _bool_is_piece(self,position,board):
        # Checks if there is a piece in the checked position
        piece=board[position[0]][position[1]]
        if piece!=self.empty:
            return True
        else: return False
    def _bool_is_player_piece(self,player,position,board):
        # Checks if there is a piece in the checked position
        piece=board[position[0]][position[1]]
        if piece!=self.empty:
            if piece[0]==player[0]:
                return True
        else: return False
    def _bool_check(self,player,board):
        king_found=False
        for row in range(8):
            for col in range(8):
                piece=board[row][col]
                if piece==player[0]+"_K":
                    king_found=True
                    break
            if king_found:
                break
        if not king_found:
            print(player+" king not found ¡It was eaten!")
        
        king_position=[row,col]
        is_check=self._bool_check_threat(player,king_position,board)
        # if is_check: print(player[0]+"_K")
        return is_check
    
    # def _bool_check_mate(self,player):
    #     if self._bool_check(player):
    #         1 asuhd asfadsfí asfasdf as[ 12 3]
            

    def _bool_check_threat(self,player,position,board):
        if player=="white":
            oponent="black"
        else:
            oponent="white"
        
        for i in range(len(self.moves)):
            move=self.moves[i]
            if move["type"]=="Pawn Promotion":
                continue
            legal,threat=self._is_legal_movement(oponent,i,board)
            if move["end_position"]==position and threat and legal:
                return True
        return False
    def _take_move(self,action):
        move=self.moves[action]
        s_pos=move["start_position"]
        piece=self.board[s_pos[0]][s_pos[1]]
        if move["type"]=="Pawn Promotion":
            1
        else:
            e_pos=move["end_position"]
            self.board[e_pos[0]][e_pos[1]]=piece
            self.board[s_pos[0]][s_pos[1]]=self.empty
    def _test_take_move(self,action):
        move=self.moves[action]
        new_board=copy.deepcopy(self.board)
        s_pos=move["start_position"]
        piece=new_board[s_pos[0]][s_pos[1]]
        if move["type"]=="Pawn Promotion":
            1
        else:
            e_pos=move["end_position"]
            new_board[e_pos[0]][e_pos[1]]=piece
            new_board[s_pos[0]][s_pos[1]]=self.empty
        return new_board
    def _check_game_end(self,player):
        done=False
        game_status=player+" moves"
        check_mate,draw=self._bool_is_check_mate_draw(player)
        if check_mate:
            done=True
            draw=False
            if player=="white":
                game_status="Black player wins by check mate"
            elif player=="black":
                game_status="White player wins by check mate"
        elif draw:
            done=True
            game_status="Game ends in a draw"
        return done,game_status
    def moves_end_pos_from_start_pos(self,player,s_pos):
        actions=[]
        end_pos=[]
        for action in range(len(self.moves)):
            move=self.moves[action]
            if move["start_position"]==s_pos:
                legal=self._is_legal(player,action,self.board)
                if legal:
                    actions.append(action)
                    end_pos.append(move["end_position"])
        return actions,end_pos
        
    

    
            

        




        




                
                


                




chess=chess_class()


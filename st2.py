
import streamlit as st
import time 
from chess_class import chess_class
import copy


if "chess" not in st.session_state:
     chess=chess_class()
     st.session_state["chess"]=chess_class()
chess=st.session_state["chess"]
if "board" not in st.session_state:
     st.session_state["board"]=copy.deepcopy(chess.board)
if "selected_piece" not in st.session_state:
     st.session_state["selected_piece"]=[]
if "state" not in st.session_state:
     st.session_state["state"]="select_piece"
if "player" not in st.session_state:
     st.session_state["player"]="white"
player=st.session_state["player"]

done,game_status=chess._check_game_end(player)
if done:
     st.write(game_status)
key=0
columns=st.columns(8)
for col in range(8):
     for row in range(8):
          piece=st.session_state["board"][row][col]
          if piece==st.session_state["chess"].empty:
               st.session_state["board"][row][col]="---"
          piece=st.session_state["board"][row][col]
          if columns[col].button(piece,key=str(key)):
               st.session_state["board"]=copy.deepcopy(chess.board)
               if piece[1]=="x":
                    pos=[row,col]
                    actions=st.session_state["actions"]
                    end_positions=st.session_state["end_positions"]
                    for i in range(len(actions)):
                         if end_positions[i]==pos:
                              break
                    action=actions[i]
                    chess._take_move(action)
                    st.session_state["board"]=copy.deepcopy(chess.board)
                    if player=="white":
                         st.session_state["player"]="black"
                    else:
                         st.session_state["player"]="white"
                    st.experimental_rerun()
               else:

                    
                    actions,end_positions=chess.moves_end_pos_from_start_pos(player,[row,col])
                    if len(actions)==0:
                         st.session_state["selected_piece"]=[]
                         st.session_state["state"]=="select_piece"
                         st.session_state["actions"]=actions
                         st.session_state["end_positions"]=end_positions
                         # st.experimental_rerun()
                    else:
                         for pos in end_positions:
                              piece_=copy.deepcopy(st.session_state["board"][pos[0]][pos[1]])
                              st.session_state["board"][pos[0]][pos[1]]=str(piece_[0])+"x"+str(piece_[2])
                         
                         st.session_state["actions"]=actions
                         st.session_state["end_positions"]=end_positions
                         st.session_state["state"]=="select_move"
                    
                    st.session_state["selected_piece"]=[row,col]
                    
                    # st.session_state["board"][row][col]="XXX"





               st.experimental_rerun()
          key+=1








# key=0
# if st.session_state["state"]=="select_move":
     
#      columns=st.columns(8)
#      st.write("hi")
#      actions,end_positions=chess.moves_end_pos_from_start_pos(player,[6,0])
#      if len(actions)==0:
#           st.session_state["selected_piece"]=[]
#           st.session_state["state"]=="select_piece"
#           st.experimental_rerun()



#      for col in range(8):
#           for row in range(8):
#                piece=chess.board[row][col]
#                if piece==st.session_state["chess"].empty:
#                     piece="___"
#                if [col,row] in end_positions:
#                     piece[1]="x"
#                if columns[col].button(piece,key=str(key)):
#                     # st.session_state["board"][row][col]="xxx"
#                     st.session_state["selected_piece"]=[col,row]
#                     st.session_state["action"]=="select_piece"
#                     st.experimental_rerun()
#                key+=1








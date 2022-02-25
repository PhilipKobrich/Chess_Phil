import streamlit as st
from streamlit import caching
# from streamlit_plotly_events import plotly_events
# import plotly.express as ex
import matplotlib.pyplot as plt
from chess_class import chess_class
import plotly
import time

chess=chess_class()

selection=[]
board=chess.board
# new_board(board)
action="None"
selection=[]
def click_button():
    
    selection=[0,0]
    # st.write(str(selection))
    board[0][0]="---"

st.session_state["status"]="None"
st.session_state["board"]=board
def create_buttons(placeholder,key):

    initialize=True
    # placeholder=st.empty()
    # def _stop():
    #     placeholder.empty()
    #     board_diagram[0][0]="Algo hice"
    #     st.write(str(selection))
    placeholder.empty()
    with placeholder.container():
        if initialize:
            columns=st.columns(8)
            
            for col in range(len(columns)):
                column=columns[col]
                for row in range(8):
                    piece=st.session_state["board"][row][col]
                    if piece==chess.empty:
                        piece="___"
                    if column.button(piece,key=str(key)):
                        # st.session_state["status"]=str(col)+"_"+str(row)
                        st.session_state["status"]=[col,row]
                        st.session_state["board"][row][col]="xxx"
                    
                    key+=1
            initialize=False
        runing=True
        return placeholder


placeholder=st.empty()
key=0
placeholder= create_buttons(placeholder,key)








import json
import time
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from board import Checkers
from constants import INPUT_KEYS
from engine import Engine
from piece import Position


def render_score_board():
    if "checker" in st.session_state:
        checker: Checkers = st.session_state["checker"]
    score_board_container = st.container(key="score_board")
    with score_board_container:
        player_1, player_2 = st.columns(2)
        with player_1:
            st.subheader(":red[Player 1]")
            st.metric("Score", checker.REDS)
            st.metric("Kings", checker.RED_KINGS)
        with player_2:
            st.subheader(":grey[Player 2]")
            st.metric("Score", checker.BLACKS)
            st.metric("Kings", checker.BLACK_KINGS)


def render_board():
    if "checker" in st.session_state:
        checker: Checkers = st.session_state["checker"]
    board_container = st.container(border=True, key="board")
    with board_container:
        checker.display_board()


def refresh():
    if "update" in st.session_state and st.session_state["update"]:
        # once run set update to False
        st.session_state["update"] = False
        st.session_state["counter"] += 1
        st.session_state["turn"] = (
            "Player 1" if st.session_state["counter"] % 2 == 0 else "Player 2"
        )
        st.rerun()


def build_game_console():
    # Initialize checker game and store the state in session state if not in session state
    if "checker" not in st.session_state:
        checker = Checkers()
        engine = Engine()
        st.session_state["checker"] = checker
        if "counter" not in st.session_state:
            st.session_state["counter"] = 0
        if "turn" not in st.session_state:
            st.session_state["turn"] = "Player 1"
        if "positions_1" not in st.session_state:
            st.session_state["positions_1"] = []
        if "positions_2" not in st.session_state:
            st.session_state["positions_2"] = []
        if "engine" not in st.session_state:
            st.session_state["engine"] = engine
    render_score_board()
    render_board()


def build_player_inputs():
    st.info(f"{st.session_state['turn']}`s turn")
    chat_container = st.container(border=True, key="chat", height=350)
    player_1_chat = st.empty()
    with chat_container:
        player_1, player_2 = st.columns(2)
        with player_1:
            record_player_input = st.container(height=250, key="Player1_input")
            player_1_chat = st.chat_input(
                "Enter Json text",
                key="Player1",
                disabled="turn" in st.session_state
                and st.session_state["turn"] == "Player 2",
            )
            if "positions_1" in st.session_state:
                record_player_input.chat_message("player 1").write(
                    st.session_state["positions_1"]
                )
            if player_1_chat:
                positions = json.loads(player_1_chat)
                st.session_state["positions_1"].append(positions)
                apply_move(**positions)
        with player_2:
            print(f"{st.session_state['turn']}`s turn")
            record_player_input_2 = st.container(height=250, key="Engine")
            if "positions_2" in st.session_state:
                record_player_input_2.chat_message("Player 2").write(
                    st.session_state["positions_2"]
                )
            if (
                "engine" in st.session_state
                and "checker" in st.session_state
                and "turn" in st.session_state
                and st.session_state["turn"] == "Player 2"
            ):
                engine = st.session_state["engine"]
                checker: Checkers = st.session_state["checker"]
                time.sleep(6)
                best_move = engine.find_best_move(
                    engine.copy_board(board=checker.board)
                )
                if best_move:
                    best_move_dict = dict(zip(INPUT_KEYS, best_move))
                    print(best_move_dict)
                    st.session_state["positions_2"].append(best_move_dict)
                    apply_move(**best_move_dict)

            #####################
            ### Multi Player ####
            #####################
            # record_player_input_2 = st.container(height=200, key="Player2_input")
            # player_2_chat = st.chat_input(
            #     "Enter Json text",
            #     key="Player2",
            #     disabled="turn" in st.session_state
            #     and st.session_state["turn"] == "Player 1",
            # )
            # if "positions_2" in st.session_state:
            #     record_player_input_2.chat_message("player 2").write(
            #         st.session_state["positions_2"]
            #     )
            # if player_2_chat:
            #     positions = json.loads(player_2_chat)
            #     st.session_state["positions_2"].append(positions)
            #     apply_move(**positions)


def display_winner():
    if "checker" in st.session_state:
        checker: Checkers = st.session_state["checker"]
        winner = checker.winner()
        if winner:
            st.toast(winner)


def apply_move(row, col, new_row, new_col):
    if "checker" in st.session_state:
        checker: Checkers = st.session_state["checker"]
        try:
            checker.move(row, col, new_row, new_col)
            st.session_state["checker"] = checker
        except Exception as e:
            st.error(f"Here is the error - {e}")
        st.session_state["update"] = True
        refresh()
        print(st.session_state["turn"])


def begin_game():
    st.header(":blue[CHECKERS GAME]")
    build_game_console()
    build_player_inputs()
    display_winner()


begin_game()

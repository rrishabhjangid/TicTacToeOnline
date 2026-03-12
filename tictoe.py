import streamlit as st

st.set_page_config(page_title="Multiplayer Tic-Tac-Toe", page_icon="🎮")

# --- 1. SHARED DATABASE (In-Memory) ---
# st.cache_resource keeps this dictionary alive across all user browsers
@st.cache_resource
def get_database():
    return {}

db = get_database()

# --- 2. LOCAL SESSION STATE ---
# Keeps track of who THIS specific browser belongs to
if "my_player" not in st.session_state:
    st.session_state.my_player = None
if "room" not in st.session_state:
    st.session_state.room = None

# --- HELPER FUNCTIONS ---
def check_winner(board):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # Cols
        [0, 4, 8], [2, 4, 6]             # Diagonals
    ]
    for a, b, c in win_conditions:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if "" not in board:
        return "Draw"
    return None

def make_move(i, room_id):
    game = db[room_id]
    if game["board"][i] == "" and game["winner"] is None and game["turn"] == st.session_state.my_player:
        game["board"][i] = st.session_state.my_player
        game["winner"] = check_winner(game["board"])
        # Switch turns
        game["turn"] = "O" if st.session_state.my_player == "X" else "X"

# --- UI & APP FLOW ---
st.title("🌐 Online Multiplayer Tic-Tac-Toe")

# LOBBY: If the user isn't in a room yet
if not st.session_state.room:
    st.markdown("### Join or Create a Room")
    st.write("Share the room name with your friend so they can join you!")
    room_input = st.text_input("Enter a Room Name (e.g., 'secret-room-1')")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Create Room (Play as X)", use_container_width=True):
            if room_input:
                # Initialize the room in the shared database
                db[room_input] = {
                    "board": [""] * 9,
                    "turn": "X",
                    "winner": None,
                    "players": ["X"]
                }
                st.session_state.my_player = "X"
                st.session_state.room = room_input
                st.rerun()

    with col2:
        if st.button("Join Room (Play as O)", use_container_width=True):
            if room_input in db:
                if "O" not in db[room_input]["players"]:
                    db[room_input]["players"].append("O")
                    st.session_state.my_player = "O"
                    st.session_state.room = room_input
                    st.rerun()
                else:
                    st.error("Room is already full!")
            else:
                st.error("Room does not exist. Create it first!")

# GAME BOARD: If the user is inside a room
else:
    room_id = st.session_state.room
    game = db[room_id]

    st.subheader(f"Room: `{room_id}` | You are playing as: **{st.session_state.my_player}**")

    if st.button("Leave Room"):
        st.session_state.room = None
        st.session_state.my_player = None
        st.rerun()

    st.divider()

    # Fragment to auto-refresh only the game board every 2 seconds
    @st.fragment(run_every="2s")
    def render_board():
        # Status messages
        if game["winner"]:
            if game["winner"] == "Draw":
                st.info("🤝 It's a Draw!")
            else:
                st.success(f"🎉 Player {game['winner']} wins!")
        else:
            if game["turn"] == st.session_state.my_player:
                st.write("🟢 **It is your turn!**")
            else:
                st.write("🔴 **Waiting for opponent to move...**")

        # Draw the 3x3 Grid
        cols = st.columns(3)
        for i in range(9):
            with cols[i % 3]:
                # Use a zero-width space if empty so the button renders nicely
                label = game["board"][i] if game["board"][i] != "" else "‎"

                # Disable button if spot is taken, not your turn, or game is over
                is_disabled = (
                    game["board"][i] != "" or
                    game["turn"] != st.session_state.my_player or
                    game["winner"] is not None
                )

                if st.button(label, key=f"cell_{i}", disabled=is_disabled, use_container_width=True):
                    make_move(i, room_id)
                    st.rerun()

    render_board()
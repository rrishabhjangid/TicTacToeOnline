import streamlit as st

# Must be the very first Streamlit command
st.set_page_config(page_title="Premium Tic-Tac-Toe", page_icon="✨", layout="centered")

# --- 0. PREMIUM UI CSS ---
st.markdown("""
    <style>
    /* Gradient Title */
    .premium-title {
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 800;
        font-size: 3rem;
        background: -webkit-linear-gradient(45deg, #FF4B4B, #9B51E0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    
    /* Subtitle centering */
    .premium-subtitle {
        text-align: center;
        color: #888888;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }

    /* Game Board Tiles */
    div[data-testid="stButton"] > button {
        height: 120px;
        font-size: 3.5rem !important;
        font-weight: bold;
        border-radius: 16px;
        border: 2px solid rgba(255, 255, 255, 0.1);
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Hover effect for tiles */
    div[data-testid="stButton"] > button:hover {
        border-color: #9B51E0;
        box-shadow: 0 8px 20px rgba(155, 81, 224, 0.4);
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

# --- 1. SHARED DATABASE (In-Memory) ---
@st.cache_resource
def get_database():
    return {}

db = get_database()

# --- 2. LOCAL SESSION STATE ---
if "my_player" not in st.session_state:
    st.session_state.my_player = None
if "room" not in st.session_state:
    st.session_state.room = None

# --- 3. HELPER FUNCTIONS ---
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
        # Use emojis for a better look
        game["board"][i] = "❌" if st.session_state.my_player == "X" else "⭕"
        game["winner"] = check_winner(game["board"])
        game["turn"] = "O" if st.session_state.my_player == "X" else "X"

# --- 4. UI & APP FLOW ---
st.markdown("<div class='premium-title'>Tic-Tac-Toe Online</div>", unsafe_allow_html=True)
st.markdown("<div class='premium-subtitle'>Play with anyone, anywhere.</div>", unsafe_allow_html=True)

# LOBBY
if not st.session_state.room:
    with st.container(border=True):
        st.markdown("### 🚪 Room Lobby")
        room_input = st.text_input("Enter a Room Code:", placeholder="e.g., retro-gaming-1")
        
        st.write("") # Spacer
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✨ Create Room (Play as ❌)", use_container_width=True):
                if room_input:
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
            if st.button("🤝 Join Room (Play as ⭕)", use_container_width=True):
                if room_input in db:
                    if "O" not in db[room_input]["players"]:
                        db[room_input]["players"].append("O")
                        st.session_state.my_player = "O"
                        st.session_state.room = room_input
                        st.rerun()
                    else:
                        st


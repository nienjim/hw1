import streamlit as st
import random

st.set_page_config(page_title="價值迭代算法 (Value Iteration)", layout="wide")

# Constants
ARROWS = {'UP': '↑', 'DOWN': '↓', 'LEFT': '←', 'RIGHT': '→', 'GOAL': '🎯', 'BLOCK': '⬛'}
DIRECTIONS = ['UP', 'DOWN', 'LEFT', 'RIGHT']

def init_state():
    if 'grid_size' not in st.session_state:
        st.session_state.grid_size = 5
    if 'start' not in st.session_state:
        st.session_state.start = [0, 0]
    if 'end' not in st.session_state:
        st.session_state.end = [4, 4]
    if 'blocks' not in st.session_state:
        st.session_state.blocks = []
    if 'mode' not in st.session_state:
        st.session_state.mode = 'start'
    if 'display' not in st.session_state:
        st.session_state.display = 'random'
    if 'random_policy' not in st.session_state:
        generate_random_policy(5)
    if 'V' not in st.session_state:
        st.session_state.V = None
    if 'policy' not in st.session_state:
        st.session_state.policy = None

def generate_random_policy(size):
    rp = []
    for r in range(size):
        row = []
        for c in range(size):
            row.append(random.choice(DIRECTIONS))
        rp.append(row)
    st.session_state.random_policy = rp

init_state()

def get_next_state(r, c, a, R, C, blocks):
    actions_map = {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}
    dr, dc = actions_map.get(a, (0, 0))
    nr, nc = r + dr, c + dc
    if 0 <= nr < R and 0 <= nc < C and [nr, nc] not in blocks:
        return nr, nc
    return r, c

def run_policy_evaluation(gamma=0.9, epsilon=1e-4):
    R = C = st.session_state.grid_size
    V = [[0.0 for _ in range(C)] for _ in range(R)]
    blocks = st.session_state.blocks
    end = st.session_state.end
    policy = st.session_state.random_policy

    while True:
        delta = 0
        new_V = [[V[r][c] for c in range(C)] for r in range(R)]
        for r in range(R):
            for c in range(C):
                if [r, c] == end:
                    new_V[r][c] = 0.0
                    continue
                if [r, c] in blocks:
                    new_V[r][c] = 0.0
                    continue

                a = policy[r][c]
                if a in DIRECTIONS:
                    nr, nc = get_next_state(r, c, a, R, C, blocks)
                    reward = 10.0 if [nr, nc] == end else -0.1
                    v = reward + gamma * V[nr][nc]
                else:
                    v = 0.0
                
                new_V[r][c] = v
                delta = max(delta, abs(V[r][c] - new_V[r][c]))
        
        V = new_V
        if delta < epsilon:
            break

    st.session_state.V = V
    st.session_state.display = 'value'

def run_value_iteration(gamma=0.9, epsilon=1e-4):
    R = C = st.session_state.grid_size
    V = [[0.0 for _ in range(C)] for _ in range(R)]
    policy = [['' for _ in range(C)] for _ in range(R)]
    blocks = st.session_state.blocks
    end = st.session_state.end

    while True:
        delta = 0
        new_V = [[V[r][c] for c in range(C)] for r in range(R)]
        
        for r in range(R):
            for c in range(C):
                if [r, c] == end:
                    new_V[r][c] = 0.0
                    continue
                if [r, c] in blocks:
                    new_V[r][c] = 0.0
                    continue

                max_v = float('-inf')
                for a in DIRECTIONS:
                    nr, nc = get_next_state(r, c, a, R, C, blocks)
                    reward = 10.0 if [nr, nc] == end else -0.1
                    v = reward + gamma * V[nr][nc]
                    if v > max_v:
                        max_v = v
                
                new_V[r][c] = max_v
                delta = max(delta, abs(V[r][c] - new_V[r][c]))
        
        V = new_V
        if delta < epsilon:
            break

    for r in range(R):
        for c in range(C):
            if [r, c] == end:
                policy[r][c] = 'GOAL'
                continue
            if [r, c] in blocks:
                policy[r][c] = 'BLOCK'
                continue

            best_a = None
            max_v = float('-inf')
            for a in DIRECTIONS:
                nr, nc = get_next_state(r, c, a, R, C, blocks)
                reward = 10.0 if [nr, nc] == end else -0.1
                v = reward + gamma * V[nr][nc]
                if v > max_v + 1e-8:
                    max_v = v
                    best_a = a
            
            policy[r][c] = best_a

    st.session_state.V = V
    st.session_state.policy = policy
    st.session_state.display = 'policy'

def on_grid_size_change():
    size = st.session_state.new_grid_size
    st.session_state.grid_size = size
    st.session_state.start = [0, 0]
    st.session_state.end = [size-1, size-1]
    st.session_state.blocks = []
    st.session_state.V = None
    st.session_state.policy = None
    st.session_state.display = 'random'
    generate_random_policy(size)

def cell_clicked(r, c):
    mode = st.session_state.mode
    pos = [r, c]
    st.session_state.V = None
    st.session_state.policy = None
    st.session_state.display = 'random'

    if mode == 'start':
        if pos not in st.session_state.blocks and pos != st.session_state.end:
            st.session_state.start = pos
    elif mode == 'end':
        if pos not in st.session_state.blocks and pos != st.session_state.start:
            st.session_state.end = pos
    elif mode == 'block':
        if pos != st.session_state.start and pos != st.session_state.end:
            if pos in st.session_state.blocks:
                st.session_state.blocks.remove(pos)
            else:
                if len(st.session_state.blocks) >= st.session_state.grid_size - 2:
                    st.warning(f"作業要求：最多設定 {st.session_state.grid_size - 2} 個障礙物！", icon="⚠️")
                else:
                    st.session_state.blocks.append(pos)

col1, col2 = st.columns([1, 2])

with col1:
    st.title("Value Iteration (Streamlit)")
    
    st.selectbox("1. 網格大小 (n)", [5, 6, 7, 8, 9], index=[5, 6, 7, 8, 9].index(st.session_state.grid_size), key='new_grid_size', on_change=on_grid_size_change)
    
    st.radio("2. 點擊右側格子設定...", ['start', 'end', 'block'], format_func=lambda x: {'start':'🟢 起點 (Start)', 'end':'🔴 終點 (Goal)', 'block':'⬛ 障礙物 (Block)'}[x], key='mode')
    
    st.radio("3. 顯示模式", ['random', 'value', 'policy'], format_func=lambda x: {'random':'🎲 隨機政策效用', 'value':'🔢 價值函數 V(s)', 'policy':'🧭 最佳政策'}[x], key='display')

    st.button("📊 評估隨機政策 (Policy Eval)", use_container_width=True, type="secondary", on_click=run_policy_evaluation)
        
    st.button("🚀 執行價值迭代 (Value Iteration)", use_container_width=True, type="primary", on_click=run_value_iteration)
        
    st.info("**參數設定**\n- 終點獎勵: +10\n- 每步懲罰: -0.1\n- 折扣因子(γ): 0.9")

with col2:
    st.write("### 互動式網格地圖")
    R = C = st.session_state.grid_size
    
    for r in range(R):
        cols = st.columns(C)
        for c in range(C):
            pos = [r, c]
            is_start = (pos == st.session_state.start)
            is_end = (pos == st.session_state.end)
            is_block = (pos in st.session_state.blocks)
            
            # Formatting Display
            prefix = ""
            if is_start: prefix = "🟢 "
            elif is_end: prefix = "🔴 "
            
            if is_block:
                content = "⬛"
            else:
                display = st.session_state.display
                val = ""
                if not is_end:
                    if display == 'random':
                        act = st.session_state.random_policy[r][c]
                        val = ARROWS.get(act, act)
                    elif display == 'policy':
                        if st.session_state.policy:
                            act = st.session_state.policy[r][c]
                            val = ARROWS.get(act, act)
                        else:
                            val = "?"
                    elif display == 'value':
                        if st.session_state.V is not None:
                            val = f"{st.session_state.V[r][c]:.1f}"
                        else:
                            val = "?"
                else:
                    if display == 'value':
                        val = "0.00"
                    else:
                        val = "🎯"
                
                content = f"{prefix}{val}"
            
            if not content.strip():
                content = " "
                
            with cols[c]:
                # use_container_width fills the column gracefully
                st.button(content, key=f"btn_{r}_{c}", on_click=cell_clicked, args=(r, c), use_container_width=True)

st.markdown("""
<style>
    div[data-testid="column"] button {
        height: 60px;
        font-size: 16px;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

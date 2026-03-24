# 價值迭代算法實作 (Value Iteration) - HW1

這是一個針對「網格地圖與價值迭代算法」的作業實作專案。本專案最初建構於 Flask 前後端分離架構，後來為了方便一鍵部署與雲端展示，全面遷移並改寫為百分百純 Python 的 **Streamlit** 互動式網頁應用程式。

## 🌟 專案功能與作業要求達成

### HW1-1: 網格地圖開發
*   **動態網格大小**：允許使用者從側邊欄自由指定 $n \times n$ 的維度（範圍從 5 到 9）。
*   **互動式設定**：點擊網格即可自由設定起點 (🟢)、終點 (🔴)。
*   **動態障礙物防呆機制**：點擊空地即可新增或移除障礙物 (⬛)，且系統經過防呆保護，強制最多只能設定 $n-2$ 個障礙物。

### HW1-2: 策略顯示與價值評估 (Policy Evaluation)
*   **隨機政策顯示**：針對每一個狀態生成亂數的行動方向（上↑、下↓、左←、右→）作為初始的隨機策略。
*   **政策評估**：點選「評估隨機政策」按鈕後，後台會執行 Policy Evaluation，根據該隨機生成之動作序列，推導並在網格上顯示出每個狀態格子在該策略下的預期價值函式 $V(s)$。

### HW1-3: 使用價值迭代算法推導最佳政策 (Value Iteration)
*   **找出最佳解 (Optimal Policy)**：實裝「執行價值迭代」模組功能，演算法會根據系統設定的終點獎勵 (+10)、步伐懲罰 (-0.1) 以及折扣因子 ($\gamma=0.9$) 不斷迭代至收斂，算出最佳政策。
*   **視覺化隨意切換**：
    *   計算完成後，介面會直接將原本方向錯亂的隨機箭頭，取代為指向最佳路徑的最佳決策箭頭。
    *   提供價值觀看模式無縫切換，可以隨時觀察格子收斂後每個狀態的最佳期望回報 $V^*(s)$。

---

## 🚀 執行與使用方式 (Streamlit 版本)

因為本專案的 `streamlit_app.py` 已經是純 Streamlit 框架，**您可以直接將此資料夾上傳至 GitHub，並在 Streamlit Cloud 將其做為 Repository 連結，即可達成免伺服器的免費一鍵部署。**

若要在您的個人電腦本機端運行測試，請開啟終端機 (Terminal / PowerShell) 並執行以下指令：

```bash
# 1. 確保您的環境已安裝 Streamlit
python -m pip install streamlit

# 2. 啟動伺服器並在瀏覽器中開啟應用程式
python -m streamlit run streamlit_app.py
```

---

## 📝 開發技術筆記與除錯紀錄
在開發過程中，專案從 Flask 順利遷移至 Streamlit，期間曾克服以下兩個實力開發上容易遇到的典型問題，紀錄如下供日後維護與除錯參考：

### 1. 終端機找不到指令路徑 (Path 不存在)
*   **狀況**：在 Windows PowerShell 執行 `streamlit run` 常因系統全域環境變數 (PATH) 未將 Python Scripts 資料夾註冊，而報錯 `CommandNotFoundException`。
*   **解法**：不直接呼叫 `streamlit` 指令，改為呼叫 Python 的掛載模組指令 `python -m streamlit run`，成功順利繞開了此作業系統層級的路徑限制。

### 2. Streamlit 渲染生命週期與狀態鎖定 (`session_state` API 報錯)
*   **狀況**：由於 Streamlit 採取 Top-Down 由上而下直接重繪整個網頁的硬派機制，當按鈕（如 顯示模式）被綁定給 `key='display'` 後，如果我們使用直覺的命令式寫法 `if st.button(...): st.session_state.display = 'policy'`，因代碼在按鈕被畫製宣判後才執行狀態篡改，會引發 Streamlit 底層元件鎖定的保護報錯 (`st.session_state.display cannot be modified after the widget...`)。
*   **解法**：全面捨棄 Imperative 寫法，改採 Streamlit 官方推薦的回呼函式機制（Callbacks）。寫法變更為傳入參數函式：`st.button(..., on_click=run_value_iteration)`。此寫法能確保每一次點擊都必然在「準備由上而下重繪所有 UI 元件」之前被優先攔截執行，如此一來就能毫無衝突地先行改寫掉狀態並平順地畫出更新後的值，解決了狀態碰撞的困擾。

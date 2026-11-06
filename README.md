# MediaPipe AI 手勢控制與虛擬畫板 (Air Canvas)

本專案為電腦視覺與人機互動 (HCI) 課程實作，採用 **Google MediaPipe Hands** 21 個手部關鍵點模型，搭配 **OpenCV** 與 **NumPy**，實現食指即時追蹤、手勢控制虛擬畫板、簡報控制。

---

## 📌 專案架構 (Project Structure)

```text
MediaPipe_Gesture_Canvas/
├── index_tracking.py         # 1. 食指即時追蹤 (Landmark 8)
├── virtual_painter.py        # 2. AI 虛擬畫板 (手勢繪圖/選色/橡皮擦/儲存)
├── gesture_presentation.py   # 3. 手勢簡報控制器 (手勢切換簡報頁碼)
├── requirements.txt          # 專案依賴套件清單
├── .gitignore                # Git 排除檔 (.venv, 快取與輸出檔)
└── README.md                 # 本專案完整說明檔
```

---

## 🛠️ 環境建置與套件安裝 SOP

請使用 **VS Code** 開啟專案資料夾，並開啟 PowerShell / Bash 終端機執行：

### Step 1: 建立並啟動虛擬環境 (Virtual Environment)
```bash
# 建立虛擬環境
python -m venv .venv

# 啟動虛擬環境 (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# 啟動虛擬環境 (Mac / Linux)
source .venv/bin/activate
```

### Step 2: 安裝依賴套件
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> ⚠️ **重點注意事項 (Trouble-Shooting Guidance)**:
> 若安裝最新版 MediaPipe 出現 AttributeError 錯誤，是因為 MediaPipe 0.10.30+ 調整了 Legacy API。
> 本專案已於 `requirements.txt` 指定安裝穩定版本 `mediapipe<=0.10.14`。

---

## 🚀 執行說明

### 1. 執行食指追蹤 (Index Finger Tracking)
```bash
python index_tracking.py
```

### 2. 執行 AI 虛擬畫板 (Virtual Drawing Board)
```bash
python virtual_painter.py
```

### 3. 執行手勢簡報控制 (Gesture Presentation Controller)
```bash
python gesture_presentation.py
```

# 📋 Mobile Device Acceptance Form Extractor

A local, offline tool that extracts data from scanned "Mobile Device Acceptance Form" images and compiles it into an Excel spreadsheet — using a local vision AI model (no cloud API, no cost, no rate limits).

Built for processing bulk scanned/photographed forms (e.g. 100+ images) into a single structured Excel file with an editable table and live progress tracking.

---

## ⚙️ Requirements

- **Python 3.11**
- **Ollama** installed and running locally → https://ollama.com/download
- **Model:** `qwen2.5vl:7b` (vision-capable model used for reading the forms)
- NVIDIA GPU recommended (not required) for faster processing

### Pull the required Ollama model

```powershell
ollama pull qwen2.5vl:7b
```

Confirm it's installed:

```powershell
ollama list
```

Make sure Ollama is running in the background before starting the app (it usually runs automatically after install, or run `ollama serve`).

---

## 📁 Project Structure

```
device-form-extractor/
├── app.py                  # Streamlit UI - main entry point
├── ocr_engine.py            # Talks to Ollama, extracts structured JSON from images
├── excel_handler.py         # Appends rows to Excel, handles load/save
├── schema.py                 # Column definitions + extraction prompt
├── config.py                 # Ollama model name, host URL, paths
├── requirements.txt
├── data/
│   └── output.xlsx           # Growing Excel file (auto-created, not committed)
├── uploads/                  # Temp saved images before processing (not committed)
└── README.md
```

---

## 🚀 Setup & Run

**1. Create virtual environment (Python 3.11)**
```powershell
py -3.11 -m venv device-form-extractor\venv
```

**2. Activate the virtual environment**
```powershell
device-form-extractor\venv\Scripts\Activate.ps1
```
> If PowerShell blocks the script, run this once:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

**3. Install dependencies**
```powershell
pip install -r device-form-extractor\requirements.txt
```

**4. Make sure Ollama is running with the model available**
```powershell
ollama list
```
You should see `qwen2.5vl:7b` listed.

**5. Run the app**
```powershell
streamlit run device-form-extractor\app.py
```

This opens the app in your browser (usually `http://localhost:8501`).

---

## 🖱️ How to Use

1. Drag & drop or browse to upload form images (`.jpg`, `.jpeg`, `.png`) — multiple files supported.
2. Click **🚀 Process Images**.
3. Watch the table populate **live**, row by row, with a processing-time column for each image.
4. Once done, review/edit any misread fields directly in the table (handwriting isn't always 100% accurate).
5. Click **💾 Save Edits to Excel** to persist manual corrections.
6. Click **⬇️ Download Excel** to get the final `.xlsx` file.
7. To start a new batch, click **🗑️ Clear Table**, remove the old uploaded files, and upload new ones.

> All processed data is also auto-saved to `data/output.xlsx` after every single image — so if the app crashes mid-batch, no progress is lost.

---

## 📝 Notes

- Runs 100% locally and offline once the model is pulled — no per-image cost, no external API.
- Larger images take longer; GPU (if available) is used automatically by Ollama.
- Handwriting accuracy depends on the model — always review the table before final export.
```


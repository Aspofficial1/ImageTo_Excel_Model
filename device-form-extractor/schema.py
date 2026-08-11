# Column order matches your target Excel (image 2)
COLUMNS = [
    "Source",
    "Name of Employee",
    "Job Title",
    "Department",
    "Date",
    "MSPS",
    "Description of Device",
    "QTY",
    "Product Serial/IEMI/SIM Number",
    "MAC (LAN & Wireless)",
    "Asset No.",
    "Processing Time (s)",
]

EXTRACTION_PROMPT = """You are reading a scanned "Mobile Device Acceptance Form".
Extract the following fields exactly as written on the form.
If a field is empty or not visible, use "—" (an em dash) as the value.
Return ONLY valid JSON, no markdown, no explanation, no code fences.

JSON keys to use exactly:
{
  "Name of Employee": "",
  "Job Title": "",
  "Department": "",
  "Date": "",
  "MSPS": "",
  "Description of Device": "",
  "QTY": "",
  "Product Serial/IEMI/SIM Number": "",
  "MAC (LAN & Wireless)": "",
  "Asset No.": ""
}

Rules:
- Keep dates in the format written on the form (do not reformat).
- If handwriting is unclear, give your best reading, do not leave blank unless truly empty.
- Do not add extra keys.
- Output must be a single valid JSON object only.
"""
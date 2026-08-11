import os
import pandas as pd

from config import OUTPUT_EXCEL
from schema import COLUMNS


def load_existing() -> pd.DataFrame:
    if os.path.exists(OUTPUT_EXCEL):
        df = pd.read_excel(OUTPUT_EXCEL)
        # Ensure all expected columns exist
        for col in COLUMNS:
            if col not in df.columns:
                df[col] = "—"
        return df[COLUMNS]
    return pd.DataFrame(columns=COLUMNS)


def append_row(df: pd.DataFrame, source_filename: str, extracted: dict, proc_time: float) -> pd.DataFrame:
    # avoid duplicate source
    if not df.empty and source_filename in df["Source"].values:
        return df

    row = {"Source": source_filename}
    for col in COLUMNS[1:-1]:
        row[col] = extracted.get(col, "—")
    row["Processing Time (s)"] = round(proc_time, 2)

    new_row_df = pd.DataFrame([row], columns=COLUMNS)
    return pd.concat([df, new_row_df], ignore_index=True)


def save(df: pd.DataFrame):
    df.to_excel(OUTPUT_EXCEL, index=False)
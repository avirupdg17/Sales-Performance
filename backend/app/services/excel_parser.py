import pandas as pd
from typing import List, Dict
from io import BytesIO

def parse_excel(file: BytesIO) -> Dict[str, List[Dict]]:
    df = pd.read_excel(file, sheet_name=None)

    performance = []

    if "Performance" in df:
        perf_df = df["Performance"].fillna(0)
        for _, row in perf_df.iterrows():
            performance.append({
                "user_id": int(row.get("user_id", 0)),
                "month": str(row.get("month", "")),
                "gross": row.get("gross", 0),
                "mnp": row.get("mnp", 0),
                "jpipo": row.get("jpipo", 0),
                "mdsso": row.get("mdsso", 0),
                "fwa": row.get("fwa", 0),
                "sim_billing": row.get("sim_billing", 0),
                "jio_mnp": row.get("jio_mnp", 0),
                "site_visits": row.get("site_visits", 0),
                "activations": row.get("activations", 0),
            })

    return {"performance": performance}

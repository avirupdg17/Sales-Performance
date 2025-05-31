import pandas as pd
from typing import List, Dict
from io import BytesIO
from datetime import datetime

def parse_excel(file: BytesIO, kpi_date: datetime) -> Dict[str, List[Dict]]:
    df = pd.read_excel(file, sheet_name=None)

    performance = []

    if "Performance" in df:
        perf_df = df["Performance"].fillna(0)
        for _, row in perf_df.iterrows():
            performance.append({
                "user_id": int(row.get("Mobile Number", 0)),
                "gross": row.get("Gross", 0),
                "mnp": row.get("MNP", 0),
                "jpipo": row.get("J PIPO", 0),
                "mdsso": row.get("MDSSO", 0),
                "fwa": row.get("FWA", 0),
                "sim_billing": row.get("Sim Billing", 0),
                "jio_mnp": row.get("Jio MNP", 0),
                "site_visits": row.get("Site Visits",0),          
                "activations": row.get("Activations",0),          
                "m0_incentive": row.get("M0 Incentive(MTD)", 0),
                "m1_incentive": row.get("M1 Incentive", 0),
                "m2_incentive": row.get("M2 Incentive", 0),
                "promoter": row.get("Promoter", ""),
                "distributor": row.get("Distributor", ""),
                "role": row.get("Role", ""),
                "zsm": row.get("ZSM", ""),
                "tsm": row.get("TSM", ""),
                "date": kpi_date.strftime("%Y-%m-%d")
            })

    return {"performance": performance}

from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from collections import defaultdict
from app.auth import get_current_user
from app.database.db import SalesDB
from app.utils.common_methods import ROLE_KPIS, MONTH_MAP, get_last_3_months

router = APIRouter()

@router.get("/dashboard")
def get_dashboard(current_user: dict = Depends(get_current_user)):
    phone = current_user["phone"]

    with SalesDB() as db:
        users = db.get_records("users", [("phone", "=", phone)])
        if not users:
            raise HTTPException(status_code=404, detail="User not found")

        user = users[0]
        user_id = user["id"]
        role = user["role"]

        if role not in ROLE_KPIS:
            raise HTTPException(status_code=403, detail=f"No dashboard for role: {role}")

        kpis = ROLE_KPIS[role]
        months = get_last_3_months()  # [(year, month), ...]
        month_labels = [MONTH_MAP[m] for (_, m) in months]

        all_data = db.get_records("performance", [("role", "=", role)])

        # STEP 1: Filter latest record per user for each relevant month
        latest_monthly_records = defaultdict(lambda: {})  # {(user_id, (year, month)) -> record}

        for row in all_data:
            try:
                date_obj = datetime.strptime(row["date"], "%Y-%m-%d")
                ym = (date_obj.year, date_obj.month)
                uid = int(row["user_id"])

                if ym in months:
                    key = (uid, ym)
                    existing = latest_monthly_records.get(key)
                    if not existing or datetime.strptime(existing["date"], "%Y-%m-%d") < date_obj:
                        latest_monthly_records[key] = row
            except Exception as e:
                print(f"Skipping row due to error: {e} -- row: {row}")
                continue

        # STEP 2: Build incentive-based rankings
        rankings = {}
        for idx, (y, m) in enumerate(months):
            label = month_labels[idx]
            month_users = {}

            for (uid, (ry, rm)), record in latest_monthly_records.items():
                if (ry, rm) == (y, m):
                    month_users[uid] = {
                        "incentive": record.get("m0_incentive", 0) or 0,
                        "jio_mnp": record.get("jio_mnp", 0) or 0
                    }

            sorted_users = sorted(
                month_users.items(),
                key=lambda x: (-x[1]["incentive"], -x[1]["jio_mnp"])
            )

            for rank, (uid, _) in enumerate(sorted_users, 1):
                if uid == user_id:
                    rankings[label] = rank
                    break
            else:
                rankings[label] = None

        # STEP 3: Aggregate KPIs per user per month
        user_month_data = defaultdict(lambda: defaultdict(int))
        for row in all_data:
            try:
                date_obj = datetime.strptime(row["date"], "%Y-%m-%d")
                ym = (date_obj.year, date_obj.month)
                uid = int(row["user_id"])
                if ym in months:
                    for k in kpis:
                        user_month_data[(uid, ym)][k] += row.get(k, 0) or 0
            except Exception as e:
                print(f"Skipping row due to error: {e} -- row: {row}")
                continue

        # STEP 4: Format response
        perf_output = []
        for idx, (y, m) in enumerate(months):
            label = month_labels[idx]
            kpi_data = user_month_data.get((user_id, (y, m)), {})
            perf_output.append({
                "month": label,
                "metrics": {k: kpi_data.get(k, 0) for k in kpis}
            })

        rank_output = [
            {"month": month_labels[idx], "rank": rankings.get(month_labels[idx])}
            for idx in range(3)
        ]

        return {
            "user_id": user_id,
            "role": role,
            "kpis": kpis,
            "performance": perf_output,
            "ranking": rank_output
        }

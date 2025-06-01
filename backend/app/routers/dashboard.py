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
        user_id = phone  # Use phone number as user_id
        role = user["role"]

        if role not in ROLE_KPIS:
            raise HTTPException(status_code=403, detail=f"No dashboard for role: {role}")

        kpis = ROLE_KPIS[role]
        months = get_last_3_months()
        month_labels = [MONTH_MAP[m] for (_, m) in months]

        all_data = db.get_records("performance", [("role", "=", role)])

        user_month_data = defaultdict(lambda: defaultdict(int))
        for row in all_data:
            try:
                date_obj = datetime.strptime(row["date"], "%Y-%m-%d")
                ym = (date_obj.year, date_obj.month)
                uid = str(row["user_id"])
                if ym in months:
                    for k in kpis:
                        user_month_data[(uid, ym)][k] += row.get(k, 0) or 0
            except Exception as e:
                print(f"Skipping row due to error: {e} -- row: {row}")
                continue

        rankings = {}
        for idx, (y, m) in enumerate(months):
            key = f"m{2 - idx}_incentive"
            month_users = {}
            for row in all_data:
                if row.get("date", "").startswith(f"{y}-{m:02d}") and row["role"] == role:
                    uid = row["user_id"]
                    month_users.setdefault(uid, {"incentive": 0, "jio_mnp": 0})
                    month_users[uid]["incentive"] += row.get(key, 0) or 0
                    month_users[uid]["jio_mnp"] += row.get("jio_mnp", 0) or 0

            sorted_users = sorted(
                month_users.items(),
                key=lambda x: (-x[1]["incentive"], -x[1]["jio_mnp"])
            )

            for rank, (uid, _) in enumerate(sorted_users, 1):
                if uid == user_id:
                    rankings[month_labels[idx]] = rank
                    break
            else:
                rankings[month_labels[idx]] = None

        # 🔍 Debug block
            print(f"\n--- Debug: Month {MONTH_MAP[m]} ({y}-{m:02d}) ---")
            print("Logged-in User ID:", user_id)
            print("Month Incentive Key:", key)
            print("Users found in this month:")
            for uid, stats in month_users.items():
                print(f"  {uid}: Incentive={stats['incentive']}, Jio MNP={stats['jio_mnp']}")
            print("Sorted Users (Rank Order):")
            for i, (uid, stats) in enumerate(sorted_users, 1):
                print(f"  Rank {i}: {uid} -> Incentive={stats['incentive']}, Jio MNP={stats['jio_mnp']}")

            for rank, (uid, _) in enumerate(sorted_users, 1):
                if str(uid) == str(user_id):
                    rankings[month_labels[idx]] = rank
                    break
            else:
                rankings[month_labels[idx]] = None

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

from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from collections import defaultdict
from app.auth import get_current_user
from app.database.db import SalesDB

router = APIRouter()

ROLE_KPIS = {
    "asc": ["gross", "mnp", "mdsso", "fwa", "sim_billing", "jio_mnp"],
    "distributor": ["gross", "mnp", "jpipo", "mdsso", "fwa", "jio_mnp"],
    "promoter": ["gross", "mnp", "jpipo", "site_visits", "jio_mnp"],
    "xfe": ["mnp", "site_visits", "activations", "jio_mnp"]
}

MONTH_MAP = {
    1: "January", 2: "February", 3: "March", 4: "April", 5: "May",
    6: "June", 7: "July", 8: "August", 9: "September", 10: "October",
    11: "November", 12: "December"
}

# Determine past 3 months (M2, M1, M0)
def get_last_3_months():
    today = datetime.today()
    months = []
    for i in range(2, -1, -1):
        m = (today.month - i - 1) % 12 + 1
        y = today.year if today.month - i > 0 else today.year - 1
        months.append((y, m))
    return months

@router.get("/dashboard")
def get_dashboard(current_user: dict = Depends(get_current_user)):
    phone = current_user["phone"]

    with SalesDB() as db:
        users = db.get_records("users", [("phone", "=", phone)])
        if not users:
            raise HTTPException(status_code=404, detail="User not found")

        user = users[0]
        user_id = phone  # ✅ use phone number as user_id
        role = user["role"].lower()

        if role not in ROLE_KPIS:
            raise HTTPException(status_code=403, detail=f"No dashboard for role: {role}")

        kpis = ROLE_KPIS[role]
        months = get_last_3_months()  # [(2025, 3), (2025, 4), (2025, 5)]
        month_labels = [MONTH_MAP[m] for (_, m) in months]

        # Load performance data for all users of this role
        all_data = db.get_records("performance", [("role", "=", role)])

        # Build: { (user_id, (year, month)) → {kpis, jio_mnp} }
        user_month_data = defaultdict(lambda: defaultdict(int))
        for row in all_data:
            try:
                date_obj = datetime.strptime(row["date"], "%Y-%m-%d")
                ym = (date_obj.year, date_obj.month)
                uid = row["user_id"]  # phone number
                if ym in months:
                    for k in kpis:
                        user_month_data[(uid, ym)][k] += row.get(k, 0) or 0
            except:
                continue

        # Rankings: For each month, rank users by incentive and jio_mnp
        rankings = {}
        for idx, (y, m) in enumerate(months):
            key = f"m{2 - idx}_incentive"
            month_users = {}
            for row in all_data:
                if row.get("date", "").startswith(f"{y}-{m:02d}") and row["role"].lower() == role:
                    uid = row["user_id"]  # phone number
                    month_users.setdefault(uid, {"incentive": 0, "jio_mnp": 0})
                    month_users[uid]["incentive"] += row.get(key, 0) or 0
                    month_users[uid]["jio_mnp"] += row.get("jio_mnp", 0) or 0

            sorted_users = sorted(
                month_users.items(),
                key=lambda x: (-x[1]["incentive"], -x[1]["jio_mnp"])
            )

            # Store rank of current user
            for rank, (uid, _) in enumerate(sorted_users, 1):
                if uid == user_id:
                    rankings[month_labels[idx]] = rank
                    break
            else:
                rankings[month_labels[idx]] = None  # Not found

        # Prepare performance output for current user
        perf_output = []
        for idx, (y, m) in enumerate(months):
            label = month_labels[idx]
            kpi_data = user_month_data.get((user_id, (y, m)), {})
            perf_output.append({
                "month": label,
                "metrics": {k: kpi_data.get(k, 0) for k in kpis}
            })

        # Prepare rank output
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

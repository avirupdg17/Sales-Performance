from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from collections import defaultdict
from app.utils.common_methods import ROLE_KPIS, MONTH_MAP, get_last_3_months
from app.auth import get_current_user
from app.database.db import SalesDB
from app.utils.image_utils import blob_to_base64

router = APIRouter()

@router.get("/leaderboard")
def get_fixed_three_month_leaderboards(
    current_user: dict = Depends(get_current_user),
):
    phone = current_user["phone"]

    with SalesDB() as db:
        users = db.get_records("users", [("phone", "=", phone)])
        if not users:
            raise HTTPException(status_code=404, detail="User not found")

        user = users[0]
        role = user["role"]

        if role not in ROLE_KPIS:
            raise HTTPException(status_code=403, detail=f"No leaderboard for role: {role}")

        relevant_kpis = ROLE_KPIS[role]
        target_months = get_last_3_months()  # [(year, month), ...]

        # Initialize stats container for each target month
        stats_by_month = {
            (y, m): defaultdict(
                lambda: {
                    "__incentive": 0,
                    "__jio_mnp": 0,
                    "metrics": defaultdict(int)
                }
            ) for (y, m) in target_months
        }

        all_records = db.get_records("performance", [("role", "=", role)])

        def month_minus(y, m, offset):
            m -= offset
            while m <= 0:
                m += 12
                y -= 1
            return (y, m)

        for record in all_records:
            try:
                record_date = datetime.strptime(record["date"], "%Y-%m-%d")
                rec_year = record_date.year
                rec_month = record_date.month
                uid = str(record["user_id"])

                # Map incentives: m0 = current record month, m1 = previous month, m2 = two months ago
                for offset, incentive_key in enumerate(["m0_incentive", "m1_incentive", "m2_incentive"]):
                    target_ym = month_minus(rec_year, rec_month, offset)
                    if target_ym in stats_by_month:
                        stats_by_month[target_ym][uid]["__incentive"] += record.get(incentive_key, 0) or 0
                        stats_by_month[target_ym][uid]["__jio_mnp"] += record.get("jio_mnp", 0) or 0

                        for kpi in relevant_kpis:
                            stats_by_month[target_ym][uid]["metrics"][kpi] += record.get(kpi, 0) or 0

            except Exception as e:
                print(f"Skipping bad record: {e} — {record}")
                continue

        leaderboards = {}

        for (year, month), user_stats in stats_by_month.items():
            sorted_users = sorted(
                user_stats.items(),
                key=lambda x: (-x[1]["__incentive"], -x[1]["__jio_mnp"])
            )

            leaderboard = []
            for rank, (uid, stats) in enumerate(sorted_users[:5], 1):
                profile = db.get_user_profile(uid)
                if not profile:
                    continue

                leaderboard.append({
                    "rank": rank,
                    "user_id": uid,
                    "user_name": profile.get("name", "Unknown"),
                    "user_photo": blob_to_base64(profile.get("photo")),
                    "relevant_metrics": dict(stats["metrics"])
                })

            leaderboards[f"{year}-{month:02d}"] = leaderboard

        return {
            "role": role,
            "leaderboards": leaderboards
        }
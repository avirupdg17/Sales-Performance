from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from collections import defaultdict
from app.auth import get_current_user
from app.database.db import SalesDB
from app.utils.common_methods import ROLE_KPIS, MONTH_MAP, get_last_3_months
from app.utils.image_utils import blob_to_base64

router = APIRouter()

@router.get("/leaderboard")
def get_leaderboards(current_user: dict = Depends(get_current_user)):
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
        target_months = get_last_3_months()  # [(year, month)] with current month first

        all_records = db.get_records("performance", [("role", "=", role)])

        # Group records by (year, month)
        records_by_month = defaultdict(list)
        for rec in all_records:
            try:
                dt = datetime.strptime(rec["date"], "%Y-%m-%d")
                ym = (dt.year, dt.month)
                records_by_month[ym].append(rec)
            except Exception as e:
                print(f"Skipping bad record: {e} -- {rec}")
                continue

        # Find last upload date for each month (for previous months only)
        last_date_by_month = {}
        for ym, recs in records_by_month.items():
            max_date = max(datetime.strptime(r["date"], "%Y-%m-%d") for r in recs)
            last_date_by_month[ym] = max_date.strftime("%Y-%m-%d")
            #print(last_date_by_month)

        leaderboards = {}

        for idx, (y, m) in enumerate(target_months):
            ym = (y, m)
            month_records = records_by_month.get(ym, [])

            # For previous to previous and previous months (idx 1 or 2), filter only last date data
            if idx == 0:
                # Current month - all MTD data
                filtered_records = month_records
            else:
                last_date = last_date_by_month.get(ym)
                if last_date:
                    filtered_records = [r for r in month_records if r["date"] == last_date]
                else:
                    filtered_records = []
            #print(filtered_records)
            # Aggregate user stats
            stats = defaultdict(lambda: {
                "incentive": 0,
                "jio_mnp": 0,
                "metrics": defaultdict(int)
            })

            for rec in filtered_records:
                uid = int(rec["user_id"])
                stats[uid]["incentive"] += rec.get("m0_incentive", 0) or 0
                stats[uid]["jio_mnp"] += rec.get("jio_mnp", 0) or 0
                for kpi in relevant_kpis:
                    stats[uid]["metrics"][kpi] += rec.get(kpi, 0) or 0
            #print(stats)
            # Sort by incentive desc, then jio_mnp desc
            sorted_users = sorted(
                stats.items(),
                key=lambda x: (-x[1]["incentive"], -x[1]["jio_mnp"])
            )
            print(sorted_users)
            top_5 = []
            ftop_5 = []
        for rank, (uid, user_stats) in enumerate(sorted_users[:5], 1):
            profile_result = db.get_records("users", [("id", "=", uid)])
            if not profile_result:
                continue  # skip if user not found
            profile = profile_result[0]

            top_5.append({
                "rank": rank,
                "user_id": uid,
                "user_name": profile.get("name", "Unknown"),
                "user_photo": blob_to_base64(profile.get("photo")),
                "metrics": dict(user_stats["metrics"]),
                "incentive": user_stats["incentive"]
            })
            
            leaderboards[f"{y}-{m:02d}"] = top_5

        return {
            "role": role,
            "leaderboards": leaderboards
        }

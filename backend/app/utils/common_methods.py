from datetime import datetime

ROLE_KPIS = {
    "ASC": ["mnp", "mdsso", "fwa", "sim_billing", "jio_mnp"],
    "Distributor": ["gross", "mnp", "jpipo", "mdsso", "fwa", "jio_mnp"],
    "Promoter": ["gross", "mnp", "jpipo", "site_visits", "jio_mnp"],
    "XFE": ["mnp", "site_visits", "activations", "jio_mnp"]
}

MONTH_MAP = {
    1: "January", 2: "February", 3: "March", 4: "April", 5: "May",
    6: "June", 7: "July", 8: "August", 9: "September", 10: "October",
    11: "November", 12: "December"
}

def get_last_3_months():
    today = datetime.today().replace(day=1)
    months = []
    for i in range(3):
        month = today.month - i
        year = today.year
        if month <= 0:
            month += 12
            year -= 1
        months.append((year, month))
    return months[::-1]
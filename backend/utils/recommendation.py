import json
import os

# Load fertilizer database (new format without stage keys)
def load_fertilizer_data():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    json_path = os.path.join(base_dir, 'database', 'fertilizer_data.json')
    with open(json_path, 'r') as f:
        return json.load(f)

# Get stage index from days since sowing (0 = earliest, 6 = maturity)
def get_stage_index(crop, days):
    # Rice stage boundaries (days)
    rice_ranges = [
        (0,   7),   # germination      → index 0
        (8,   25),  # seedling         → index 1
        (26,  55),  # vegetative       → index 2
        (56,  80),  # tillering        → index 3
        (81,  95),  # flowering        → index 4
        (96,  120), # grain_filling    → index 5
        (121, 999)  # maturity         → index 6
    ]

    # Corn stage boundaries (days)
    corn_ranges = [
        (0,   7),   # germination      → index 0
        (8,   20),  # seedling         → index 1
        (21,  50),  # vegetative       → index 2
        (51,  70),  # tasseling        → index 3
        (71,  85),  # silking          → index 4
        (86,  110), # grain_filling    → index 5
        (111, 999)  # maturity         → index 6
    ]

    ranges = rice_ranges if crop == "rice" else corn_ranges

    for idx, (start, end) in enumerate(ranges):
        if start <= days <= end:
            return idx
    return 6  # fallback to maturity

# Get NPK balance status (unchanged)
def get_npk_status(deficiency):
    if deficiency == "nitrogen":
        return {
            "N": "Low ❌",
            "P": "Check Soil",
            "K": "Check Soil",
            "message": "Nitrogen is critically low. Reduce Urea dependency long term."
        }
    elif deficiency == "phosphorus":
        return {
            "N": "Overusing ⚠️",
            "P": "Low ❌",
            "K": "Check Soil",
            "message": "Phosphorus is low. Farmers in Telangana often ignore DAP."
        }
    elif deficiency == "potassium":
        return {
            "N": "Overusing ⚠️",
            "P": "Check Soil",
            "K": "Low ❌",
            "message": "Potassium is low. MOP is underused by most farmers."
        }
    else:
        return {
            "N": "Balanced ✅",
            "P": "Balanced ✅",
            "K": "Balanced ✅",
            "message": "Crop is healthy. Maintain balanced NPK ratio 4:2:1."
        }

# Get cost saving tip (unchanged)
def get_cost_saving(deficiency):
    if deficiency == "nitrogen":
        return "Applying correct Urea dose saves Rs 800-1200/acre/season"
    elif deficiency == "phosphorus":
        return "Adding DAP improves yield by 15-20% saving Rs 2000/acre"
    elif deficiency == "potassium":
        return "Adding MOP improves grain quality saving Rs 1500/acre"
    else:
        return "Balanced NPK saves Rs 1000-2000/acre compared to Urea only farming"

# Main recommendation function (stages removed)
def get_recommendation(crop, days, deficiency):
    
    # Load data (new structure: data[crop][deficiency] = list of 7 objects)
    data = load_fertilizer_data()
    
    # Get stage index based on days (0..6)
    idx = get_stage_index(crop, days)
    
    # Get fertilizer recommendation from the list at position idx
    recommendation = data[crop][deficiency][idx]
    
    # Get NPK status
    npk_status = get_npk_status(deficiency)
    
    # Get cost saving
    cost_saving = get_cost_saving(deficiency)
    
    # Build response (growth_stage field removed)
    response = {
        "crop"          : crop,
        "days"          : days,
        "deficiency"    : deficiency,
        "fertilizer"    : recommendation["fertilizer"],
        "dosage"        : recommendation["dosage"],
        "method"        : recommendation["method"],
        "npk_tip"       : recommendation["npk_tip"],
        "npk_status"    : npk_status,
        "cost_saving"   : cost_saving
    }
    
    return response
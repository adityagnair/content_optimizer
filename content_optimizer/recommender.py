# recommender.py

from functools import lru_cache

# ----------------------------
# CONFIG
# ----------------------------
PLATFORMS = ["Instagram", "YouTube"]

WEIGHTS = {
    "engagement": 0.5,
    "timing": 0.2,
    "platform": 0.15,
    "efficiency": 0.15
}

# Values from PDF scoring script
PLATFORM_BIAS = {
    ("SHORT", "Instagram"): 1.0,
    ("LONG", "YouTube"): 1.0,
    ("SHORT", "YouTube"): 0.85,
    ("LONG", "Instagram"): 0.7
}


# ----------------------------
# PREPROCESS TO DICTIONARIES
# ----------------------------
def build_lookup(creators, activity_df, history_df):
    creator_base = {
        row.creator_id: row.base_engagement
        for row in creators.itertuples()
    }

    creator_cooldown = {
        row.creator_id: getattr(row, 'cooldown_hours', 0)
        for row in creators.itertuples()
    }

    activity = {
        (row.platform, row.time_slot): row.activity_score
        for row in activity_df.itertuples()
    }

    history = {
        (row.creator_id, row.platform, row.content_type, row.time_slot): row.avg_engagement
        for row in history_df.itertuples()
    }

    return creator_base, activity, history, creator_cooldown


# ----------------------------
# SCORE FUNCTION
# ----------------------------
# ----------------------------
# SCORE FUNCTION
# ----------------------------
def compute_detailed_score(base, act, hist, platform_bias):
    # Engagement score contribution
    eng_score = (base * act * hist) / 1.5
    
    # Timing score
    timing_score = act
    
    # Platform quality score
    platform_score = platform_bias
    
    # Combined weighted score
    total_score = (
        WEIGHTS["engagement"] * eng_score +
        WEIGHTS["timing"] * timing_score +
        WEIGHTS["platform"] * platform_score
    )
    
    return total_score, eng_score, timing_score, platform_score


# ----------------------------
# MAIN RECOMMENDER
# ----------------------------
def recommend_for_content(row, creator_base, activity, history, creator_cooldown, last_post_map):
    creator_id = row["creator_id"]
    content_type = row["content_type"]
    created_time = row["created_timestamp"]
    
    base = creator_base[creator_id]
    cooldown = creator_cooldown.get(creator_id, 0)

    best_score = -float('inf')
    best_platform = None
    best_time = None
    best_metrics = (0, 0, 0)

    for platform in PLATFORMS:
        # Check cooldown constraint
        last_time = last_post_map.get((creator_id, platform), -100)
        
        for t in range(24):
            # Cooldown check: if we post at time t, is it at least cooldown hours after last_time?
            if t < last_time + cooldown:
                continue

            act = activity[(platform, t)]
            hist = history[(creator_id, platform, content_type, t)]
            bias = PLATFORM_BIAS[(content_type, platform)]

            score, eng, tim, plt = compute_detailed_score(base, act, hist, bias)

            if score > best_score:
                best_score = score
                best_platform = platform
                best_time = t
                best_metrics = (eng, tim, plt)

    # Fallback if no time slot is valid (shouldn't happen with large enough range)
    if best_platform is None:
        best_platform = PLATFORMS[0]
        best_time = created_time
        best_metrics = (0, 0, 0)

    # Determine decision: POST_NOW or SCHEDULE
    if best_time == created_time:
        decision = "POST_NOW"
    else:
        decision = "SCHEDULE"

    # Update last_post_map for this creator/platform
    last_post_map[(creator_id, best_platform)] = best_time

    # Return results
    return best_platform, best_time, decision, best_metrics

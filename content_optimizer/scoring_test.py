import pandas as pd
import time

def run_scoring():
    # ------------------------
    # Load Data
    # ------------------------
    try:
        content = pd.read_csv("content.csv")
        activity = pd.read_csv("platform_activity.csv")
        history = pd.read_csv("historical_engagement.csv")
        creators = pd.read_csv("creators.csv")
        submission = pd.read_csv("submission.csv")
    except Exception as e:
        print(f"Error loading files: {e}")
        return

    start_time = time.time()

    # ------------------------
    # Metrics accumulators
    # ------------------------
    engagement_total = 0
    timing_total = 0
    platform_score_total = 0

    # ------------------------
    # Iterate over submissions
    # ------------------------
    # Optimization: pre-index data for faster lookup
    activity_dict = activity.set_index(['platform', 'time_slot'])['activity_score'].to_dict()
    history_dict = history.set_index(['creator_id', 'platform', 'content_type', 'time_slot'])['avg_engagement'].to_dict()
    creators_dict = creators.set_index('creator_id')['base_engagement'].to_dict()
    content_dict = content.set_index('content_id').to_dict('index')

    for _, row in submission.iterrows():
        cid = row["content_id"]
        platform = row["platform"]
        time_slot = row["time_slot"]
        
        c_row = content_dict[cid]
        creator_id = c_row["creator_id"]
        content_type = c_row["content_type"]

        # --- Activity ---
        act = activity_dict.get((platform, time_slot), 0)
        
        # --- Historical ---
        hist = history_dict.get((creator_id, platform, content_type, time_slot), 0)
        
        # --- Creator base ---
        base = creators_dict.get(creator_id, 0)

        # ------------------------
        # 1. Engagement
        # ------------------------
        engagement = base * act * hist
        engagement_total += engagement

        # ------------------------
        # 2. Timing Score
        # ------------------------
        timing_total += act

        # ------------------------
        # 3. Platform Quality (soft)
        # ------------------------
        if content_type == "SHORT" and platform == "Instagram":
            platform_score = 1.0
        elif content_type == "LONG" and platform == "YouTube":
            platform_score = 1.0
        elif content_type == "SHORT" and platform == "YouTube":
            platform_score = 0.85
        else:  # LONG on Instagram (worst)
            platform_score = 0.7
        platform_score_total += platform_score

    # ------------------------
    # Efficiency
    # ------------------------
    latency = time.time() - start_time
    efficiency_score = max(0, 1 - latency)  # normalized

    # ------------------------
    # Normalize Metrics
    # ------------------------
    n = len(submission)
    if n == 0:
        print("Empty submission!")
        return

    engagement_score = engagement_total / n
    timing_score = timing_total / n
    platform_score = platform_score_total / n

    # Optional normalization (safe scaling)
    engagement_score = min(engagement_score, 1.5) / 1.5

    # ------------------------
    # Final Score
    # ------------------------
    final_score = (
        0.50 * engagement_score +
        0.20 * timing_score +
        0.15 * platform_score +
        0.15 * efficiency_score
    )

    # ------------------------
    # Output
    # ------------------------
    print("\n--- SCORE BREAKDOWN ---")
    print(f"Engagement Score: {round(engagement_score, 4)}")
    print(f"Timing Score:     {round(timing_score, 4)}")
    print(f"Platform Score:   {round(platform_score, 4)}")
    print(f"Efficiency Score: {round(efficiency_score, 4)}")
    print(f"\n [SCORE] Final Score: {round(final_score, 4)}")

if __name__ == "__main__":
    run_scoring()

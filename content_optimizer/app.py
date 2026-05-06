from data_loader import load_data
from recommender import recommend_for_content, build_lookup
import pandas as pd


def run_interactive(creator_base, activity_map, history_map, creator_cooldown):
    print("\n--- [ Interactive Content Optimizer ] ---")
    print("Enter content details to get an optimized recommendation.")
    
    try:
        content_id = input("Enter Content ID (e.g., 1-100): ")
        creator_id = int(input("Enter Creator ID (e.g., 1-50): "))
        if creator_id not in creator_base:
            print(f"Error: Creator ID {creator_id} not found in database.")
            return

        content_type = input("Enter Content Type (SHORT/LONG): ").upper()
        if content_type not in ["SHORT", "LONG"]:
            print("Error: Content Type must be SHORT or LONG.")
            return

        created_time = int(input("Enter Time of Upload (Hour 0-23): "))
        if not (0 <= created_time <= 23):
            print("Error: Time must be between 0 and 23.")
            return

        row = {
            "content_id": content_id,
            "creator_id": creator_id,
            "content_type": content_type,
            "created_timestamp": created_time
        }

        # For interactive, we assume no recent posts (clean state)
        last_post_map = {}

        platform, time_slot, decision, metrics = recommend_for_content(
            row, creator_base, activity_map, history_map, creator_cooldown, last_post_map
        )
        eng, tim, plt = metrics

        print("\n--- [ Recommendation Result ] ---")
        print(f"Content ID:            {content_id}")
        print(f"Platform of Upload:    {platform}")
        print(f"Updated Time of Upload: {time_slot}:00")
        print(f"Action Decision:       {decision}")
        print(f"Parameters Used:")
        print(f" - Engagement Score: {eng:.4f}")
        print(f" - Timing Score:     {tim:.4f}")
        print(f" - Platform Quality: {plt:.4f}")
        print(f" - Cooldown Applied: {creator_cooldown.get(creator_id, 0)} hours")
        print("---------------------------------\n")

    except ValueError:
        print("Error: Invalid input. Please enter numbers for ID and Time.")


def main():
    creators, activity, history, content = load_data()

    # build fast lookup tables
    creator_base, activity_map, history_map, creator_cooldown = build_lookup(
        creators, activity, history
    )

    print("\n=== Content Posting Optimization System ===")
    print("1. Run Batch Optimization (content.csv)")
    print("2. Interactive Recommendation (Manual Input)")
    choice = input("Select an option (1/2): ")

    if choice == "1":
        results = []
        import time
        last_post_map = {}
        
        for _, row in content.iterrows():
            item_start = time.time()
            platform, time_slot, decision, metrics = recommend_for_content(
                row, creator_base, activity_map, history_map, creator_cooldown, last_post_map
            )
            item_latency = time.time() - item_start
            item_efficiency = max(0, 1 - item_latency)
            
            eng, tim, plt = metrics
            results.append([
                row["content_id"], platform, time_slot, decision, 
                round(eng, 4), round(tim, 4), round(plt, 4), round(item_efficiency, 4)
            ])

        df = pd.DataFrame(results, columns=[
            "content_id", "platform", "time_slot", "decision", 
            "engagement_param", "timing_param", "platform_param", "efficiency_param"
        ])
        
        df.to_csv("submission.csv", index=False)
        print(f"[OK] Batch optimized recommendations generated in 'submission.csv'!")
    
    elif choice == "2":
        while True:
            run_interactive(creator_base, activity_map, history_map, creator_cooldown)
            cont = input("Recommend another? (y/n): ").lower()
            if cont != 'y':
                break
    else:
        print("Invalid choice. Exiting.")


if __name__ == "__main__":
    main()

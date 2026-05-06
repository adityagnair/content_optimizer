# cli.py

from data_loader import load_data
from recommender import recommend_for_content, build_lookup

def run_cli():
    print("\n📊 Content Posting Optimization System")
    print("--------------------------------------")

    creators, activity, history, content = load_data()
    creator_base, activity_map, history_map = build_lookup(
        creators, activity, history
    )

    while True:
        try:
            print("\n🔹 Enter Content Details")

            creator_id = int(input("Creator ID (1-50): "))
            content_type = input("Content Type (SHORT/LONG): ").strip().upper()
            created_time = int(input("Created Time (0-23): "))

            if content_type not in ["SHORT", "LONG"]:
                print("❌ Invalid content type!")
                continue

            if created_time < 0 or created_time > 23:
                print("❌ Invalid time slot!")
                continue

            test_row = {
                "creator_id": creator_id,
                "content_type": content_type,
                "created_timestamp": created_time
            }

            platform, time_slot, decision = recommend_for_content(
                test_row, creator_base, activity_map, history_map
            )

            print("\n✅ Recommendation")
            print("-------------------")
            print(f"Platform  : {platform}")
            print(f"Time Slot : {time_slot}:00")
            print(f"Decision  : {decision}")

        except Exception as e:
            print("⚠️ Error:", e)

        cont = input("\nDo you want to try again? (y/n): ").lower()
        if cont != 'y':
            print("\n👋 Exiting...")
            break


if __name__ == "__main__":
    run_cli()

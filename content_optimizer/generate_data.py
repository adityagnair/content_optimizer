# generate_data.py
import pandas as pd
import random

random.seed(42)

NUM_CREATORS = 50
NUM_CONTENT = 500

creators = list(range(1, NUM_CREATORS + 1))
platforms = ["Instagram", "YouTube"]
content_types = ["SHORT", "LONG"]
time_slots = list(range(24))

# Creators
creators_df = pd.DataFrame({
    "creator_id": creators,
    "base_engagement": [round(random.uniform(0.6, 1.4), 2) for _ in creators]
})

# Platform activity
activity_data = []
for p in platforms:
    for t in time_slots:
        if p == "Instagram":
            score = 0.4 + (0.6 if 18 <= t <= 22 else 0.2)
        else:
            score = 0.4 + (0.6 if 20 <= t <= 23 else 0.2)
        activity_data.append([p, t, round(score, 2)])

activity_df = pd.DataFrame(activity_data, columns=["platform", "time_slot", "activity_score"])

# Historical engagement
hist_data = []
for c in creators:
    for p in platforms:
        for ct in content_types:
            for t in time_slots:
                base = random.uniform(0.3, 1.0)
                if (p == "Instagram" and ct == "SHORT") or (p == "YouTube" and ct == "LONG"):
                    base *= 1.25
                else:
                    base *= 0.85
                hist_data.append([c, p, ct, t, round(base, 3)])

hist_df = pd.DataFrame(hist_data, columns=[
    "creator_id", "platform", "content_type", "time_slot", "avg_engagement"
])

# Content
content_data = []
for i in range(NUM_CONTENT):
    content_data.append([
        i + 1,
        random.choice(creators),
        random.choice(content_types),
        random.randint(0, 23)
    ])

content_df = pd.DataFrame(content_data, columns=[
    "content_id", "creator_id", "content_type", "created_timestamp"
])

# Save
creators_df.to_csv("creators.csv", index=False)
activity_df.to_csv("platform_activity.csv", index=False)
hist_df.to_csv("historical_engagement.csv", index=False)
content_df.to_csv("content.csv", index=False)

print("✅ Data generated")

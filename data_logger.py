from datetime import datetime, timedelta

# Store the dwell time as a datetime object
dwelltime = datetime.now()

# Simulate some delay (in real usage, this would be the actual pause duration)
import time
time.sleep(1)  # Simulate a 35-second delay

# Check the elapsed time
current_time = datetime.now()
elapsed_time = (current_time - dwelltime).total_seconds()

# Compare elapsed time with 30 seconds
if elapsed_time > 30:
    print("Elapsed time exceeds 30 seconds. Issuing resume macro.")
else:
    print("Elapsed time is within 30 seconds. No action needed.")

# Print the elapsed time for debugging
print(f"Elapsed Time: {elapsed_time:.2f} seconds")
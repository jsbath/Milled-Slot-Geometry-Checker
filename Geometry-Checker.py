# Author: Josh Bath, EIT
# Date: January 13, 2016
# Description: Script to determine edge cases where characteristic equations break down.
# Python version: 3.5.0

from datetime import datetime

# Start timer to give elapsed time
start_time = datetime.now()

def is_geo_possible(tr, dr, wr):
    
    # Most important dimensions that dictate if geometry can be created and meshed successfully
    outside_dia = 4.5
    inside_dia = outside_dia * tr
    slot_depth = (outside_dia - inside_dia) * dr
    slot_width = slot_depth * wr

    # Case 1: Failure if ID is larger than or equal to OD (will never happen per bounds of Thickness Ratio)
    if inside_dia >= outside_dia:
        return False

    # Case 2: Failure if slot width is less than or equal to zero (will never happen per bounds of Width Ratio)
    if slot_width <= 0:
        return False

    # Case 3: Failure if slot depth is less than or equal to zero (will never happen per bounds of Depth Ratio)
    if slot_depth <= 0:
        return False

    # Case 4: Failure if slot depth is larger than or equal to wall thickness (slot becomes thru hole)
    elif slot_depth >= ((outside_dia - inside_dia) / 2):
        return False

    #Case Default: Geometry possible
    else:
        return True

# Create critical ratio ranges (list comprehension instead of range() because of floating
# point bounds/steps). Exclude Aspect Ratio as it will have no impact on geometry failure.
thickness_ratio = [x * .05 for x in range(1, 20)]   # Min: 0.05, Max: 0.95, Step: 0.05
depth_ratio = [x * .05 for x in range(1, 20)]       # Min: 0.05, Max: 0.95, Step: 0.05
width_ratio = [x * .05 for x in range(40, 791)]     # Min: 2, Max: 39.5, Step: 0.05

# Counter to tally geometry attempts
success_count = 0
fail_count = 0
total_count = 0

# Nested for-each loop to iterate through all permutations sequentially
for tr in thickness_ratio:
    for dr in depth_ratio:
        for wr in width_ratio:
            if is_geo_possible(tr, dr, wr) is True:
                success_count += 1
                total_count += 1
                print("--SUCCESS!-- (#{0}): TR: {1:.2f} DR: {2:.2f} WR: {3:.2f}".format(total_count, tr, dr, wr))
            else:
                fail_count += 1
                total_count += 1
                print("--FAILURE!-- (#{0}): TR: {1:.2f} DR: {2:.2f} WR: {3:.2f}".format(total_count, tr, dr, wr))

print("")
print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
print("TOTAL ITERATIONS COMPUTED: {0}".format(total_count))
print("SUCCESSES: {0}".format(success_count))
print("FAILURES: {0}".format(fail_count))
print("% SUCCESS: {0:.2f}".format((success_count / total_count) * 100))
print("TIME ELAPSED: {0}".format(datetime.now() - start_time))
print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
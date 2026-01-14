import collections

class GlobalBalancedSchedulerCSP:
    def __init__(self, interviewee_avail, interleaved_slots, total_cap_per_slot=2, daily_limit=13):
        self.interviewee_avail = interviewee_avail
        self.slots = interleaved_slots
        self.total_cap_per_slot = total_cap_per_slot
        self.daily_limit = daily_limit
        self.assignment = {}
        self.slot_occupancy = collections.defaultdict(int)
        self.daily_occupancy = collections.defaultdict(int)

    def is_consistent(self, person, day, time):
        # Daily balancing check
        if self.daily_occupancy[day] >= self.daily_limit:
            return False
        
        # Total capacity check (Fixed at 2 persons)
        if self.slot_occupancy[(day, time)] >= self.total_cap_per_slot:
            return False
        
        # Interviewee availability check
        hour = int(time.split(':')[0])
        if any(d == day and h == hour for d, h in self.interviewee_avail.get(person, [])):
            return True
            
        return False

    def solve(self, interviewee_list, index=0):
        if index == len(interviewee_list):
            return True

        current_person = interviewee_list[index]
        
        # Grouping Heuristic: 1명이 이미 배정된 Slot을 우선 탐색하여 2인 1조를 유도합니다.
        priority_levels = [1, 0]
        
        for level in priority_levels:
            for day, time in self.slots:
                if self.slot_occupancy[(day, time)] == level:
                    if self.is_consistent(current_person, day, time):
                        # Assign Variable to Slot
                        self.assignment[current_person] = (day, time)
                        self.slot_occupancy[(day, time)] += 1
                        self.daily_occupancy[day] += 1
                        
                        if self.solve(interviewee_list, index + 1):
                            return True
                        
                        # Backtrack
                        del self.assignment[current_person]
                        self.slot_occupancy[(day, time)] -= 1
                        self.daily_occupancy[day] -= 1

        return self.solve(interviewee_list, index + 1)

def generate_time_list(start, end, skip=12):
    times = []
    for h in range(start, end):
        if h == skip: continue
        times.append(f"{h:02d}:00")
        times.append(f"{h:02d}:30")
    return times

# 1. Interleaved Slots (Early Finish + Balancing)
fri_times = generate_time_list(15, 22)
sat_times = generate_time_list(10, 17)
sun_times = generate_time_list(10, 16)

interleaved_slots = []
max_len = max(len(fri_times), len(sat_times), len(sun_times))
for i in range(max_len):
    if i < len(sat_times): interleaved_slots.append(("1/17(토)", sat_times[i]))
    if i < len(sun_times): interleaved_slots.append(("1/18(일)", sun_times[i]))
    if i < len(fri_times): interleaved_slots.append(("1/16(금)", fri_times[i]))

# 2. Interviewee Availability Data (Interviewer Condition Removed)
itve_avail_data = {
    "오창현": [("1/16(금)", 15), ("1/16(금)", 16), ("1/17(토)", 10), ("1/17(토)", 11), ("1/18(일)", 10), ("1/18(일)", 11)],
    "강동인": [("1/16(금)", 20), ("1/16(금)", 21), ("1/17(토)", 10), ("1/17(토)", 11), ("1/18(일)", 10), ("1/18(일)", 11)],
    "김형훈": [("1/16(금)", 15), ("1/16(금)", 16), ("1/17(토)", 10), ("1/17(토)", 11)],
    "류민주": [("1/16(금)", 15), ("1/16(금)", 16), ("1/17(토)", 10), ("1/17(토)", 11)],
    "용이립": [("1/17(토)", 10), ("1/17(토)", 11)],
    "장현정": [("1/18(일)", 10), ("1/18(일)", 11), ("1/18(일)", 13)],
    "백우헌": [("1/18(일)", 10), ("1/18(일)", 11)],
    "이주호": [("1/16(금)", 15), ("1/16(금)", 20), ("1/18(일)", 10), ("1/18(일)", 11)],
    "강지훈": [("1/16(금)", 15), ("1/17(토)", 14), ("1/18(일)", 10)],
    "배예림": [("1/17(토)", 14), ("1/18(일)", 10), ("1/18(일)", 11)],
    "최재민": [("1/18(일)", 10), ("1/18(일)", 11)],
    "김윤주": [("1/16(금)", 16), ("1/17(토)", 11), ("1/18(일)", 11)],
    "김현우": [("1/16(금)", 19), ("1/17(토)", 11)],
    "홍지욱": [("1/16(금)", 17), ("1/17(토)", 11), ("1/18(일)", 11)],
    "정윤호": [("1/16(금)", 15), ("1/18(일)", 11)],
    "진승환": [("1/16(금)", 15), ("1/17(토)", 15), ("1/18(일)", 13)],
    "하준수": [("1/17(토)", 15), ("1/18(일)", 13)],
    "이예슬": [("1/16(금)", 18), ("1/17(토)", 15)],
    "권태욱": [("1/16(금)", 15), ("1/17(토)", 15)],
    "이호재": [("1/16(금)", 15), ("1/17(토)", 13), ("1/18(일)", 13)],
    "노제희": [("1/16(금)", 20), ("1/17(토)", 13)],
    "정연욱": [("1/16(금)", 15), ("1/17(토)", 16), ("1/18(일)", 13)],
    "이재환": [("1/16(금)", 15), ("1/18(일)", 13)],
    "윤민섭": [("1/16(금)", 15), ("1/18(일)", 13)],
    "권상현": [("1/17(토)", 13), ("1/18(일)", 13)],
    "최재현": [("1/17(토)", 13)],
    "이재준": [("1/17(토)", 14), ("1/18(일)", 14)],
    "김아현": [("1/16(금)", 16), ("1/18(일)", 14)],
    "김다헌": [("1/18(일)", 14)],
    "Ari M": [("1/17(토)", 14), ("1/18(일)", 14)],
    "김민지": [("1/16(금)", 16), ("1/17(토)", 14)],
    "장현성": [("1/16(금)", 16), ("1/17(토)", 14)],
    "최석훈": [("1/16(금)", 15)],
    "양승완": [("1/16(금)", 18), ("1/18(일)", 14)],
    "곽준성": [("1/16(금)", 18)],
    "김태현": [("1/16(금)", 17)],
    "박준형": [("1/16(금)", 17), ("1/16(금)", 19)]
}

# 3. Solver Execution
# 39명을 3일로 나눌 시 하루 약 13명 배정 (daily_limit=13)
scheduler = GlobalBalancedSchedulerCSP(itve_avail_data, interleaved_slots, daily_limit=13)
itve_list = list(itve_avail_data.keys())
scheduler.solve(itve_list)

# 4. Result Display
results = collections.defaultdict(lambda: collections.defaultdict(list))
for p, (day, time) in scheduler.assignment.items():
    results[day][time].append(p)

for day in ["1/17(토)", "1/18(일)", "1/16(금)"]:
    print(f"\n--- {day} ---")
    day_res = results[day]
    for t in sorted(day_res.keys()):
        print(f"{t}: {', '.join(day_res[t])}")
    print(f"Total: {scheduler.daily_occupancy[day]}명")
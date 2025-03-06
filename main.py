import json
from datetime import datetime


def parse_time(time_str):
    return datetime.strptime(time_str, "%H:%M:%S")


def calculate_race_time(start, finish):
    start_time = parse_time(start)
    finish_time = parse_time(finish)
    if finish_time < start_time:
        finish_time = finish_time.replace(day=2)
    race_duration = finish_time - start_time
    return str(race_duration)


def load_prizes(file_path):
    prizes = {}
    with open(file_path, encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(" ", 2)
            place = int(parts[0])
            prize = parts[2] if len(parts) > 2 else ""
            prizes[place] = prize
    return prizes


def process_race_data(input_file, prize_files):
    with open(input_file, encoding='utf-8') as f:
        race_data = json.load(f)

    categories = {}
    for entry in race_data:
        category = entry["Категория"].lower()
        if category not in categories:
            categories[category] = []
        race_time = calculate_race_time(entry["Время старта"], entry["Время финиша"])
        categories[category].append({
            "Нагрудный номер": entry["Нагрудный номер"],
            "Имя и Фамилия": f"{entry['Имя']} {entry['Фамилия']}",
            "Время": race_time
        })

    for category, athletes in categories.items():
        athletes.sort(key=lambda x: (x["Время"], x["Нагрудный номер"]))

        prize_list = load_prizes(prize_files.get(category, ""))
        for idx, athlete in enumerate(athletes, start=1):
            athlete["Место"] = idx
            if idx <= 49:
                athlete["Приз"] = prize_list.get(idx, "")

        with open(f"{category}.json", "w", encoding='utf-8') as f:
            json.dump(athletes, f, ensure_ascii=False, indent=2)


def main():
    prize_files = {
        "m15": "prizes_list_m15.txt",
        "m16": "prizes_list_m16.txt",
        "m18": "prizes_list_m18.txt",
        "w15": "prizes_list_w15.txt",
        "w16": "prizes_list_w16.txt",
        "w18": "prizes_list_w18.txt",
    }
    process_race_data("race_data.json", prize_files)


if __name__ == "__main__":
    main()


import json
import math
from pathlib import Path

# 根据当前文件位置定位项目根目录，避免运行目录不同导致找不到数据
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "attractions.json"


def load_attractions():
    """读取景点数据"""
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def calculate_distance(lat1, lon1, lat2, lon2):
    """Haversine 公式计算两点间球面距离，单位：km"""
    radius = 6371.0

    lat1, lon1, lat2, lon2 = map(
        math.radians, [lat1, lon1, lat2, lon2]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    a = min(1.0, max(0.0, a))
    return 2 * radius * math.asin(math.sqrt(a))


def find_nearby_attractions(latitude, longitude, radius_km=3):
    """查询指定半径内的景点，按距离从近到远排列"""
    attractions = load_attractions()
    results = []

    for attraction in attractions:
        distance = calculate_distance(
            latitude,
            longitude,
            attraction["latitude"],
            attraction["longitude"]
        )

        if distance <= radius_km:
            results.append({
                **attraction,
                "distance_km": round(distance, 3)
            })

    return sorted(results, key=lambda x: x["distance_km"])


def plan_route(latitude, longitude, attractions):
    """最近邻算法规划近似游览顺序"""
    remaining = [item.copy() for item in attractions]
    route = []
    current_lat = latitude
    current_lon = longitude
    total_distance = 0.0

    while remaining:
        nearest = min(
            remaining,
            key=lambda item: calculate_distance(
                current_lat,
                current_lon,
                item["latitude"],
                item["longitude"]
            )
        )

        distance = calculate_distance(
            current_lat,
            current_lon,
            nearest["latitude"],
            nearest["longitude"]
        )

        route.append({
            **nearest,
            "segment_distance_km": round(distance, 3)
        })

        total_distance += distance
        current_lat = nearest["latitude"]
        current_lon = nearest["longitude"]
        remaining.remove(nearest)

    return {
        "route": route,
        "total_distance_km": round(total_distance, 3),
        "distance_type": "straight_line",
        "algorithm": "nearest_neighbor"
    }


if __name__ == "__main__":
    # 米兰大教堂附近的测试坐标
    test_lat = 45.464121
    test_lon = 9.191872

    print("=== 附近景点查询 ===")
    nearby = find_nearby_attractions(
        test_lat, test_lon, radius_km=3
    )

    for item in nearby:
        print(f"{item['name']}: {item['distance_km']} km")

    print("\n=== 游览路线规划 ===")
    result = plan_route(test_lat, test_lon, nearby)

    for index, item in enumerate(result["route"], start=1):
        print(
            f"{index}. {item['name']} "
            f"(本段距离: {item['segment_distance_km']} km)"
        )

    print(
        f"总直线距离: {result['total_distance_km']} km"
    )

import random

class TrafficLight:
    """信号機の状態を管理するクラス"""
    def __init__(self, initial_state, durations):
        self.states = ["青", "黄", "赤"]
        self.durations = durations
        self.current_state = initial_state
        self.timer = self.durations[self.current_state]

    def update(self, delta_time):
        self.timer -= delta_time
        if self.timer <= 0:
            current_index = self.states.index(self.current_state)
            next_index = (current_index + 1) % len(self.states)
            self.current_state = self.states[next_index]
            self.timer = self.durations[self.current_state]

class Vehicle:
    """車両を管理するクラス"""
    def __init__(self, road, direction):
        self.road = road
        self.direction = direction
        
        self.length = 50
        self.width_on_road = 20
        self.speed = 2
        
        LANE_CENTER_NS_N = 390
        LANE_CENTER_NS_S = 510
        LANE_CENTER_WE_W = 390
        LANE_CENTER_WE_E = 510
        
        if self.road == "NS":
            self.draw_width = self.width_on_road
            self.draw_height = self.length
            self.y = 800 if direction == 1 else -self.draw_height
            self.x = LANE_CENTER_NS_S - self.draw_width / 2 if direction == 1 else LANE_CENTER_NS_N - self.draw_width / 2
        else: # WE
            self.draw_width = self.length
            self.draw_height = self.width_on_road
            self.x = -self.draw_width if direction == 1 else 800
            self.y = LANE_CENTER_WE_W - self.draw_height / 2 if direction == 1 else LANE_CENTER_WE_E - self.draw_height / 2

    def move(self):
        if self.road == "NS":
            self.y -= self.speed * self.direction
        else:
            self.x += self.speed * self.direction
            
    def is_out_of_bounds(self, width, height):
        return self.x > width or self.x < -self.draw_width or \
               self.y > height or self.y < -self.draw_height

class Simulation:
    """シミュレーション全体を管理するクラス"""
    def __init__(self):
        self.ns_light = TrafficLight("青", {"青": 15, "黄": 3, "赤": 22})
        self.we_light = TrafficLight("赤", {"赤": 28, "青": 10, "黄": 2})
        self.vehicles = []
        self.time_since_last_spawn = 0
        self.spawn_interval = 2

    def update(self, delta_time):
        self.ns_light.update(delta_time)
        self.we_light.update(delta_time)

        self.time_since_last_spawn += delta_time
        if self.time_since_last_spawn >= self.spawn_interval:
            self.spawn_vehicle()
            self.time_since_last_spawn = 0

        vehicles_to_remove = []
        for v in self.vehicles:
            if self.check_can_move(v):
                v.move()

            if v.is_out_of_bounds(800, 800):
                vehicles_to_remove.append(v)
        
        self.vehicles = [v for v in self.vehicles if v not in vehicles_to_remove]

    def spawn_vehicle(self):
        road = random.choice(["NS", "WE"])
        direction = random.choice([1, -1])
        # 新しい車両が既存の車両と重ならないかチェック
        # (簡易的なチェック: 同じ進入路の最後の車と十分に離れているか)
        # ※今回はcheck_can_moveが頑健になったので、ここでのチェックは不要
        self.vehicles.append(Vehicle(road, direction))

    def check_can_move(self, vehicle):
        """車両が動けるか（信号と先行車）を判定する"""
        
        # --- 1. 信号のチェック ---
        STOP_LINE_N = 350
        STOP_LINE_S = 550
        STOP_LINE_W = 350
        STOP_LINE_E = 550
        
        light_state = self.ns_light.current_state if vehicle.road == "NS" else self.we_light.current_state
        if light_state in ["赤", "黄"]:
            if vehicle.road == "NS":
                # 南向き (N->S, dir=-1)
                if vehicle.direction == -1 and (vehicle.y + vehicle.draw_height) > STOP_LINE_N - 20 and (vehicle.y + vehicle.draw_height) <= STOP_LINE_N:
                    return False
                # 北向き (S->N, dir=1)
                if vehicle.direction == 1 and vehicle.y < STOP_LINE_S + 20 and vehicle.y >= STOP_LINE_S:
                    return False
            else: # WE
                # 東向き (W->E, dir=1)
                if vehicle.direction == 1 and vehicle.x < STOP_LINE_W + 20 and vehicle.x >= STOP_LINE_W:
                    return False
                # 西向き (E->W, dir=-1)
                if vehicle.direction == -1 and (vehicle.x + vehicle.draw_width) > STOP_LINE_E - 20 and (vehicle.x + vehicle.draw_width) <= STOP_LINE_E:
                    return False

        # --- 2. 先行車との衝突チェック ---
        # 車両長さの1/5を安全な車間距離とする
        safety_gap = vehicle.length / 5

        for other in self.vehicles:
            if vehicle is other or vehicle.road != other.road or vehicle.direction != other.direction:
                continue

            # is_other_ahead: otherがvehicleの進行方向にいるか
            # gap: vehicleの前端とotherの後端の距離
            is_other_ahead = False
            gap = float('inf')

            if vehicle.road == "NS":
                if vehicle.direction == 1: # 北向き (S->N)
                    if other.y < vehicle.y:
                        is_other_ahead = True
                        gap = vehicle.y - (other.y + other.draw_height)
                else: # 南向き (N->S)
                    if other.y > vehicle.y:
                        is_other_ahead = True
                        gap = other.y - (vehicle.y + vehicle.draw_height)
            else: # WE
                if vehicle.direction == 1: # 東向き (W->E)
                    if other.x > vehicle.x:
                        is_other_ahead = True
                        gap = other.x - (vehicle.x + vehicle.draw_width)
                else: # 西向き (E->W)
                    if other.x < vehicle.x:
                        is_other_ahead = True
                        gap = vehicle.x - (other.x + other.draw_width)
            
            # 先行車がいて、車間距離が安全距離より短い場合は停止
            if is_other_ahead and gap < safety_gap:
                return False

        return True
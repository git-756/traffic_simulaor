# simulation.py
import random

class TrafficLight:
    """信号機の状態を管理するクラス"""
    def __init__(self, initial_state, durations):
        self.states = ["青", "黄", "赤"]
        self.durations = durations
        self.current_state = initial_state
        self.timer = self.durations[self.current_state]

    def update(self, delta_time):
        """時間経過で信号の状態を更新する"""
        self.timer -= delta_time
        if self.timer <= 0:
            current_index = self.states.index(self.current_state)
            next_index = (current_index + 1) % len(self.states)
            self.current_state = self.states[next_index]
            self.timer = self.durations[self.current_state]

class Vehicle:
    """車両を管理するクラス"""
    def __init__(self, road, direction):
        self.road = road  # "NS" (南北) or "WE" (東西)
        self.direction = direction  # 1 (南→北, 西→東) or -1 (北→南, 東→西)
        
        # 初期位置を設定
        if self.road == "NS":
            self.x = 425 if direction == 1 else 475
            self.y = 800 if direction == 1 else 0
        else: # WE
            self.x = 0 if direction == 1 else 800
            self.y = 475 if direction == 1 else 425
            
        self.speed = 2
        self.width = 20
        self.height = 40

    def move(self):
        """車両を移動させる"""
        if self.road == "NS":
            self.y -= self.speed * self.direction
        else: # WE
            self.x += self.speed * self.direction
            
    def is_out_of_bounds(self, width, height):
        """車両が画面外に出たか判定"""
        return self.x < -self.width or self.x > width or \
               self.y < -self.height or self.y > height

class Simulation:
    """シミュレーション全体を管理するクラス"""
    def __init__(self):
        # 南北: 青15s, 黄3s, 赤22s
        self.ns_light = TrafficLight("青", {"青": 15, "黄": 3, "赤": 22})
        # 東西: 赤18s, 青10s, 黄2s
        self.we_light = TrafficLight("赤", {"赤": 18, "青": 10, "黄": 2})
        
        self.vehicles = []
        self.time_since_last_spawn = 0
        self.spawn_interval = 2 # 2秒ごとに車両を生成

    def update(self, delta_time):
        """シミュレーションの状態を1フレーム分更新する"""
        self.ns_light.update(delta_time)
        self.we_light.update(delta_time)

        # 車両の生成
        self.time_since_last_spawn += delta_time
        if self.time_since_last_spawn >= self.spawn_interval:
            self.spawn_vehicle()
            self.time_since_last_spawn = 0

        # 車両の移動と削除
        vehicles_to_remove = []
        for v in self.vehicles:
            can_move = self.check_can_move(v)
            if can_move:
                v.move()

            if v.is_out_of_bounds(800, 800):
                vehicles_to_remove.append(v)
        
        self.vehicles = [v for v in self.vehicles if v not in vehicles_to_remove]

    def spawn_vehicle(self):
        """新しい車両をランダムに生成する"""
        road = random.choice(["NS", "WE"])
        direction = random.choice([1, -1])
        self.vehicles.append(Vehicle(road, direction))

# simulation.py の check_can_move メソッドを書き換え
    def check_can_move(self, vehicle):
        """車両が信号に従って動けるか判定する"""
        # 交差点の境界座標
        INTERSECTION_Y_START = 350
        INTERSECTION_Y_END = 550
        INTERSECTION_X_START = 350
        INTERSECTION_X_END = 550

        # 車両の先端が停止すべきかを判定する範囲
        DETECTION_RANGE = 50 

        if vehicle.road == "NS":
            light_state = self.ns_light.current_state
            if light_state in ["赤", "黄"]:
                # 北から南へ向かう車両 (direction=-1)
                # 車両の下端が交差点の北端に近づいているか
                vehicle_front_y = vehicle.y + vehicle.height
                if (INTERSECTION_Y_START - DETECTION_RANGE) < vehicle_front_y < INTERSECTION_Y_START:
                    return False
            
                # 南から北へ向かう車両 (direction=1)
                # 車両の上端が交差点の南端に近づいているか
                vehicle_front_y = vehicle.y
                if INTERSECTION_Y_END < vehicle_front_y < (INTERSECTION_Y_END + DETECTION_RANGE):
                    return False
        else: # WE
            light_state = self.we_light.current_state
            if light_state in ["赤", "黄"]:
                # 東から西へ向かう車両 (direction=-1)
                # 車両の右端が交差点の東端に近づいているか
                vehicle_front_x = vehicle.x + vehicle.height # 横向きなのでheight
                if INTERSECTION_X_END < vehicle_front_x < (INTERSECTION_X_END + DETECTION_RANGE):
                    return False

                # 西から東へ向かう車両 (direction=1)
                # 車両の左端が交差点の西端に近づいているか
                vehicle_front_x = vehicle.x
                if (INTERSECTION_X_START - DETECTION_RANGE) < vehicle_front_x < INTERSECTION_X_START:
                    return False
        
        return True
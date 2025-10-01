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

    def check_can_move(self, vehicle):
        """車両が信号に従って動けるか判定する"""
        stop_line_ns = 400
        stop_line_we = 400
        
        if vehicle.road == "NS":
            # 南向き(direction=-1)で停止線より手前、かつ信号が赤か黄の場合
            if vehicle.direction == -1 and 350 < vehicle.y < stop_line_ns and self.ns_light.current_state in ["赤", "黄"]:
                return False
            # 北向き(direction=1)で停止線より手前、かつ信号が赤か黄の場合
            if vehicle.direction == 1 and 450 > vehicle.y > stop_line_ns and self.ns_light.current_state in ["赤", "黄"]:
                return False
        else: # WE
            # 西向き(direction=-1)で停止線より手前、かつ信号が赤か黄の場合
            if vehicle.direction == -1 and 450 > vehicle.x > stop_line_we and self.we_light.current_state in ["赤", "黄"]:
                return False
            # 東向き(direction=1)で停止線より手前、かつ信号が赤か黄の場合
            if vehicle.direction == 1 and 350 < vehicle.x < stop_line_we and self.we_light.current_state in ["赤", "黄"]:
                return False
        
        return True
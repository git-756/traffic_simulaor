# main.py
import time

class TrafficLight:
    """
    信号機の状態を管理するクラス
    """
    def __init__(self, name, states, durations):
        """
        Args:
            name (str): 信号機の名前 (例: "南北方向", "東西方向")
            states (list): 信号機の状態のリスト (例: ["青", "黄", "赤"])
            durations (dict): 各状態の継続時間（秒） (例: {"青": 10, "黄": 2, "赤": 12})
        """
        self.name = name
        self.states = states
        self.durations = durations
        self.current_state_index = 0 # 初期状態はリストの先頭（例: "青"）

    def get_current_state(self):
        """現在の状態を返す"""
        return self.states[self.current_state_index]

    def get_current_duration(self):
        """現在の状態の継続時間を返す"""
        state = self.get_current_state()
        return self.durations[state]

    def switch_to_next_state(self):
        """次の状態に切り替える"""
        self.current_state_index = (self.current_state_index + 1) % len(self.states)
        print(f"[{self.name}] 信号が {self.get_current_state()} に変わりました。")


def run_simulation(duration_seconds):
    """
    指定された時間だけ信号シミュレーションを実行する
    
    Args:
        duration_seconds (int): シミュレーションの総実行時間（秒）
    """
    # 南北方向（主道路）の信号機を設定
    # 青(15秒) -> 黄(3秒) -> 赤(22秒) のサイクル
    ns_light = TrafficLight(
        name="南北方向",
        states=["青", "黄", "赤"],
        durations={"青": 15, "黄": 3, "赤": 22}
    )

    # 東西方向（従道路）の信号機を設定
    # 南北が赤の間だけ青になる
    # 赤(18秒) -> 青(10秒) -> 黄(2秒) -> 赤(10秒) ※これは単純化のため赤から開始
    we_light = TrafficLight(
        name="東西方向",
        states=["赤", "青", "黄"],
        durations={"赤": 18, "青": 10, "黄": 2}
    )
    # 初期状態を赤に設定
    we_light.current_state_index = 0

    print("--- 信号シミュレーションを開始します ---")
    print(f"初期状態: [{ns_light.name}] {ns_light.get_current_state()}, [{we_light.name}] {we_light.get_current_state()}")

    simulation_time = 0
    while simulation_time < duration_seconds:
        # 現在の各信号の継続時間を取得
        ns_duration = ns_light.get_current_duration()
        we_duration = we_light.get_current_duration()

        # このサイクルで経過する時間は、両方の信号が次に切り替わるまでの最短時間
        # 今回は同期していると仮定し、南北の時間を基準とする
        time_to_wait = ns_duration
        
        # 待機時間を表示
        print(f"\nシミュレーション時間: {simulation_time}秒")
        print(f"現在の状態: [{ns_light.name}] {ns_light.get_current_state()}, [{we_light.name}] {we_light.get_current_state()}")
        print(f"次の変化まで {time_to_wait}秒 待機します...")

        # 待機
        time.sleep(time_to_wait)

        # 時間を更新
        simulation_time += time_to_wait
        
        # 信号を次の状態に切り替える
        ns_light.switch_to_next_state()
        we_light.switch_to_next_state()

    print("\n--- シミュレーションを終了します ---")

if __name__ == "__main__":
    # 120秒間シミュレーションを実行
    run_simulation(120)
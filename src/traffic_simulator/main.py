# main.py
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import QTimer
from simulation import Simulation
from widgets import SimulationWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("交通信号シミュレーター")
        self.setGeometry(100, 100, 820, 850) # ウィンドウサイズを調整

        # シミュレーションインスタンスを作成
        self.simulation = Simulation()

        # UIのセットアップ
        self.setup_ui()

        # QTimerのセットアップ
        self.timer = QTimer(self)
        self.timer.setInterval(50)  # 50ミリ秒ごとに更新 (20 FPS)
        self.timer.timeout.connect(self.update_simulation)

    def setup_ui(self):
        # メインのウィジェットとレイアウト
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 描画ウィジェットを作成
        self.simulation_widget = SimulationWidget(self.simulation)
        layout.addWidget(self.simulation_widget)

        # 開始/停止ボタン
        self.start_button = QPushButton("シミュレーション開始")
        self.start_button.clicked.connect(self.toggle_simulation)
        layout.addWidget(self.start_button)
        
        self.is_running = False

    def toggle_simulation(self):
        if self.is_running:
            self.timer.stop()
            self.start_button.setText("シミュレーション再開")
        else:
            self.timer.start()
            self.start_button.setText("シミュレーション停止")
        self.is_running = not self.is_running
        
    def update_simulation(self):
        """タイマーによって呼び出される更新処理"""
        # 1フレームの時間 (秒単位)
        delta_time = self.timer.interval() / 1000.0
        
        # シミュレーションロジックを更新
        self.simulation.update(delta_time)
        
        # 描画ウィジェットに再描画を指示
        self.simulation_widget.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
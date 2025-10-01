# widgets.py
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont
from PySide6.QtCore import Qt, QRect

class SimulationWidget(QWidget):
    """シミュレーションを描画するためのウィジェット"""
    def __init__(self, simulation, parent=None):
        super().__init__(parent)
        self.simulation = simulation

    def paintEvent(self, event):
        """描画処理を行う（このメソッドは自動的に呼ばれる）"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing) # アンチエイリアスを有効に

        # 背景を描画
        painter.fillRect(self.rect(), Qt.darkGray)

        # 道路を描画
        self.draw_roads(painter)
        
        # 信号機を描画
        self.draw_traffic_lights(painter)
        
        # 車両を描画
        self.draw_vehicles(painter)
        
        painter.end()
        
    def draw_roads(self, painter):
        road_color = QColor(80, 80, 80)
        # 南北道路
        painter.fillRect(350, 0, 200, 800, road_color)
        # 東西道路
        painter.fillRect(0, 350, 800, 200, road_color)

    def draw_traffic_lights(self, painter):
        # 色の定義
        colors = {
            "赤": Qt.red,
            "黄": Qt.yellow,
            "青": Qt.green
        }
        
        # 南北の信号
        ns_color = colors[self.simulation.ns_light.current_state]
        painter.setBrush(QBrush(ns_color))
        painter.drawEllipse(320, 320, 20, 20) # 北向き用
        painter.drawEllipse(560, 560, 20, 20) # 南向き用

        # 東西の信号
        we_color = colors[self.simulation.we_light.current_state]
        painter.setBrush(QBrush(we_color))
        painter.drawEllipse(560, 320, 20, 20) # 西向き用
        painter.drawEllipse(320, 560, 20, 20) # 東向き用

    def draw_vehicles(self, painter):
        painter.setBrush(QBrush(QColor(100, 150, 200))) # 車両の色
        painter.setPen(Qt.NoPen)
        for v in self.simulation.vehicles:
            if v.road == "NS":
                painter.drawRect(v.x, v.y, v.width, v.height)
            else: # WE
                # 進行方向に応じて車両の向きを変える
                painter.drawRect(v.x, v.y, v.height, v.width)
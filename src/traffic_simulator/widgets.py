# widgets.py
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPolygonF # QPolygonFとQPointFを追加でインポート
from PySide6.QtCore import Qt, QRect, QPointF

class SimulationWidget(QWidget):
    # __init__ と paintEvent は変更なし
    def __init__(self, simulation, parent=None):
        super().__init__(parent)
        self.simulation = simulation

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), Qt.darkGray)
        self.draw_roads(painter)
        self.draw_traffic_lights(painter) # この中で矢印も描画
        self.draw_vehicles(painter)
        painter.end()
        
    # draw_roads は変更なし
    def draw_roads(self, painter):
        road_color = QColor(80, 80, 80)
        painter.fillRect(350, 0, 200, 800, road_color)
        painter.fillRect(0, 350, 800, 200, road_color)

    # draw_traffic_lights メソッドを書き換え
    def draw_traffic_lights(self, painter):
        colors = {"赤": Qt.red, "黄": Qt.yellow, "青": Qt.green}
        
        # --- 南北の信号 ---
        ns_color = colors[self.simulation.ns_light.current_state]
        painter.setBrush(QBrush(ns_color))
        # 北向き用（画面上側、南へ進む車用）の信号
        painter.drawEllipse(320, 320, 20, 20) 
        # 南向き用（画面下側、北へ進む車用）の信号
        painter.drawEllipse(560, 560, 20, 20) 

        # --- 東西の信号 ---
        we_color = colors[self.simulation.we_light.current_state]
        painter.setBrush(QBrush(we_color))
        # 西向き用（画面右側、西へ進む車用）の信号
        painter.drawEllipse(560, 320, 20, 20)
        # 東向き用（画面左側、東へ進む車用）の信号
        painter.drawEllipse(320, 560, 20, 20)

        # --- 矢印の描画 ---
        painter.setBrush(QBrush(Qt.white))
        painter.setPen(Qt.NoPen)

        # 北向き用信号に対する下向き矢印 (▼)
        arrow_n = QPolygonF([QPointF(325, 345), QPointF(335, 345), QPointF(330, 355)])
        painter.drawPolygon(arrow_n)

        # 南向き用信号に対する上向き矢印 (▲)
        arrow_s = QPolygonF([QPointF(565, 555), QPointF(575, 555), QPointF(570, 545)])
        painter.drawPolygon(arrow_s)

        # 西向き用信号に対する左向き矢印 (◄)
        arrow_w = QPolygonF([QPointF(555, 325), QPointF(555, 335), QPointF(545, 330)])
        painter.drawPolygon(arrow_w)

        # 東向き用信号に対する右向き矢印 (►)
        arrow_e = QPolygonF([QPointF(345, 565), QPointF(345, 575), QPointF(355, 570)])
        painter.drawPolygon(arrow_e)

    # draw_vehicles は変更なし
    def draw_vehicles(self, painter):
        painter.setBrush(QBrush(QColor(100, 150, 200)))
        painter.setPen(Qt.NoPen)
        for v in self.simulation.vehicles:
            if v.road == "NS":
                painter.drawRect(v.x, v.y, v.width, v.height)
            else:
                painter.drawRect(v.x, v.y, v.height, v.width)
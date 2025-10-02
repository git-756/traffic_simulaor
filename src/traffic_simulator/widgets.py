from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPolygonF
from PySide6.QtCore import Qt, QRect, QPointF

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
        # 道路の背景
        road_color = QColor(80, 80, 80)
        painter.fillRect(350, 0, 200, 800, road_color) # 南北
        painter.fillRect(0, 350, 800, 200, road_color) # 東西

        # --- 白い点線用のペン ---
        pen_dashed = QPen(Qt.white, 2, Qt.DashLine)
        
        # --- 南北道路の車線 ---
        painter.setPen(pen_dashed)
        painter.drawLine(450, 0, 450, 350) # 交差点手前まで
        painter.drawLine(450, 550, 450, 800) # 交差点後から
        
        # --- 東西道路の車線 ---
        painter.setPen(pen_dashed)
        painter.drawLine(0, 450, 350, 450)
        painter.drawLine(550, 450, 800, 450)
        
        # --- 中央線の描画 (黄色い実線) ---
        pen_solid_yellow = QPen(QColor(255, 200, 0), 3, Qt.SolidLine)
        painter.setPen(pen_solid_yellow)
        # 南北道路の中央線 (交差点は描画しない)
        painter.drawLine(450, 0, 450, 350) # 交差点手前まで
        painter.drawLine(450, 550, 450, 800) # 交差点後から
        # 東西道路の中央線 (交差点は描画しない)
        painter.drawLine(0, 450, 350, 450)
        painter.drawLine(550, 450, 800, 450)


    def draw_traffic_lights(self, painter):
        colors = {"赤": Qt.red, "黄": Qt.yellow, "青": Qt.green}
        
        ns_color = colors[self.simulation.ns_light.current_state]
        painter.setBrush(QBrush(ns_color))
        painter.drawEllipse(320, 320, 20, 20) 
        painter.drawEllipse(560, 560, 20, 20) 

        we_color = colors[self.simulation.we_light.current_state]
        painter.setBrush(QBrush(we_color))
        painter.drawEllipse(560, 320, 20, 20)
        painter.drawEllipse(320, 560, 20, 20)

        painter.setBrush(QBrush(Qt.white))
        painter.setPen(Qt.NoPen)

        arrow_n = QPolygonF([QPointF(325, 345), QPointF(335, 345), QPointF(330, 355)])
        painter.drawPolygon(arrow_n)
        arrow_s = QPolygonF([QPointF(565, 555), QPointF(575, 555), QPointF(570, 545)])
        painter.drawPolygon(arrow_s)
        arrow_w = QPolygonF([QPointF(555, 325), QPointF(555, 335), QPointF(545, 330)])
        painter.drawPolygon(arrow_w)
        arrow_e = QPolygonF([QPointF(345, 565), QPointF(345, 575), QPointF(355, 570)])
        painter.drawPolygon(arrow_e)

    def draw_vehicles(self, painter):
        for v in self.simulation.vehicles:
            # 車両本体の描画
            painter.setBrush(QBrush(QColor(100, 150, 200)))
            painter.setPen(Qt.NoPen)
            painter.drawRect(v.x, v.y, v.draw_width, v.draw_height)

            # --- 車両の中心に進行方向の矢印を描画 ---
            painter.setBrush(QBrush(Qt.white))
            
            # 車両の中心座標 (描画サイズに基づいて計算)
            center_x = v.x + v.draw_width / 2
            center_y = v.y + v.draw_height / 2
            
            arrow = QPolygonF()
            if v.road == "NS":
                if v.direction == 1: # 北向き (▲)
                    arrow.append(QPointF(center_x, center_y - 5))
                    arrow.append(QPointF(center_x - 4, center_y + 3))
                    arrow.append(QPointF(center_x + 4, center_y + 3))
                else: # 南向き (▼)
                    arrow.append(QPointF(center_x, center_y + 5))
                    arrow.append(QPointF(center_x - 4, center_y - 3))
                    arrow.append(QPointF(center_x + 4, center_y - 3))
            else: # WE
                if v.direction == 1: # 東向き (►)
                    arrow.append(QPointF(center_x + 5, center_y))
                    arrow.append(QPointF(center_x - 3, center_y - 4))
                    arrow.append(QPointF(center_x - 3, center_y + 4))
                else: # 西向き (◄)
                    arrow.append(QPointF(center_x - 5, center_y))
                    arrow.append(QPointF(center_x + 3, center_y - 4))
                    arrow.append(QPointF(center_x + 3, center_y + 4))
            
            painter.drawPolygon(arrow)
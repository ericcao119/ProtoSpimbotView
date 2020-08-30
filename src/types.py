from dataclasses import dataclass
from math import cos, sin

from PyQt5.QtCore import QPoint, QPointF, QRect, QRectF, Qt
from PyQt5.QtGui import QBrush, QColor, QImage, QPainter, QPen

from src.config import SCALE, WORLD_SIZE
from src.images import *

QImage()


BOT_RADIUS = 4
BOT_POINTER_LENGTH = 8


@dataclass
class Bot:
    id: int
    x: float
    y: float
    angle: float
    done: bool = False

    def draw(self, painter: QPainter):
        delta_x = (int)(cos(self.angle) * BOT_POINTER_LENGTH)
        delta_y = (int)(sin(self.angle) * BOT_POINTER_LENGTH)

        if self.id == 0:
            color = QColor(0xFF, 0x00, 0x00, 0xFF)
        else:
            color = QColor(0x00, 0x00, 0xFF, 0xFF)

        pen = QPen(color)
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(color)

        painter.setPen(pen)
        painter.setBrush(brush)

        painter.drawPie(
            SCALE(self.x - BOT_RADIUS),
            SCALE(self.y - BOT_RADIUS),
            SCALE(2 * BOT_RADIUS),
            SCALE(2 * BOT_RADIUS),
            0,
            360 * 64,
        )
        pen.setWidth(1)

        painter.drawLine(
            SCALE(self.x),
            SCALE(self.y),
            SCALE(self.x + delta_x),
            SCALE(self.y + delta_y),
        )


@dataclass
class Photon:
    color: int
    x: float
    y: float

    def draw(self, painter: QPainter):
        painter.setRenderHint(QPainter.Antialiasing)

        if self.color == 0:
            color = QColor(0xFF, 0x07, 0x3A, 0xFF)
        elif self.color == 1:
            color = QColor(0x4D, 0x4D, 0xFF, 0xFF)
        else:
            color = QColor(0xDD, 0xD9, 0x2A, 0xFF)

        pen = QPen(color)
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(color)

        painter.setPen(pen)
        painter.setBrush(brush)

        tl = QPointF(SCALE(self.x - 1), SCALE(self.y - 1))
        br = QPointF(SCALE(self.x + 1), SCALE(self.y + 1))

        body = QRectF(tl, br)
        painter.drawPie(body, 0, 360 * 64)


WIDTH = 8
HEIGHT = 8


@dataclass
class Map:
    string: str

    def draw(self, painter: QPainter):
        for r in range(int(WORLD_SIZE / HEIGHT)):
            for c in range(int(WORLD_SIZE / WIDTH)):
                Tile(self.string[r * int(WORLD_SIZE / WIDTH) + c], r, c).draw(painter)
            # print(self.string[r * int(WORLD_SIZE / WIDTH) : (r + 1) * int(WORLD_SIZE / WIDTH)])
            # print()


@dataclass
class Tile:
    variant: str
    row: int
    col: int

    def draw(self, painter: QPainter):
        tl = QPoint(SCALE(self.row * WIDTH), SCALE(self.col * HEIGHT))
        br = QPoint(SCALE((self.row + 1) * WIDTH), SCALE((self.col + 1) * HEIGHT))
        r = QRect(tl, br)
        painter.drawImage(r, self.get_image())

    def get_image(self):
        return {
            "F": test_floor_png,
            "W": test_wall_png,
            "U": test_beacon_png,
            "": test_square_png,
        }[self.variant]

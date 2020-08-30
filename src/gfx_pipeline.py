"""Pipeline for converting spiml config to graphics"""

import subprocess as sp
import sys
from pathlib import Path
from typing import Any, Dict
from math import floor, ceil

import cv2
import numpy as np
import yaml
from PyQt5.Qt import QApplication
from PyQt5.QtCore import QPoint, QPointF, QRect, QRectF, Qt
from PyQt5.QtGui import QColor, QFont, QImage, QPainter, QPainterPath, QPixmap

from src.colors import *
from src.config import (
    CYCLE_LIMIT,
    DRAW_CYCLES,
    FFMPEG_BIN,
    LAB_PART_NUM,
    LABEL_SPACE,
    NUM_CONTEXTS,
    SCALE,
    TEST_PATH,
    WORLD_SIZE,
    DARKEN_CYCLE,
)
from src.spiml import from_yaml
from src.types import *
from src.pipeline import Pipeline

def cycle(frame: int) -> int:
    return frame * DRAW_CYCLES

def count_multiples(start: int, end: int, factor: int) -> int:
    """Returns the number of multiples of within the range start to end, not including end"""
    upper = ceil((start + 1) / factor)
    lower = floor(end / factor)
    return lower - upper + 1

# TODO: Convert to decoratror to allow it to surround a (regular graphics pipeline)
class GFXPipeline:
    def __init__(self):
        self.silent = QApplication([])
        # Static Objects
        self.window: QPixmap = QPixmap(
            SCALE(WORLD_SIZE), SCALE(WORLD_SIZE + LABEL_SPACE)
        )
        self.map: QPixmap = QPixmap(SCALE(WORLD_SIZE), SCALE(WORLD_SIZE))
        self.overlay: QPixmap = QPixmap(
            SCALE(WORLD_SIZE), SCALE(WORLD_SIZE),
        )
        self.overlay.fill(QColor(Qt.transparent))

        command = [
            FFMPEG_BIN,
            "-y",  # (optional) overwrite output file if it exists
            "-f",
            "rawvideo",
            "-pix_fmt",
            # "rgba",
            "rgb24",
            "-s:v",
            f"{int(SCALE(WORLD_SIZE))}x{int(SCALE(WORLD_SIZE + LABEL_SPACE))}",  # size of one frame
            "-r",
            "48",  # frames per second
            "-i",
            "-",  # The input comes from a pipe
            "-an",  # Tells FFMPEG not to expect any audio
            "-g",
            "6",
            "-crf",
            "20",
            "-c:v",
            "libx264",
            "outpy.mp4",
            # "libvpx-vp9",
            # "outpy.webm",
        ]
        # print(" ".join(command))
        self.pipe = sp.Popen(
            command, stdin=sp.PIPE, stderr=sys.stderr.buffer, stdout=sys.stdout.buffer
        )
        self.frame_counter = 0

    def compose_layers(self):
        rect = QRect(0, 0, SCALE(WORLD_SIZE), SCALE(WORLD_SIZE))

        def compose_overlay():
            painter = QPainter(self.map)
            painter.drawPixmap(rect, self.overlay)

        def compose_map():
            painter = QPainter(self.window)
            painter.drawPixmap(rect, self.map)

        compose_overlay()
        compose_map()

    def darken_overlay(self, overlay_painter: QPainter):
        overlay_painter.setCompositionMode(QPainter.CompositionMode_DestinationIn)
        window = QRect(0, 0, SCALE(WORLD_SIZE), SCALE(WORLD_SIZE))
        overlay_painter.fillRect(window, QBrush(QColor(0, 0, 0, 200)))

    def display_text(self, painter: QPainter, pen: QPen, x: int, y: int, string: str):
        if len(string) > 25:
            string = string[:25]
            string[-1] = "."
            string[-2] = "."
            string[-3] = "."

        white_pen = QPen(Qt.white)
        path = QPainterPath()

        white_pen.setWidth(3)
        painter.setPen(white_pen)

        font = QFont()
        font.setPointSize(SCALE(8))
        painter.setFont(font)

        path.addText(SCALE(x - 1), SCALE(y), font, string)
        path.addText(SCALE(x - 1), SCALE(y - 1), font, string)
        path.addText(SCALE(x), SCALE(y - 1), font, string)
        path.addText(SCALE(x), SCALE(y), font, string)

        painter.drawPath(path)
        painter.setPen(pen)
        painter.drawText(SCALE(x), SCALE(y), string)

    def draw_label(self, painter: QPainter, metrics: Dict[str, Any]):
        self.draw_timer(painter)

        text_pen = QPen(lightblack)
        text_pen.setWidth(1)

        font = QFont()
        font.setPointSize(SCALE(8))
        painter.setFont(font)

        # General text
        self.display_text(painter, text_pen, 10, WORLD_SIZE + 10, "Buckets of paint:")
        self.display_text(painter, text_pen, 10, WORLD_SIZE + 25, "Inventory:")
        self.display_text(painter, text_pen, 10, WORLD_SIZE + 40, "Tiles painted:")

        if LAB_PART_NUM == 1 or LAB_PART_NUM == 2:
            self.display_text(painter, text_pen, 10, WORLD_SIZE + 55, "Score:")

        lred_pen = QPen(lightred)
        lblue_pen = QPen(lightblue)

        if cycle(self.frame_counter) >= CYCLE_LIMIT:
            if metrics["Score"][0] != metrics["Score"][1]:
                if metrics["Score"][0] > metrics["Score"][1]:
                    text_pen = lred_pen
                    text = "RED"
                else:
                    text_pen = lblue_pen
                    text = "BLUE"

                self.display_text(painter, text_pen, 260, WORLD_SIZE + 14, text)
                self.display_text(painter, text_pen, 260, WORLD_SIZE + 14 + 11, "WINS!")
            else:
                self.display_text(painter, text_pen, 260, WORLD_SIZE + 14, "TIE!")

        self.display_text(
            painter, lred_pen, 100, WORLD_SIZE + 40, str(metrics["Score"][0])
        )
        self.display_text(
            painter, lblue_pen, 100 + 50, WORLD_SIZE + 40, str(metrics["Score"][1])
        )

    def draw_timer(self, painter: QPainter):
        if CYCLE_LIMIT > 0:
            scaled_time = int(WORLD_SIZE * cycle(self.frame_counter) / CYCLE_LIMIT)
            pen = QPen()
            brush = QBrush(Qt.SolidPattern)

            if scaled_time < WORLD_SIZE / 2:
                pen.setColor(time_low)
                brush.setColor(time_low)
            elif scaled_time < 3 * WORLD_SIZE / 4:
                pen.setColor(time_mid)
                brush.setColor(time_mid)
            else:
                pen.setColor(time_hig)
                brush.setColor(time_hig)
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawRect(SCALE(0), SCALE(WORLD_SIZE + 45), SCALE(scaled_time), SCALE(5))

    def feed(self, document):
        self.window.fill(QColor.fromRgba(0xFFFFFFFF))
        
        n_darken = count_multiples(cycle(self.frame_counter), cycle(self.frame_counter + 1), DARKEN_CYCLE)

        for i in range(n_darken):
            self.darken_overlay(QPainter(self.overlay))

        # Start writing here

        for m in document["Map"]:
            m.draw(QPainter(self.map))

        if "Photons" in document and document["Photons"] is not None:
            for photon in document["Photons"]:
                photon.draw(QPainter(self.overlay))

        for bot in document["Bots"]:
            bot.draw(QPainter(self.map))
        self.draw_label(QPainter(self.window), document["Metrics"])
        self.compose_layers()
        self.frame_counter += 1

        out_image = QImage(self.window).convertToFormat(QImage.Format_RGB888)

        width = out_image.width()
        height = out_image.height()

        ptr = out_image.constBits()
        s = ptr.asstring(width * height * 3)
        arr = np.fromstring(s, dtype=np.uint8).reshape((height, width, 3))

        self.pipe.stdin.write(arr.tobytes())

    def feed_many(self, path: Path):
        for doc in from_yaml(path):
            if doc is not None:
                self.feed(doc)
        self.close()

    def close(self):
        self.pipe.stdin.close()
        self.pipe.wait()


gfx = GFXPipeline()

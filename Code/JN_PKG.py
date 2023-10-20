from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from enum import Enum

# ICON CLASSS
class JN_Icon(QIcon):
    """
    For setting up icon for the JN_SVG_WIDGET class. 

    ## Note:
    Functions that starts with `j` can be use publicly. Only use these functions

    ## Instruction:
    1. Initiate buy calling `__init__(file, pos)`
    
    ## Functions:
    `jgetIcon()`            Returns QIcon\n
    `jgetSize()`            Returns QSize of the image.\n
    `jsetPosition(pos)`     Set position ICON on UI\n
    `jgetSVGFile()`         Returns filepath of image file\n
    `jsetSVGFile(file)`     Sets image of icon\n
    `jgetGeometry()`        Returns geometry attribute.\n
    `jsetGeometry(geo)`     Sets geometry attribute\n

    `Author: Justine Nagdaparan`
    `Date:   2023-10-19 (YYYY-MM-DD)`

    """

    class Type(Enum):
        LOCKED = 0
        UNLOCKED = 1

    
    def __init__(self, file: str, pos: QPoint) -> None:
        """
        Must initiate\n

        file : string -- The real part (default 0.0)
        poa : QPoint -- Coordinate of the icon on the UI
        
        """
        super().__init__(file)
        self.svg_file: str = file
        self.icon_geo: QRect = None
        self.size: QSize = None
        self.jsetPosition(pos)

    # Note: functions that start at j can be use publicly

    def jgetIcon(self) -> QIcon:
        """Returns the QIcon object"""
        return self

    
    def jgetSize(self) -> QSize:
        """
        Returns the actual size of the image.\n
        QSize is a tuple( width, height )
        """
        return self.size

    
    def jsetPosition(self, pos: QPoint) -> None:
        """
        Manually set the position of the ICON on the UI\n
        pos : QPoint -- QPoint(x,y) Coordinate of the icon on the UI
        """
        renderer = QSvgRenderer(self.svg_file)
        self.size = renderer.defaultSize()
        x = pos.x()
        y = pos.y()
        w = self.size.width()
        h = self.size.height()
        self.jsetGeometry(QRect(x, y, w, h))

    def jgetSVGFile(self) -> str:
        """Returns the filepath to the image file"""
        return self.svg_file

    def jsetSVGFile(self, file: str) -> None:
        """Sets the image of the icon manually"""
        self.svg_file = file

    def jgetGeometry(self) -> QRect:
        """
        Returns the geometry obj of the QIcon. \n
        Geometry holds x and y coord and length width size.
        """
        return self.icon_geo

    def jsetGeometry(self, geo: QRect) -> None:
        """
        Manually Sets the geometry attribute of the icon\n
        geo : QRect -- QRect(x,y,w,h)
        """
        self.icon_geo = geo




class JN_SVG_Widget():
    
    def __init__(self, parent=None) -> None:
        self.en_click: bool = True
        self.en_hold: bool = False
        self.en_glow: bool = False
        self.en_glow_anim: bool = False
        self.en_shadow: bool = True
        self.en_scale: bool = False
        self.en_scale_anim: bool = False

        self.glow_upValue: float = 15.0
        self.glow_downValue: float = 0
        self.glow_color: str = "#FFFFFF"
        self.glow_animDuration: int = 200
        self.shadow_color: str = "#292929"
        self.shadow_blur: float = 5.0
        self.shadow_offset: tuple[int, int] = (5, 5)

        self.scale_upValue: QSize = None
        self.scale_downValue: QSize = None
        self.scale_animDuration: int = 200

        self.entrance_duration: int = 500
        self.exit_duration: int = 500

        self.WIDGET = QPushButton(parent)
        self.WIDGET.setFlat(True)
        self.WIDGET.pressed.connect(self.__press__)
        self.WIDGET.released.connect(self.__release__)

        self.geo = QRect(0, 0, 0, 0)
        self.icon: JN_Icon = None
        self.glow = QGraphicsDropShadowEffect(self.WIDGET)
        self.WIDGET.setGraphicsEffect(self.glow)
        self.glow.setOffset(0, 0)
        self.glow.setEnabled(False)
        self.glow_anim = QPropertyAnimation(self.glow, b"blurRadius")
        self.scale_anim = QPropertyAnimation(self.WIDGET, b"iconSize")

        self.j_showShadow()

        self.press_cb = None
        self.release_cb = None
        self.afterEntrance_cb = None
        self.afterExit_cb = None

        self._glow_finSig_connected = False
        self._scale_finSig_connected = False

    def _ignore(): pass

    def _bg_trans(self):
        self.WIDGET.setStyleSheet("background-color: transparent")

    def jn_disconnectSignals(self, sig:pyqtBoundSignal):
        try:
            sig.disconnect()
        except:
            pass

    def j_iconSet(self, icon=None):
        self.icon = icon
        self.WIDGET.setIcon(self.icon.jgetIcon())
        self.WIDGET.setIconSize(self.icon.jgetSize())

        self.scale_upValue = self.icon.jgetSize()
        self.scale_downValue = self.icon.jgetSize()

        self.j_updateGeometry()

    def j_featureSet(
        self,

        glow_onPR=None,
        glow_anim=None,
        glow_upValue=None,
        glow_downValue=None,
        glow_color=None,
        glow_animDuration=None,

        shadow_on=None,
        shadow_color=None,
        shadow_blur=None,
        shadow_offset=None,

        scale_onPR=None,
        scale_anim=None,
        scale_upValue=None,
        scale_downValue=None,
        scale_animDuration=None,

        entrance_duration=None,
        exit_duration=None

    ):

        if glow_onPR is not None:
            self.en_glow = glow_onPR
            self.glow.setBlurRadius(0)
            self.glow.setColor(QColor(self.glow_color))
            self.glow.setEnabled(False)

        if glow_onPR and glow_anim is not None:
            self.en_glow_anim = glow_anim

        if shadow_on is not None:
            self.en_shadow = shadow_on
        if self.en_shadow:
            self.j_showShadow()

        if glow_upValue is not None:
            self.glow_upValue = glow_upValue

        if glow_downValue is not None:
            self.glow_downValue = glow_downValue

        if glow_color is not None:
            self.glow_color = glow_color

        if glow_animDuration is not None:
            self.glow_animDuration = glow_animDuration

        if shadow_color is not None:
            self.shadow_color = shadow_color

        if shadow_blur is not None:
            self.shadow_blur = shadow_blur

        if shadow_offset is not None:
            self.shadow_blur = shadow_offset

        if scale_onPR is not None:
            self.en_scale = scale_onPR

        if self.en_scale and scale_anim is not None:
            self.en_scale_anim = scale_anim

        if scale_upValue is not None:
            self.scale_upValue = scale_upValue
            self.j_updateGeometry()

        if scale_downValue is not None:
            self.scale_downValue = scale_downValue

        if scale_animDuration is not None:
            self.scale_animDuration = scale_animDuration

        if entrance_duration is not None:
            self.entrance_duration = entrance_duration

        if exit_duration is not None:
            self.exit_duration = exit_duration

    def j_updateGeometry(self):
        self.geo = self.icon.jgetGeometry()
        self.geo.setSize(self.scale_upValue)

        increase: QSize = self.scale_upValue - self.icon.jgetSize()

        x = int(self.icon.jgetGeometry().x() - (increase.width() / 2))
        y = int(self.icon.jgetGeometry().y() - (increase.height() / 2))

        self.geo.setX(x)
        self.geo.setY(y)

        self.WIDGET.setGeometry(self.geo)

    def j_showShadow(self):
        if self.en_shadow:
            self.glow.setBlurRadius(self.shadow_blur)
            self.glow.setColor(QColor(self.shadow_color))
            self.glow.setOffset(self.shadow_offset[0], self.shadow_offset[1])
            self.glow.setEnabled(True)

    def j_callbackPress(self, cb=None):
        if cb is None:
            self.press_cb = None
            self.jn_disconnectSignals(self.WIDGET.pressed)
            self.WIDGET.pressed.connect(self._bg_trans)
        else:
            self.jn_disconnectSignals(self.WIDGET.pressed)
            self.WIDGET.pressed.connect(self.__press__)
            self.press_cb = cb

    def j_callbackRelease(self, cb=None):
        if cb is None:
            self.release_cb = None
            self.jn_disconnectSignals(self.WIDGET.released)
        else:
            self.jn_disconnectSignals(self.WIDGET.released)
            self.WIDGET.released.connect(self.__release__)
            self.release_cb = cb

    def j_setEntryExitCallbacks(self, entry=None, exit=None, clear=False):
        if not clear:
            if entry is not None:
                self.afterEntrance_cb = entry
            if exit is not None:
                self.afterExit_cb = exit
        else:
            self.afterEntrance_cb = None
            self.afterExit_cb = None

    def j_enableClick(self, enable=True):
        self.en_click = enable

    def j_bringFront(self):
        self.WIDGET.raise_()

    def __press__(self):

        self._bg_trans()

        if self.en_click:

            if self.en_glow and self.en_glow_anim:
                self.j_animateGlow(
                    blur_start=self.glow_downValue,
                    blur_end=self.glow_upValue,
                    duration=self.glow_animDuration,
                    color=self.glow_color,
                    offset=(0, 0)
                )

            elif self.en_glow:
                self.glow.setBlurRadius(self.glow_upValue)
                self.glow.setColor(self.glow_color)
                self.glow.setOffset(0, 0)
                self.glow.setEnabled(True)

            else:
                if self.en_shadow:
                    self.j_showShadow()

            if self.en_scale and self.en_scale_anim:

                self.j_animateScale(
                    size_end=self.scale_upValue,
                    duration=self.scale_animDuration
                )

            try:
                self.press_cb()
            except:
                pass

    def __release__(self):

        if self.en_click:

            if self.en_glow and self.en_glow_anim:
                self.j_animateGlow(
                    blur_end=self.glow_downValue,
                    duration=self.glow_animDuration,
                    color=self.glow_color,
                    offset=(0, 0),
                    animFinish_cb=self.j_showShadow
                )
            elif self.en_glow:
                self.glow.setBlurRadius(self.glow_downValue)
                self.glow.setColor(self.glow_color)
                self.glow.setOffset(0, 0)
                self.glow.setEnabled(True)

            if self.en_shadow and not self.en_glow_anim:
                self.j_showShadow()

            if self.en_scale and self.en_scale_anim:
                self.j_animateScale(
                    size_end=self.scale_downValue,
                    duration=self.scale_animDuration
                )

            try:
                self.release_cb()
            except:
                pass

    def j_animateGlow(
        self,
        blur_start=None,
        blur_end=15.0,
        duration=200,
        color="#FFFFFF",
        offset=(0, 0),
        animFinish_cb=None
    ):

        if blur_start is None:
            blur_start = self.glow.blurRadius()

        self.glow.setColor(QColor(color))
        self.glow.setOffset(offset[0], offset[1])
        self.glow.setEnabled(True)

        self.glow_anim.stop()
        self.glow_anim.setDuration(duration)
        self.glow_anim.setStartValue(blur_start)
        self.glow_anim.setEndValue(blur_end)

        self.jn_disconnectSignals(self.glow_anim.finished)
        if animFinish_cb is not None:
            self.glow_anim.finished.connect(animFinish_cb)

        self.glow_anim.start()

    def j_animateScale(
        self,
        size_end=None,
        duration=200,
        animFinish_cb=None
    ):
        if size_end is None:
            size_end = self.scale_upValue
        self.scale_anim.stop()
        self.scale_anim.setEasingCurve(QEasingCurve.Linear)
        self.scale_anim.setDuration(duration)
        self.scale_anim.setStartValue(self.WIDGET.iconSize())
        self.scale_anim.setEndValue(size_end)

        self.jn_disconnectSignals(self.scale_anim.finished)
        if animFinish_cb is not None:
            self.scale_anim.finished.connect(animFinish_cb)

        self.scale_anim.start()

    def j_Entrance(self, animate=False):

        if animate:
            self.j_animateScale(
                size_end=self.icon.jgetSize(),
                duration=self.entrance_duration,
                animFinish_cb=self.afterEntrance_cb
            )
        else:
            if self.en_shadow:
                self.j_showShadow()
            self.WIDGET.setIconSize(self.icon.jgetSize())

            self.jn_disconnectSignals(self.scale_anim.finished)
            self.jn_disconnectSignals(self.glow_anim.finished)
            try:
                self.afterEntrance_cb
            except:
                pass

    def j_Exit(self, animate=False):

        if animate:
            self.j_animateScale(
                size_end=QSize(0, 0),
                duration=self.exit_duration,
                animFinish_cb=self.afterExit_cb
            )
        else:
            self.glow_anim.stop()
            self.scale_anim.stop()

            self.WIDGET.setIconSize(QSize(0, 0))

            self.jn_disconnectSignals(self.scale_anim.finished)
            self.jn_disconnectSignals(self.glow_anim.finished)

            try:
                self.afterExit_cb
            except:
                pass

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGraphicsEffect, QGraphicsBlurEffect, QGraphicsDropShadowEffect
from PySide6.QtCore import QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor


class CombinedEffect(QGraphicsEffect):
    def __init__(self, effect1, effect2, parent=None):
        super().__init__(parent)
        self.effect1 = effect1
        self.effect2 = effect2

    def draw(self, painter):
        if self.effect1:
            self.effect1.draw(painter)
        if self.effect2:
            self.effect2.draw(painter)

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setGeometry(100, 100, 400, 200)
    window.setWindowTitle("Animate Combined QGraphicsEffect")

    # Create a QWidget
    widget = QWidget(window)
    widget.setGeometry(100, 50, 200, 100)

    # Create two QGraphicsEffects
    blur_effect = QGraphicsBlurEffect()
    blur_effect.setBlurRadius(5)

    shadow_effect = QGraphicsDropShadowEffect()
    shadow_effect.setBlurRadius(10)
    shadow_effect.setColor(QColor(0, 0, 0, 127))
    shadow_effect.setOffset(5, 5)

    # Combine the effects into a custom CombinedEffect
    combined_effect = CombinedEffect(blur_effect, shadow_effect)

    # Apply the custom CombinedEffect to the widget
    widget.setGraphicsEffect(combined_effect)

    # Create an animation to change the blur radius and shadow offset over time
    animation = QPropertyAnimation(combined_effect, b"effect1.blurRadius")
    animation.setDuration(2000)  # Animation duration in milliseconds (2 seconds)
    animation.setStartValue(5)
    animation.setEndValue(20)
    animation.setEasingCurve(QEasingCurve.Type.Linear)

    # Start the animation
    animation.start()

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

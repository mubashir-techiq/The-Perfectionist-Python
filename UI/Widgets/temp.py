import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QScrollArea
from PyQt5.uic import loadUi


class Appointment2(QWidget):
    def __init__(self, price, name, gender):
        super(Appointment2, self).__init__()
        loadUi('Widgets/Appointment 2.ui', self)
        self.price.setText(price)
        self.name.setText(name)
        self.gender.setText(gender)


class Form(QWidget):
    def __init__(self):
        super(Form, self).__init__()

        # Create a QVBoxLayout to hold the Appointment2 widgets
        layout = QVBoxLayout()

        # Create a QScrollArea and set the layout as its widget
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_widget.setLayout(layout)
        scroll_area.setWidget(scroll_widget)

        # Add 10 Appointment2 widgets to the layout
        for i in range(10):
            appointment = Appointment2(f"Price {i+1}", f"Name {i+1}", f"Gender {i+1}")
            layout.addWidget(appointment)

        # Set the scroll area as the main layout of the form
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())

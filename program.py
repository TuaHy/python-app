from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
import sys
class Alert(QMessageBox): #kế thừa
    def error_message(self, title, message):
        self.setIcon(QMessageBox.Icon.Critical)
        self.setWindowTitle(title)
        self.setText(message)
        self.exec()

    def success_message(self, title, message):
        self.setIcon(QMessageBox.Icon.Information)
        self.setWindowTitle(title)
        self.setText(message)
        self.exec()

class Login(QWidget): # kế thừa
    def __init__(self): #khởi tạo đối tượng
        super().__init__() # gọi phương thức khởi tạo của lớp cha (super trả về lớp cha là QWidget)
        uic.loadUi("ui/login.ui", self)

        self.email_input = self.findChild(QLineEdit, "txt_email")
        self.password_input = self.findChild(QLineEdit, "txt_password")
        self.btn_login = self.findChild(QPushButton, "btn_login")
        self.btn_register = self.findChild(QPushButton, "btn_register")
        self.btn_eye = self.findChild(QPushButton, "btn_eye")

        self.btn_eye.clicked.connect(lambda: self.show_password(self.btn_eye, self.password_input)) #lambda là Dùng để truyền tham số vào hàm xử lý sự kiện
        self.btn_login.clicked.connect(self.login)
        self.btn_register.clicked.connect(self.show_register)

    def show_password(self, button: QPushButton, input: QLineEdit):
        if input.echoMode() == QLineEdit.EchoMode.Password:
            input.setEchoMode(QLineEdit.EchoMode.Normal)
            button.setIcon(QIcon("img/eye-solid.svg"))
        else:
            input.setEchoMode(QLineEdit.EchoMode.Password)
            button.setIcon(QIcon("img/eye-slash-solid.svg"))
    
    def login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if email == "":
            msg.error_message("Login", "Email is required")
            self.email_input.setFocus()
            return

        if password == "":
            msg.error_message("Login", "Password is required")
            self.password_input.setFocus()
            return

        with open("data/users.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                if data[0] == email and data[1] == password:
                    msg.success_message("Login", "Welcome to the system")
                    self.show_home(email)
                    return
        
        msg.error_message("Login", "Invalid email or password")
        self.email_input.setFocus()

    def show_register(self):
        self.register = Register()
        self.register.show()

    def show_home(self, email):
        self.home = Home(email)
        self.home.show()

class  Register(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/register.ui", self)

        self.email_input = self.findChild(QLineEdit, "txt_email")
        self.password_input = self.findChild(QLineEdit, "txt_password")
        self.name_input = self.findChild(QLineEdit, "txt_name")
        self.confirm_password_input = self.findChild(QLineEdit, "txt_confirm_password")
        self.btn_login = self.findChild(QPushButton, "btn_login") 
        self.btn_register = self.findChild(QPushButton, "btn_register") 
        self.btn_eye_p = self.findChild(QPushButton, "btn_eye_p")    
        self.btn_eye_cp = self.findChild(QPushButton, "btn_eye_cp")

        self.btn_eye_p.clicked.connect(lambda: self.show_password(self.btn_eye_p, self.password_input))
        self.btn_eye_cp.clicked.connect(lambda: self.show_password(self.btn_eye_cp, self.confirm_password_input))
        self.btn_register.clicked.connect(self.register)
        self.btn_login.clicked.connect(self.show_login)

    def show_password(self, button: QPushButton, input: QLineEdit):
        if input.echoMode() == QLineEdit.EchoMode.Password:
            input.setEchoMode(QLineEdit.EchoMode.Normal)
            button.setIcon(QIcon("img/eye-solid.svg"))
        else:
            input.setEchoMode(QLineEdit.EchoMode.Password)
            button.setIcon(QIcon("img/eye-slash-solid.svg"))

    def register(self):
        email = self.email_input.text().strip()
        name = self.name_input.text().strip()
        password = self.password_input.text().strip()
        confirm_pass = self.confirm_password_input.text().strip()

        if email == "":
            msg.error_message("Register", "Email is required")
            self.email_input.setFocus()
            return
        
        if name == "":
            msg.error_message("Register", "Name is required")
            self.name_input.setFocus()
            return
        
        if password == "":
            msg.error_message("Register", "Password is required")
            self.password_input.setFocus()
            return
        
        if confirm_pass == "":
            msg.error_message("Register", "Confirm password is required")
            self.confirm_password_input.setFocus()
            return
        
        with open("data/users.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                if data[0] == email:
                    msg.error_message("Register", "Email already exists")
                    self.email_input.setFocus()
                    return
        with open("data/users.txt", "a") as file:
            file.write(f"{email},{password},{name}\n")
        msg.success_message("Register", "Account created successfully")
        self.show_login()

    def show_login(self):
        self.login = Login()
        self.login.show()

class Home(QWidget):
    def __init__(self, email):
        super().__init__()
        uic.loadUi("ui/Home.ui",self)

        self.email = email
        self.stack_widget = self.findChild(QStackedWidget, "stackedWidget")
        self.btn_home = self.findChild(QPushButton, "btn_home")
        self.btn_profile = self.findChild(QPushButton, "btn_profile")
        self.btn_list = self.findChild(QPushButton, "btn_list")
        self.btn_search = self.findChild(QPushButton, "btn_search")
        self.btn_booking = self.findChild(QPushButton, "btn_booking")

        self.btn_home.clicked.connect(lambda: self.navigate_screen(self.stack_widget, 0))
        self.btn_list.clicked.connect(lambda: self.navigate_screen(self.stack_widget, 1))
        self.btn_search.clicked.connect(lambda: self.navigate_screen(self.stack_widget, 1))
        self.btn_profile.clicked.connect(lambda: self.navigate_screen(self.stack_widget, 2))
        self.btn_booking.clicked.connect(lambda: self.navigate_screen(self.stack_widget, 3))


    def navigate_screen(self, stackWidget: QStackedWidget, index: int):
        stackWidget.setCurrentIndex(index)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    msg = Alert()
    login = Login()
    login.show()
    app.exec()
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
import sys
import json
from data_io import *

class ItemWidget(QWidget):
    def __init__(self, data=None):
        super().__init__()
        uic.loadUi("ui/item.ui", self)
        
        # Store data
        self.data = data
        
        # Find child widgets - only the essential ones
        self.lb_name = self.findChild(QLabel, "lb_name")
        self.lb_image = self.findChild(QLabel, "lb_image")
        self.lb_rating = self.findChild(QLabel, "lb_rating")
        self.lb_price = self.findChild(QLabel, "lb_price")
        self.lb_icon_star = self.findChild(QLabel, "lb_icon_star")
        self.btn_detail = self.findChild(QPushButton, "btn_detail")
        self.btn_booking = self.findChild(QPushButton, "btn_booking")
        

        
        # Connect signals only if buttons exist
        if self.btn_detail:
            self.btn_detail.clicked.connect(self.show_detail)
        if self.btn_booking:
            self.btn_booking.clicked.connect(self.booking)
        
        # Apply beautiful styling
        # self.apply_styling()
        
        # Set data if provided
        if data:
            self.set_data(data)
    
    def apply_styling(self):
        """Apply beautiful CSS styling to the widget"""
        # Main widget styling
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 15px;
                border: 2px solid #e0e0e0;
            }
            QWidget:hover {
                border: 2px solid #4CAF50;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
        """)
        
        # Style for name label
        if self.lb_name:
            self.lb_name.setStyleSheet("""
                QLabel {
                    color: #2E7D32;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 10px;
                    background-color: transparent;
                }
            """)
        
        # Style for image label
        if self.lb_image:
            self.lb_image.setStyleSheet("""
                QLabel {
                    border-radius: 10px;
                    border: 1px solid #e0e0e0;
                    background-color: #f5f5f5;
                }
            """)
        
        # Style for rating label
        if self.lb_rating:
            self.lb_rating.setStyleSheet("""
                QLabel {
                    color: #FF9800;
                    font-size: 14px;
                    font-weight: bold;
                    background-color: transparent;
                }
            """)
        
        # Style for price label
        if self.lb_price:
            self.lb_price.setStyleSheet("""
                QLabel {
                    color: #E91E63;
                    font-size: 14px;
                    font-weight: bold;
                    background-color: transparent;
                }
            """)
        
        # Style for buttons
        if self.btn_detail:
            self.btn_detail.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 8px 16px;
                    font-weight: bold;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
                QPushButton:pressed {
                    background-color: #0D47A1;
                }
            """)
        
        if self.btn_booking:
            self.btn_booking.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 8px 16px;
                    font-weight: bold;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #388E3C;
                }
                QPushButton:pressed {
                    background-color: #2E7D32;
                }
            """)
    
    def set_data(self, data):
        """Set data for the item widget"""
        self.data = data
        
        try:
            # Set name if label exists
            if self.lb_name:
                self.lb_name.setText(data.get("name", ""))
            
            # Set image if label exists
            if self.lb_image:
                image_path = data.get("image", "")
                if image_path:
                    pixmap = QPixmap(image_path)
                    if not pixmap.isNull():
                        self.lb_image.setPixmap(pixmap)
            
            # Set rating if label exists
            if self.lb_rating:
                rating = data.get("rating", 0)
                self.lb_rating.setText(f"{rating}/5")
            
            # Set price if label exists
            if self.lb_price:
                price = data.get("price", "")
                self.lb_price.setText(price)
            
            # Set star icon if label exists
            if self.lb_icon_star:
                star_path = "img/star-solid.svg"
                star_pixmap = QPixmap(star_path)
                if not star_pixmap.isNull():
                    self.lb_icon_star.setPixmap(star_pixmap)
                    
        except Exception as e:
            print(f"Error setting data in ItemWidget: {e}")
            import traceback
            traceback.print_exc()
    
    def show_detail(self):
        """Show detail page for this item"""
        if self.data:
            try:
                # Find the Home widget in the widget hierarchy
                parent = self.parent()
                while parent and not hasattr(parent, 'show_detail_page'):
                    parent = parent.parent()
                if parent:
                    parent.show_detail_page(self.data)
                else:
                    print("Could not find Home widget with show_detail_page method")
            except Exception as e:
                print(f"Error in show_detail: {e}")
    
    def booking(self):
        """Handle booking for this item"""
        if self.data:
            try:
                # Find the Home widget in the widget hierarchy
                parent = self.parent()
                while parent and not hasattr(parent, 'handle_booking'):
                    parent = parent.parent()
                if parent:
                    parent.handle_booking(self.data)
                else:
                    print("Could not find Home widget with handle_booking method")
            except Exception as e:
                print(f"Error in booking: {e}")

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
                
        user = get_user_by_email_and_password(email, password)
        if user:
            msg.success_message("Login", "Welcome to the system")
            self.show_home(user["id"])
            self.close()
            return
        
        msg.error_message("Login", "Invalid email or password")
        self.email_input.setFocus()

    def show_register(self):
        self.register = Register()
        self.register.show()
        self.close()

    def show_home(self, id):
        self.home = Home(id)
        self.home.show()
        self.close()

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
                
        user = get_user_by_email(email)
        if user:
            msg.error_message("Register", "Email already exits")
            self.email_input.setFocus()
            return
        
        create_user(email, password, name)
        msg.success_message("Register", "Account created successfully")
        self.show_login()

    def show_login(self):
        self.login = Login()
        self.login.show()
        self.close()

class Home(QWidget):
    def __init__(self, id):
        super().__init__()
        self.id = id

        uic.loadUi("ui/Home.ui", self)

        self.id = id
        self.user = get_user_by_id(id)
        self.load_user_info()
        
        # Find main widgets
        self.stack_widget = self.findChild(QStackedWidget, "stackedWidget")
        
        # Find buttons
        self.btn_home = self.findChild(QPushButton, "btn_home")
        self.btn_list = self.findChild(QPushButton, "btn_list")
        self.btn_search = self.findChild(QPushButton, "btn_search")
        self.btn_profile = self.findChild(QPushButton, "btn_profile")
        self.btn_booking = self.findChild(QPushButton, "btn_booking")
        self.btn_save_account = self.findChild(QPushButton, "btn_save_account")
        self.btn_avatar = self.findChild(QPushButton, "btn_avatar")
        
        # Find user input fields
        self.txt_name = self.findChild(QLineEdit, "txt_name")
        self.txt_email = self.findChild(QLineEdit, "txt_email")
        self.txt_birthday = self.findChild(QDateEdit, "txt_birthday")
        self.txt_gender = self.findChild(QComboBox, "txt_gender")

        # Connect button signals
        self.btn_home.clicked.connect(lambda: self.navigate_screen(self.stack_widget, 0))
        self.btn_list.clicked.connect(lambda: self.navigate_to_list())
        self.btn_search.clicked.connect(lambda: self.navigate_screen(self.stack_widget, 1))
        self.btn_profile.clicked.connect(lambda: self.navigate_screen(self.stack_widget, 2))
        self.btn_booking.clicked.connect(lambda: self.navigate_screen(self.stack_widget, 3))
        self.btn_avatar.clicked.connect(self.update_avatar)
        self.btn_save_account.clicked.connect(self.update_user_info)
        
        # Initialize variables
        self.scroll_area = None
        self.scroll_layout = None
        self.scroll_area_setup_done = False
        


    def navigate_screen(self, stackWidget: QStackedWidget, index: int):
        stackWidget.setCurrentIndex(index)
    
    def navigate_to_list(self):
        """Navigate to list page and ensure data is loaded"""

        self.navigate_screen(self.stack_widget, 1)
        
        # Find scroll area in the list page
        if not self.scroll_area:
            self.find_scroll_area()
        
        # Load football fields when navigating to list page
        self.load_football_fields()

    def find_scroll_area(self):
        """Find the scroll area in the list page"""
        # Get the list page widget (index 1)
        list_page = self.stack_widget.widget(1)
        if list_page:
            # Find scroll area within the list page
            self.scroll_area = list_page.findChild(QScrollArea, "scrollArea")
            if self.scroll_area:
                # Setup scroll area
                self.setup_scroll_area()

    def load_user_info(self):
        self.user = get_user_by_id(self.id)
        self.txt_name.setText(self.user["name"])
        self.txt_email.setText(self.user["email"])
        self.txt_birthday.setDate(QDate.fromString(self.user["birthday"], "dd/MM/yyyy"))
        self.txt_gender.setCurrentText(self.user["gender"])
        self.btn_avatar.setIcon(QIcon(self.user["avatar"]))

    def update_avatar(self):
        file,_ = QFileDialog.getOpenFileName(self,"Select Image","","Image Files(*.png *.jpg *jpeg *.bmp)")
        if file:
            self.user["avatar"] = file
            self.btn_avatar.setIcon(QIcon(file))
            update_user_avatar(self.id, file)
            msg.success_message("Update", "Avatar updated successfully")

    def update_user_info(self):
        name = self.txt_name.text().strip()
        birthday = self.txt_birthday.date().toString("dd/MM/yyyy")
        gender = self.txt_gender.currentText()
        update_user(self.id, name, birthday, gender)    
        msg.success_message("Update", "User info updated successfully")
        self.load_user_info()
    
    def setup_scroll_area(self):
        """Setup scroll area for football fields list"""
        if not self.scroll_area:
            return False
            
        # Check if already set up
        if hasattr(self, 'scroll_area_setup_done') and self.scroll_area_setup_done:
            return True
            
        # Get the scroll area widget contents
        self.scroll_content = self.scroll_area.findChild(QWidget, "scrollAreaWidgetContents")
        if self.scroll_content:
            # Check if widget already has a layout
            if self.scroll_content.layout():
                # Remove existing layout
                old_layout = self.scroll_content.layout()
                self.scroll_content.setLayout(None)
                if old_layout:
                    old_layout.deleteLater()
            
            # Create new grid layout for the scroll content (2 columns)
            self.scroll_layout = QGridLayout(self.scroll_content)
            self.scroll_layout.setSpacing(30)  # Increased spacing between items
            self.scroll_layout.setContentsMargins(30, 30, 30, 30)  # Increased margins
            
            # Set size policy for scroll content
            self.scroll_content.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            
            # Ensure scroll area is properly configured
            self.scroll_area.setWidgetResizable(True)
            self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            self.scroll_area_setup_done = True
            return True
        else:
            return False
    
    def load_football_fields(self):
        """Load football fields data and create item widgets"""
        try:
            # Ensure scroll area is found and set up
            if not self.scroll_area:
                self.find_scroll_area()
            
            if not self.scroll_area:
                return
                
            # Ensure scroll area is set up
            if not self.scroll_area_setup_done:
                setup_success = self.setup_scroll_area()
                if not setup_success:
                    return
            
            # Check if scroll layout is available
            if not hasattr(self, 'scroll_layout') or self.scroll_layout is None:
                return
                
            # Load data using data_io functions
            try:
                football_fields = load_football_fields()
            except Exception as e:
                return
            
            # Clear existing items
            for i in reversed(range(self.scroll_layout.count())):
                widget = self.scroll_layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()
            
            # Create item widgets
            widgets_created = 0
            row = 0
            col = 0
            max_cols = 2  # 2 columns
            
            for field_data in football_fields:
                try:
                    item_widget = ItemWidget(field_data)
                    if item_widget:
                        # Set size policy for item widget
                        item_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                        item_widget.setMinimumHeight(400)  # Increased height for better appearance
                        item_widget.setMinimumWidth(450)   # Set minimum width
                        
                        # Add to grid layout
                        self.scroll_layout.addWidget(item_widget, row, col)
                        
                        # Move to next position
                        col += 1
                        if col >= max_cols:
                            col = 0
                            row += 1
                        
                        widgets_created += 1
                except Exception as e:
                    import traceback
                    traceback.print_exc()
            
            # Add stretch to push items to top (QGridLayout doesn't have addStretch)
            # Instead, add an empty widget that expands
            stretch_widget = QWidget()
            stretch_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.scroll_layout.addWidget(stretch_widget, row, 0, 1, max_cols)  # Span all columns
            
            # Force layout update
            self.scroll_content.updateGeometry()
            self.scroll_area.updateGeometry()
                
        except Exception as e:
            import traceback
            traceback.print_exc()
    
    def show_detail_page(self, field_data):
        """Show detail page for selected football field"""
        # Navigate to detail page (index 3)
        self.navigate_screen(self.stack_widget, 3)
        # TODO: Update detail page with field_data
    
    def handle_booking(self, field_data):
        """Handle booking for selected football field"""
        try:
            # Simple booking message for now
            msg.success_message("Booking", f"Booking request sent for {field_data.get('name', 'Unknown field')}")
        except Exception as e:
            msg.error_message("Booking", "An error occurred while processing your booking")
    
    def search_football_fields(self, query, search_type="name"):
        """Search football fields using data_io functions"""
        try:
            results = search_football_fields(query, search_type)
            return results
        except Exception as e:
            return []
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    msg = Alert()
    home = Home(1)
    home.show()
    app.exec()
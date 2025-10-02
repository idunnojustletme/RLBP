
from PySide6 import QtWidgets

from config_lib import load_config, save_config, default_config

class ConfigEditorWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Configuration")
        self.setGeometry(200, 200, 500, 600)
        self.setModal(True)
        
        try:
            with open("config.yaml", "r") as file:
                self.config_data = load_config()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load config: {e}. Loading default config.")
            self.config_data = default_config
        
        self.setup_ui()
    
    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        
        form_layout = QtWidgets.QFormLayout()
        
        config = self.config_data.copy()
        
        self.inputs = {}
       
        self.inputs["intiface_ip"] = QtWidgets.QLineEdit(config.get("intiface_ip", "ws://127.0.0.1:12345"))
        form_layout.addRow("Intiface IP:", self.inputs["intiface_ip"])
        
        self.inputs["min_vibe_strength"] = QtWidgets.QSpinBox()
        self.inputs["min_vibe_strength"].setRange(0, 100)
        self.inputs["min_vibe_strength"].setValue(config.get("min_vibe_strength", 20))
        form_layout.addRow("Min Vibe Strength (%):", self.inputs["min_vibe_strength"])
        
        self.inputs["max_vibe_strength"] = QtWidgets.QSpinBox()
        self.inputs["max_vibe_strength"].setRange(0, 100)
        self.inputs["max_vibe_strength"].setValue(config.get("max_vibe_strength", 100))
        form_layout.addRow("Max Vibe Strength (%):", self.inputs["max_vibe_strength"])
        
        self.inputs["min_vibe_time"] = QtWidgets.QDoubleSpinBox()
        self.inputs["min_vibe_time"].setRange(0.1, 60.0)
        self.inputs["min_vibe_time"].setSingleStep(0.1)
        self.inputs["min_vibe_time"].setValue(config.get("min_vibe_time", 0.5))
        form_layout.addRow("Min Vibe Time (s):", self.inputs["min_vibe_time"])
        
        self.inputs["max_vibe_time"] = QtWidgets.QDoubleSpinBox()
        self.inputs["max_vibe_time"].setRange(0.1, 20.0)
        self.inputs["max_vibe_time"].setSingleStep(0.1)
        self.inputs["max_vibe_time"].setValue(config.get("max_vibe_time", 20.0))
        form_layout.addRow("Max Vibe Time (s):", self.inputs["max_vibe_time"])
        
        self.inputs["vibe_strength_divider"] = QtWidgets.QDoubleSpinBox()
        self.inputs["vibe_strength_divider"].setRange(0.1, 10.0)
        self.inputs["vibe_strength_divider"].setSingleStep(0.1)
        self.inputs["vibe_strength_divider"].setValue(config.get("vibe_strength_divider", 1.5))
        form_layout.addRow("Vibe Strength Divider:", self.inputs["vibe_strength_divider"])
        
        self.inputs["vibe_time_divider"] = QtWidgets.QSpinBox()
        self.inputs["vibe_time_divider"].setRange(1, 100)
        self.inputs["vibe_time_divider"].setValue(config.get("vibe_time_divider", 25))
        form_layout.addRow("Vibe Time Divider:", self.inputs["vibe_time_divider"])
        
        self.inputs["min_vibe_score"] = QtWidgets.QSpinBox()
        self.inputs["min_vibe_score"].setRange(0, 1000)
        self.inputs["min_vibe_score"].setValue(config.get("min_vibe_score", 10))
        form_layout.addRow("Min Vibe Score:", self.inputs["min_vibe_score"])
        
        layout.addLayout(form_layout)
        
        reset_button = QtWidgets.QPushButton("Reset to Default")
        reset_button.clicked.connect(self.reset_to_default)
        
        button_layout = QtWidgets.QHBoxLayout()
        
        save_button = QtWidgets.QPushButton("Save and reload")
        save_button.clicked.connect(self.save_config)
        
        cancel_button = QtWidgets.QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        layout.addWidget(reset_button)
    
    def reset_to_default(self):
        reply = QtWidgets.QMessageBox.question(
            self, 
            "Reset to Default", 
            "Are you sure you want to reset all values to default?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            self.inputs["intiface_ip"].setText(default_config["intiface_ip"])
            self.inputs["min_vibe_strength"].setValue(default_config["min_vibe_strength"])
            self.inputs["max_vibe_strength"].setValue(default_config["max_vibe_strength"])
            self.inputs["min_vibe_time"].setValue(default_config["min_vibe_time"])
            self.inputs["max_vibe_time"].setValue(default_config["max_vibe_time"])
            self.inputs["vibe_strength_divider"].setValue(default_config["vibe_strength_divider"])
            self.inputs["vibe_time_divider"].setValue(default_config["vibe_time_divider"])
            self.inputs["min_vibe_score"].setValue(default_config["min_vibe_score"])
    
    def save_config(self):
        config = {}
        
        config["intiface_ip"] = self.inputs["intiface_ip"].text()
        config["min_vibe_strength"] = self.inputs["min_vibe_strength"].value()
        config["max_vibe_strength"] = self.inputs["max_vibe_strength"].value()
        config["min_vibe_time"] = self.inputs["min_vibe_time"].value()
        config["max_vibe_time"] = self.inputs["max_vibe_time"].value()
        config["vibe_strength_divider"] = self.inputs["vibe_strength_divider"].value()
        config["vibe_time_divider"] = self.inputs["vibe_time_divider"].value()
        config["min_vibe_score"] = self.inputs["min_vibe_score"].value()
        
        if save_config(config):
          QtWidgets.QMessageBox.information(self, "Success", "Configuration saved successfully!")
          self.accept()
        else:
          QtWidgets.QMessageBox.critical(self, "Error", f"Failed to save config")
          
# Import built-in modules
import os

import maya.cmds as cmds
import pymel.core as pmc

import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

# Import third-party modules
from PySide2 import QtCore, QtGui, QtWidgets

import importlib as imp
import functions
imp.reload(functions)

tool_name = "Clean Export"
version = "0.1"


class SanityCheckWidget(QtWidgets.QWidget):
    """
    Custom Qt Widget to show the state of a given Sanity check
    """

    def __init__(self, name="Default Check", check_id=0):
        super(SanityCheckWidget, self).__init__()

        self.name = name
        self.id = check_id

        layout = QtWidgets.QHBoxLayout()
        self.lbl_name = QtWidgets.QLabel(name)
        self.lbl_name.setAlignment(QtCore.Qt.AlignLeft)
        layout.addWidget(self.lbl_name)

        self.cbx_state_display = QtWidgets.QCheckBox()
        self.cbx_state_display.setEnabled(False)
        layout.addWidget(self.cbx_state_display)

        self.setLayout(layout)

    def set_lbl_text(self, text="Sanity Check"):
        self.lbl_name.setText(text)

    def set_sanity_state(self, state=True):
        if state:
            self.cbx_state_display.setChecked(True)
            self.lbl_name.setStyleSheet("color: rgb(77, 187, 237);")
        else:
            self.cbx_state_display.setChecked(False)
            self.lbl_name.setStyleSheet("")



class Ui_clean_export_generatorWindow(object):
    def setupUi(self, clean_export_generatorWindow):

        clean_export_generatorWindow.setObjectName("clean_export_generatorWindow")
        clean_export_generatorWindow.resize(600, 300)

        self.build_default_header(clean_export_generatorWindow)

        self.build_help()

        # Tool Specific UI

        self.gL_main_grp = QtWidgets.QGridLayout()
        self.gL_main_grp.setObjectName("gL_source")


        self.lbl_main_grp = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_main_grp.setFont(font)
        self.lbl_main_grp.setAlignment(
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        )
        self.lbl_main_grp.setObjectName("lbl_main_grp")
        self.gL_main_grp.addWidget(self.lbl_main_grp, 0, 0)

        self.le_source_obj = QtWidgets.QLineEdit(self.centralwidget)
        self.le_source_obj.setMinimumSize(QtCore.QSize(250, 30))
        self.le_source_obj.setAlignment(
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        )
        #self.le_source_obj.setDragEnabled(True)
        self.le_source_obj.setObjectName("le_source_obj")
        #self.le_source_obj.setEnabled(False)
        self.gL_main_grp.addWidget(self.le_source_obj, 1, 0)

        self.btn_add_sel = QtWidgets.QPushButton(self.centralwidget)
        self.btn_add_sel.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_add_sel.setObjectName("btn_add_sel")
        self.gL_main_grp.addWidget(self.btn_add_sel, 1, 1)

        self.verticalLayout.addLayout(self.gL_main_grp)

        spacerItem4 = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        self.gL_main_grp.addItem(spacerItem4, 2, 0)

        self.lbl_export_path = QtWidgets.QLabel("Export Path")
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_export_path.setFont(font)
        self.lbl_export_path.setAlignment(
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        )
        self.lbl_export_path.setObjectName("lbl_main_grp")
        self.gL_main_grp.addWidget(self.lbl_export_path, 3, 0)

        self.le_export_path = QtWidgets.QLineEdit(self.centralwidget)
        self.le_export_path.setMinimumSize(QtCore.QSize(250, 30))
        self.le_export_path.setAlignment(
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        )
        #self.le_export_path.setDragEnabled(True)
        self.le_export_path.setObjectName("le_export_path")
        #self.le_source_obj.setEnabled(False)
        self.gL_main_grp.addWidget(self.le_export_path, 4, 0)

        self.btn_export_path = QtWidgets.QToolButton()
        self.btn_export_path.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_export_path.setIcon(self.btn_export_path.style().standardIcon(QtWidgets.QStyle.SP_DialogOpenButton))
        self.btn_export_path.setObjectName("btn_export_path")
        self.set_export_path()

        self.gL_main_grp.addWidget(self.btn_export_path, 4, 1)

        self.verticalLayout.addLayout(self.gL_main_grp)

        spacerItem5 = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        self.verticalLayout.addItem(spacerItem5)


        self.horizontalLineTop = QtWidgets.QFrame(self.centralwidget)
        self.horizontalLineTop.setFrameShadow(QtWidgets.QFrame.Plain)
        self.horizontalLineTop.setFrameShape(QtWidgets.QFrame.HLine)
        self.horizontalLineTop.setObjectName("horizontalLineTop")
        self.verticalLayout.addWidget(self.horizontalLineTop)

        spacerItem5 = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        self.verticalLayout.addItem(spacerItem5)

        # Build Sanity Check UI

        self.vL_sanity = QtWidgets.QVBoxLayout()

        self.check_widgets = []

        for check in functions.CHECK_LIST:
            check_widget = SanityCheckWidget(check, functions.CHECK_LIST[check])

            self.check_widgets.append(check_widget)

            self.vL_sanity.addWidget(check_widget)

        self.verticalLayout.addLayout(self.vL_sanity)

        spacerItem6 = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        self.verticalLayout.addItem(spacerItem6)

        self.horizontalLineBot = QtWidgets.QFrame(self.centralwidget)
        self.horizontalLineBot.setFrameShadow(QtWidgets.QFrame.Plain)
        self.horizontalLineBot.setFrameShape(QtWidgets.QFrame.HLine)
        self.horizontalLineBot.setObjectName("horizontalLineBot")
        self.verticalLayout.addWidget(self.horizontalLineBot)

        spacerItem7 = QtWidgets.QSpacerItem(
            10, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        self.verticalLayout.addItem(spacerItem7)

        self.lbl_output = QtWidgets.QLabel()
        self.lbl_output.setAlignment(QtCore.Qt.AlignHCenter)
        self.verticalLayout.addWidget(self.lbl_output)

        spacerItem8 = QtWidgets.QSpacerItem(
            10, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        self.verticalLayout.addItem(spacerItem8)

        self.btn_export = QtWidgets.QPushButton()
        self.verticalLayout.addWidget(self.btn_export)

        spacerItem9 = QtWidgets.QSpacerItem(
            10, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        self.verticalLayout.addItem(spacerItem9)


        clean_export_generatorWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(clean_export_generatorWindow)

    def build_help(self):
        # Help Button
        self.hL_help = QtWidgets.QHBoxLayout()
        self.hL_help.setObjectName("hL_help")
        self.btn_help = QtWidgets.QToolButton()
        # self.btn_help.setIconSize(QtCore.QSize(10, 10))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        font.setPointSize(7)
        self.btn_help.setFont(font)
        self.btn_help.setStyleSheet("color: rgb(77, 187, 237);")
        self.btn_help.setObjectName("btn_help")
        self.hL_help.addWidget(self.btn_help)
        self.hL_help.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.verticalLayout.addLayout(self.hL_help)
        spacerItem_help = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.verticalLayout.addItem(spacerItem_help)

    def build_default_header(self, clean_export_generatorWindow):
        # Setting up the default PXO header
        self.centralwidget = QtWidgets.QWidget(clean_export_generatorWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        # Shot Field Displaying current Workspace
        self.shotField = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.shotField.setFont(font)
        self.shotField.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.shotField.setObjectName("shotField")
        # Getting Contents from environment variables
        self.shotField.setText(
            "sample_shot_text"
        )
        self.gridLayout.addWidget(self.shotField, 2, 2, 1, 1)
        self.projectField = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setBold(True)
        font.setWeight(75)
        self.projectField.setFont(font)
        self.projectField.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.projectField.setObjectName("projectField")
        self.gridLayout.addWidget(self.projectField, 1, 2, 1, 1)

        # Adding the tool name header
        self.toolName = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.toolName.setFont(font)
        self.toolName.setAlignment(
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter # QtCore.Qt.AlignTrailing
        )
        self.toolName.setObjectName("toolName")
        self.gridLayout.addWidget(self.toolName, 0, 0, 4, 1)
        # Adding Spacers and Lines
        spacerItem = QtWidgets.QSpacerItem(
            40, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.verticalLine = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalLine.sizePolicy().hasHeightForWidth())
        self.verticalLine.setSizePolicy(sizePolicy)
        self.verticalLine.setFrameShadow(QtWidgets.QFrame.Plain)
        self.verticalLine.setFrameShape(QtWidgets.QFrame.VLine)
        self.verticalLine.setObjectName("verticalLine")
        self.gridLayout.addWidget(self.verticalLine, 0, 1, 4, 1)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout.addItem(spacerItem1, 4, 2, 1, 1)
        self.horizontalLineTop = QtWidgets.QFrame(self.centralwidget)
        self.horizontalLineTop.setFrameShadow(QtWidgets.QFrame.Plain)
        self.horizontalLineTop.setFrameShape(QtWidgets.QFrame.HLine)
        self.horizontalLineTop.setObjectName("horizontalLineTop")
        self.gridLayout.addWidget(self.horizontalLineTop, 5, 0, 1, 3)
        spacerItem2 = QtWidgets.QSpacerItem(
            40, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.verticalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.gridLayout)

    def retranslateUi(self, clean_export_generatorWindow):
        _translate = QtCore.QCoreApplication.translate
        clean_export_generatorWindow.setWindowTitle(
            _translate(
                "clean_export_generatorWindow", "{} {}".format(tool_name, version)
            )
        )
        self.projectField.setText(
            "projectField_sample_text"
        )

        self.toolName.setText(
            "DW Clean Export"
        )

        self.lbl_main_grp.setText(_translate("clean_export_generatorWindow", "Parent Group"))
        self.le_source_obj.setPlaceholderText(_translate("clean_export_generatorWindow", "add root group here"))

        self.btn_add_sel.setText(_translate("clean_export_generatorWindow", "<<"))
        self.btn_add_sel.clicked.connect(lambda : self.add_selection())

        self.btn_help.setText(_translate("clean_export_generatorWindow", "Documentation"))
        self.btn_help.clicked.connect(lambda : functions.show_help())

        self.lbl_output.setText("Output is here!")

        self.btn_export_path.clicked.connect(lambda : self.getDir())

        self.btn_export.setText("Export Tagged Geo")
        self.btn_export.clicked.connect(lambda: self.export_btn_clicked())

    def getDir(self):
        if not os.path.isdir(self.le_export_path.text()):
            os.makedirs(self.le_export_path.text())

        file = str(QtWidgets.QFileDialog.getExistingDirectory(self.centralwidget, "Select Directory", self.le_export_path.text()))

        self.set_export_path(file)
        return file

    def set_export_path(self, path=""):
        if not path:
            self.le_export_path.setText(functions.build_default_export_path())
        else:
            self.le_export_path.setText(path)

    def update_sanity_state(self, id):
        check_widget = [x for x in self.check_widgets if x.id == id]
        for widget in check_widget:
            widget.set_sanity_state(True)


    def export_btn_clicked(self):

        root_grp = self.le_source_obj.text()

        if not root_grp:
            self.lbl_output.setText("Please Select a root group first!")
            return

        # Save current file
        original_file, val_save_scene = functions.save_current_scene()


        # Save as Temp Workfile
        val_temp_file = functions.save_as_temp_file()
        if val_temp_file:
            self.update_sanity_state(0)
        else:
            self.lbl_output.setText("Couldn't save to temp File. Aborting!")
            return

        # Parent to World
        val_parent_world = functions.parent_to_world(root_grp)
        if val_parent_world:
            self.update_sanity_state(1)
        else:
            self.lbl_output.setText("Couldn't parent root grp to world. Aborting!")
            return

        # get all geo from top grp
        meshes, transforms, val_get_geo = functions.get_geo_from_sel(root_grp)
        if val_get_geo:
            self.update_sanity_state(2)
        else:
            self.lbl_output.setText("No Geo found to Export. Aborting!")
            return

        # Delete History
        val_delete_history = functions.delete_history(meshes)
        if val_delete_history:
            self.update_sanity_state(3)
        else:
            self.lbl_output.setText("Couldn't delete History. Aborting!")
            return

        # Freeze Transformations
        val_freeze_transforms = functions.freeze_transformations(transforms)
        if val_freeze_transforms:
            self.update_sanity_state(4)
        else:
            self.lbl_output.setText("Couldn't freeze Transforms. Aborting!")
            return

        # Apply lambert1
        val_assign_lambert = functions.assign_lambert(transforms)
        if val_assign_lambert:
            self.update_sanity_state(5)
        else:
            self.lbl_output.setText("Couldn't assign initialShadingGroup. Aborting!")
            return

        # Export Selection
        if not self.le_export_path.text():
            self.set_export_path()
        export_dir = self.le_export_path.text()

        export_path = os.path.join(export_dir, root_grp + ".mb")

        self.lbl_output.setText("Sanity Check Successful! Exporting file to : {}".format(export_path))

        pmc.select(root_grp)
        pmc.exportSelected(export_path, force=True)


        # reload original file
        pmc.openFile(original_file, force=True)



    def reset_sanity(self):
        for widget in self.check_widgets:
            widget.set_sanity_state(False)


    def add_selection(self):
        self.reset_sanity()
        text = functions.get_and_validate_sel()
        if text:
            self.le_source_obj.setText(text[-1])
        else:
            self.le_source_obj.setText("")

def run():
    """Launch the app."""

    windowName = "clean_export_generatorWindow"

    functions.kill_existing_app(windowName)


    app = QtWidgets.QApplication.instance()

    for obj in QtWidgets.QApplication.topLevelWidgets():
        if obj.objectName() == "MayaWindow":
            clean_export_generatorWindow = QtWidgets.QMainWindow(obj)
            ui = Ui_clean_export_generatorWindow()
            ui.setupUi(clean_export_generatorWindow)
            clean_export_generatorWindow.show()


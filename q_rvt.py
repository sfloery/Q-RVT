# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QRVT
                                 A QGIS plugin
 Wrapper for the RVT
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2018-11-30
        git sha              : $Format:%H$
        copyright            : (C) 2018 by covigeos e.U.
        email                : s.floery@covigeos.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import importlib
import time
import subprocess
import os
import sys
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QFile, QFileInfo
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QFileDialog, QGroupBox,QLineEdit,QCheckBox,QComboBox,QWidget

from qgis.core import QgsProject

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .q_rvt_dialog import QRVTDialog

def load_raster_layers(self):

    avail_raster_layers = {}

    self.dlg.select_input_files.clear()

    for layer in QgsProject.instance().mapLayers().values():
        
        # If layer is a raster and it is not a multiband type
        if layer.type() == 1 and layer.bandCount() == 1:

            layer_name = layer.name()
            layer_path = layer.dataProvider().dataSourceUri()

            self.dlg.select_input_files.addItem(layer_name)

            avail_raster_layers[layer_name] = layer_path

    self.avail_raster_layers = avail_raster_layers
            
def check_rvt_installation(self):

    cwd = os.path.dirname(os.path.realpath(__file__))

    file_with_rvt_path = os.path.abspath(os.path.join(cwd, "rvt_path.txt"))

    if os.path.exists(file_with_rvt_path):
        
        with open(file_with_rvt_path, "r") as rvt_file:
            self.rvt_exe_dir = os.path.abspath(rvt_file.readline())
            return True

    else:

        #options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        
        rvt_path = os.path.abspath(QFileDialog.getExistingDirectory(None,"Select RVT directory!"))
        
        if rvt_path:

            with open(file_with_rvt_path, "w") as path_file:
                path_file.write(rvt_path)

            self.rvt_exe_dir = rvt_path

def do_stuff(self):

    rvt_dir = self.rvt_exe_dir

    proc_file_path = os.path.join(rvt_dir, "settings", "process_files.txt")
    settings_path = os.path.join(rvt_dir, "settings", "default_settings.txt")

    selected_layers = []

    for proc_layer in self.dlg.select_input_files.checkedItems():
        selected_layers.append(proc_layer)

    with open(proc_file_path, "w") as proc_file:

        for layer_name in selected_layers:
            layer_path = self.avail_raster_layers[layer_name]

            proc_file.write("%s\n" % (layer_path))

    with open(settings_path, "w") as settings_file:

        settings_file.write("overwrite = 1\n\n")
        settings_file.write("exaggeration_factor = %s\n" % (self.dlg.vertical_factor.text()))

        for widget in self.dlg.children():

            if isinstance(widget, QGroupBox):

                if widget.isChecked():
                    settings_file.write("\n%s = 1\n" % (widget.accessibleDescription()))

                    group_box = widget

                    for widget in group_box.children():

                        #horizontal layouts are stored as widgets
                        if isinstance(widget, QWidget):

                            #get all linedit and combo boxes within the layout widget
                            widget_line = widget.findChildren(QLineEdit)
                            widget_combo = widget.findChildren(QComboBox)

                            if widget_line:
                                for line in widget_line:
                                    line_desc = line.accessibleDescription()
                                    line_text = line.text()

                                    settings_file.write("%s = %s\n" % (line_desc, line_text))

                            if widget_combo:
                                for combo in widget_combo:
                                    combo_desc = combo.accessibleDescription()
                                    combo_text = combo.currentText()

                                    settings_file.write("%s = %s\n" % (combo_desc, combo_text))

                        if isinstance(widget, QLineEdit):
                            line_desc = widget.accessibleDescription()
                            line_text = widget.text()

                            settings_file.write("%s = %s\n" % (line_desc, line_text))

                        if isinstance(widget, QCheckBox):
                            
                            check_desc = widget.accessibleDescription()

                            if widget.isChecked():
                                check_text = 1
                            else:
                                check_text = 0

                            settings_file.write("%s = %i\n" % (check_desc, check_text))

                        if isinstance(widget, QComboBox):
                            combo_desc = widget.accessibleDescription()
                            combo_text = widget.currentText()

                            settings_file.write("%s = %s\n" % (combo_desc, combo_text))

                else:
                    settings_file.write("%s = 0\n\n" % (widget.accessibleDescription()))

    rvt_exe_path = os.path.abspath(os.path.join(rvt_dir, "RVT_1.3_Win64.exe"))
    
    run_rvt_py_path = os.path.abspath(os.path.join(self.plugin_dir, "run_rvt_exe.py"))
    print(run_rvt_py_path)

    python_path = os.environ['PYTHONHOME']
    python_exe_path = os.path.join(python_path, "python.exe")

    cmd = [python_exe_path, run_rvt_py_path, rvt_exe_path, rvt_dir]
    print(cmd)

    run_rvt_cmd = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    run_rvt_cmd.wait()
    cmd_out, cmd_err = run_rvt_cmd.communicate()

    if run_rvt_cmd.returncode == 0:
        pass
    else:
        raise ValueError(cmd_err)
    
    start_time_str = cmd_out.strip().decode("utf-8") 

    for layer in selected_layers:
        raster_layer_name = layer
        raster_layer_path = self.avail_raster_layers[layer]
        raster_layer_dir = os.path.abspath(os.path.dirname(raster_layer_path))

        layer_log_name = raster_layer_name + "_process_log_" + start_time_str + ".txt"
        layer_log_path = os.path.join(raster_layer_dir, raster_layer_name + "_process_log_" + start_time_str + ".txt")

        if os.path.exists(layer_log_path):
            log_file = open(os.path.abspath(layer_log_path), "r")
            log_content = log_file.readlines()
            print(log_content)

        else:
            print("Log-File coult not be loaded!")


def activate_all_groups(self):

    self.dlg.group_hillshading.setChecked(True)
    self.dlg.group_hillshading_multiple.setChecked(True)
    self.dlg.group_pca.setChecked(True)
    self.dlg.group_slope.setChecked(True)
    self.dlg.group_local_relief.setChecked(True)
    self.dlg.group_sky_view.setChecked(True)
    self.dlg.group_anisotropic.setChecked(True)
    self.dlg.group_openess_pos.setChecked(True)
    self.dlg.group_openess_neg.setChecked(True)
    self.dlg.group_illumination.setChecked(True)
    self.dlg.group_local_dominance.setChecked(True)

def deactivate_all_groups(self):

    self.dlg.group_hillshading.setChecked(False)
    self.dlg.group_hillshading_multiple.setChecked(False)
    self.dlg.group_pca.setChecked(False)
    self.dlg.group_slope.setChecked(False)
    self.dlg.group_local_relief.setChecked(False)
    self.dlg.group_sky_view.setChecked(False)
    self.dlg.group_anisotropic.setChecked(False)
    self.dlg.group_openess_pos.setChecked(False)
    self.dlg.group_openess_neg.setChecked(False)
    self.dlg.group_illumination.setChecked(False)
    self.dlg.group_local_dominance.setChecked(False)

def check_module(self, module_name):
    module_spec = importlib.util.find_spec(module_name)

    if module_spec is not None:
        print("%s already installed!" % (module_name))

    else:
        print("Installing %s..." % (module_name))

        python_path = os.environ['PYTHONHOME']

        #install the required module using the qgis python environment; as we don't have
        #administrator privileges we user the --user setting to install it the the user home
        cmd_pip_module = python_path + os.sep + "python.exe -m pip install --user %s" % module_name
        cmd = subprocess.Popen(cmd_pip_module, stdout=subprocess.PIPE, shell=True)


class QRVT:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'QRVT_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = QRVTDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Relief Visualization Toolbox')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Relief Visualization Toolbox')
        self.toolbar.setObjectName(u'Relief Visualization Toolbox')

        self.cwd = os.getcwd()

        #if a layer is added / removed update the available raster layers in the
        #selection dialog
        QgsProject.instance().layersAdded.connect(lambda: load_raster_layers(self))
        QgsProject.instance().layersRemoved.connect(lambda: load_raster_layers(self))

        check_module(self, "pywinauto")
        check_module(self, "psutil")

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('QRVT', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToRasterMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/q_rvt/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Relief Visualization Toolbox'),
            callback=self.run,
            parent=self.iface.mainWindow())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginRasterMenu(
                self.tr(u'&Relief Visualization Toolbox'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def run(self):
        """Run method that performs all the real work"""

        #check if a file exists within the directory of the plugin which stores
        #information about where to find the rvt installation
        check_rvt_installation(self)
        
        print("Location of RVT-Installation: %s" % (self.rvt_exe_dir))

        load_raster_layers(self)

        #create events when pressing the button

        #run this function if the start button is pressed
        self.dlg.start_button.clicked.connect(lambda: do_stuff(self))

        #close the application if the exit button is pressed
        self.dlg.close_button.clicked.connect(self.dlg.close)

        self.dlg.select_all_button.clicked.connect(lambda: activate_all_groups(self))
        self.dlg.select_none_button.clicked.connect(lambda: deactivate_all_groups(self))

        # show the dialog
        self.dlg.show()
        

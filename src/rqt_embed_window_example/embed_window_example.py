import os
import roslib
import rospy
import rospkg
import rviz
import subprocess

from qt_gui.plugin import Plugin
from python_qt_binding import loadUi
from python_qt_binding.QtWidgets import QWidget
from rqt_embed_window.embed_window_widget import EmbedWindowWidget


class EmbedWindowExample(Plugin):
    """
    Class encapsulating the GUI
    """

    def __init__(self, context):
        """
        Initialise the class
        """
        super(EmbedWindowExample, self).__init__(context)
        self.setObjectName("EmbedWindowExample")
        
        # Important paths
        package_path = rospkg.RosPack().get_path("rqt_embed_window_example")
        resource_path = os.path.join(package_path, "resource")

        # Create graphical user interface (GUI)
        self._widget = QWidget()
        ui_file = os.path.join(resource_path, "EmbedWindowExample.ui")
        loadUi(ui_file, self._widget, {'EmbedWindowWidget': EmbedWindowWidget})
        self._widget.setObjectName("EmbedWindowExampleUi")
        
        # Start the two applications
        self._widget.rviz_widget.add_external_window_widget("rviz -s None")
        self._widget.plotjuggler_widget.add_external_window_widget("plotjuggler --nosplash")
        
        if context.serial_number() > 1:
            self._widget.setWindowTitle(self._widget.windowTitle() + (" (%d)" % context.serial_number()))
        context.add_widget(self._widget)
        
        return

    def shutdown_plugin(self):
        # Free resources
        self._widget.rviz_widget.kill_process()
        self._widget.plotjuggler_widget.kill_process()
        return

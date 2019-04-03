#!/usr/bin/env python
import os
import time

import rospy

from biomech_comms.msg import ExoCommand
from biomech_comms.comm_codes import CommandCode

class ExoGuiSender():
    def __init__(self, widget, pub_topic, data):
        """
        :param context: plugin context hook to enable adding widgets as a ROS_GUI pane, ''PluginContext''
        """
        publisher = rospy.Publisher(pub_topic, ExoCommand, queue_size=10)

        self._widget = widget
        self._data = data
        self._command_pub = publisher;
        self._command = ExoCommand()

        self._widget.setObjectName('BiomechGui')
        self._widget.startTrialButton.clicked.connect(self.start_trial)
        self._widget.endTrialButton.clicked.connect(self.end_trial)
        self._widget.calibrateTorqueButton.clicked.connect(self.calibrate_torque)
        self._widget.bluetoothCheckButton.clicked.connect(self.check_bluetooth)


    def send_command(self, command, *data):
        self._command.command_code = command
        self._command.data = data
        self._command_pub.publish(self._command)

    def report_info(self, info):
        self._widget.exoReportLabel.setText(info)

    def start_trial(self):
        self.report_info("Starting Trial")
        self.send_command(CommandCode.START_TRIAL)

    def end_trial(self):
        self.report_info("Ending Trial")
        self.send_command(CommandCode.END_TRIAL)

    def calibrate_torque(self):
        self.report_info("Calibrating Torque")
        self.send_command(CommandCode.CALIBRATE_TORQUE)

    def check_bluetooth(self):
        self._data["check_bluetooth_fail"] = True
        self.report_info("Checking bluetooth")
        self.send_command(CommandCode.CHECK_BLUETOOTH)
        rospy.Timer(rospy.Duration(1), self.check_bluetooth_fail, oneshot=True)

    def check_bluetooth_fail(self, event):
        if self._data["check_bluetooth_fail"]:
            self.report_info("Bluetooth failed")

    def get_left_pid(self):
        self.send_command(CommandCode.GET_LEFT_ANKLE_PID_PARAMS)

    def set_left_pid(self):
        self.send_command(CommandCode.SET_LEFT_RIGHT_ANKLE_PID_PARAMS, p,i,d)

    def set_torque(self, widget):
        def _set_torque():
            try:
                pfx = float(widget.pfxLine.text())
                dfx = float(widget.dfxLine.text())
                self.send_command(CommandCode.SET_LEFT_ANKLE_SETPOINT, pfx,dfx)
            except ValueError:
                self.report_info("Bad Torque Setpoint")
        return _set_torque

    def get_torque(self, widget):
        def _get_torque():
            self.send_command(CommandCode.GET_LEFT_ANKLE_SETPOINT)
        return _get_torque
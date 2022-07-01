# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\jonathan.t.kopf\Desktop\Dev_Env_Shared\UEWS_rebuild\uwes_rebuild\UI Files\tracking_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UEWS_Tracking_GUI(object):
    def setupUi(self, UEWS_Tracking_GUI):
        UEWS_Tracking_GUI.setObjectName("UEWS_Tracking_GUI")
        UEWS_Tracking_GUI.resize(1210, 713)
        UEWS_Tracking_GUI.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        UEWS_Tracking_GUI.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(UEWS_Tracking_GUI)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.StateReceiver = StateReceiver(self.centralwidget)
        self.StateReceiver.setMinimumSize(QtCore.QSize(0, 0))
        self.StateReceiver.setMaximumSize(QtCore.QSize(0, 0))
        self.StateReceiver.setBaseSize(QtCore.QSize(0, 0))
        self.StateReceiver.setObjectName("StateReceiver")
        self.verticalLayout.addWidget(self.StateReceiver)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setIconSize(QtCore.QSize(16, 16))
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout.setSpacing(16)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.gridLayout.setContentsMargins(-1, -1, -1, 0)
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.valid_track_points = QtWidgets.QLabel(self.tab)
        self.valid_track_points.setObjectName("valid_track_points")
        self.gridLayout.addWidget(self.valid_track_points, 1, 10, 1, 1, QtCore.Qt.AlignRight)
        self.sub_in_bounds = QtWidgets.QLabel(self.tab)
        self.sub_in_bounds.setObjectName("sub_in_bounds")
        self.gridLayout.addWidget(self.sub_in_bounds, 2, 7, 1, 1)
        self.ProjectedY = QtWidgets.QLabel(self.tab)
        self.ProjectedY.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ProjectedY.setObjectName("ProjectedY")
        self.gridLayout.addWidget(self.ProjectedY, 2, 0, 1, 1)
        self.alarm_on_indicator = QLed(self.tab)
        self.alarm_on_indicator.setObjectName("alarm_on_indicator")
        self.gridLayout.addWidget(self.alarm_on_indicator, 3, 8, 1, 1)
        self.proj_x_val = QtWidgets.QLCDNumber(self.tab)
        self.proj_x_val.setAutoFillBackground(False)
        self.proj_x_val.setFrameShape(QtWidgets.QFrame.Panel)
        self.proj_x_val.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.proj_x_val.setLineWidth(1)
        self.proj_x_val.setMidLineWidth(1)
        self.proj_x_val.setSmallDecimalPoint(False)
        self.proj_x_val.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.proj_x_val.setObjectName("proj_x_val")
        self.gridLayout.addWidget(self.proj_x_val, 1, 1, 1, 1)
        self.valid_track_pts_val = QtWidgets.QLCDNumber(self.tab)
        self.valid_track_pts_val.setAutoFillBackground(False)
        self.valid_track_pts_val.setFrameShape(QtWidgets.QFrame.Panel)
        self.valid_track_pts_val.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.valid_track_pts_val.setLineWidth(1)
        self.valid_track_pts_val.setMidLineWidth(1)
        self.valid_track_pts_val.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.valid_track_pts_val.setObjectName("valid_track_pts_val")
        self.gridLayout.addWidget(self.valid_track_pts_val, 1, 11, 1, 1)
        self.sub_pos_good = QtWidgets.QLabel(self.tab)
        self.sub_pos_good.setObjectName("sub_pos_good")
        self.gridLayout.addWidget(self.sub_pos_good, 4, 7, 1, 1)
        self.depth_violations_val = QtWidgets.QLCDNumber(self.tab)
        self.depth_violations_val.setAutoFillBackground(False)
        self.depth_violations_val.setFrameShape(QtWidgets.QFrame.Panel)
        self.depth_violations_val.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.depth_violations_val.setLineWidth(1)
        self.depth_violations_val.setMidLineWidth(1)
        self.depth_violations_val.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.depth_violations_val.setObjectName("depth_violations_val")
        self.gridLayout.addWidget(self.depth_violations_val, 4, 11, 1, 1)
        self.alert_count_val = QtWidgets.QLCDNumber(self.tab)
        self.alert_count_val.setAutoFillBackground(False)
        self.alert_count_val.setFrameShape(QtWidgets.QFrame.Panel)
        self.alert_count_val.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.alert_count_val.setLineWidth(1)
        self.alert_count_val.setMidLineWidth(1)
        self.alert_count_val.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.alert_count_val.setObjectName("alert_count_val")
        self.gridLayout.addWidget(self.alert_count_val, 3, 11, 1, 1)
        self.z_val = QtWidgets.QLCDNumber(self.tab)
        self.z_val.setAutoFillBackground(False)
        self.z_val.setFrameShape(QtWidgets.QFrame.Panel)
        self.z_val.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.z_val.setLineWidth(1)
        self.z_val.setMidLineWidth(1)
        self.z_val.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.z_val.setObjectName("z_val")
        self.gridLayout.addWidget(self.z_val, 3, 3, 1, 1)
        self.no_sub_data_val = QtWidgets.QLCDNumber(self.tab)
        self.no_sub_data_val.setAutoFillBackground(False)
        self.no_sub_data_val.setFrameShape(QtWidgets.QFrame.Panel)
        self.no_sub_data_val.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.no_sub_data_val.setLineWidth(1)
        self.no_sub_data_val.setMidLineWidth(1)
        self.no_sub_data_val.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.no_sub_data_val.setObjectName("no_sub_data_val")
        self.gridLayout.addWidget(self.no_sub_data_val, 2, 11, 1, 1)
        self.no_sub_data = QtWidgets.QLabel(self.tab)
        self.no_sub_data.setObjectName("no_sub_data")
        self.gridLayout.addWidget(self.no_sub_data, 2, 10, 1, 1, QtCore.Qt.AlignRight)
        self.proj_y_val = QtWidgets.QLCDNumber(self.tab)
        self.proj_y_val.setAutoFillBackground(False)
        self.proj_y_val.setFrameShape(QtWidgets.QFrame.Panel)
        self.proj_y_val.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.proj_y_val.setLineWidth(1)
        self.proj_y_val.setMidLineWidth(1)
        self.proj_y_val.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.proj_y_val.setObjectName("proj_y_val")
        self.gridLayout.addWidget(self.proj_y_val, 2, 1, 1, 1)
        self.x_ok = QtWidgets.QLabel(self.tab)
        self.x_ok.setObjectName("x_ok")
        self.gridLayout.addWidget(self.x_ok, 1, 5, 1, 1)
        self.speed_ok_indicator = QLed(self.tab)
        self.speed_ok_indicator.setObjectName("speed_ok_indicator")
        self.gridLayout.addWidget(self.speed_ok_indicator, 4, 4, 1, 1)
        self.send_warn_tones_indicator = QLed(self.tab)
        self.send_warn_tones_indicator.setObjectName("send_warn_tones_indicator")
        self.gridLayout.addWidget(self.send_warn_tones_indicator, 1, 8, 1, 1)
        self.tp_course = QtWidgets.QLabel(self.tab)
        self.tp_course.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tp_course.setObjectName("tp_course")
        self.gridLayout.addWidget(self.tp_course, 4, 0, 1, 1)
        self.speed_val = QtWidgets.QLCDNumber(self.tab)
        self.speed_val.setAutoFillBackground(False)
        self.speed_val.setFrameShape(QtWidgets.QFrame.Panel)
        self.speed_val.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.speed_val.setLineWidth(1)
        self.speed_val.setMidLineWidth(1)
        self.speed_val.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.speed_val.setObjectName("speed_val")
        self.gridLayout.addWidget(self.speed_val, 4, 3, 1, 1)
        self.speed = QtWidgets.QLabel(self.tab)
        self.speed.setObjectName("speed")
        self.gridLayout.addWidget(self.speed, 4, 2, 1, 1, QtCore.Qt.AlignRight)
        self.alarm_enable_indicator = QLed(self.tab)
        self.alarm_enable_indicator.setObjectName("alarm_enable_indicator")
        self.gridLayout.addWidget(self.alarm_enable_indicator, 2, 8, 1, 1)
        self.z_ok = QtWidgets.QLabel(self.tab)
        self.z_ok.setObjectName("z_ok")
        self.gridLayout.addWidget(self.z_ok, 3, 5, 1, 1)
        self.proj_pos_good = QtWidgets.QLabel(self.tab)
        self.proj_pos_good.setWordWrap(True)
        self.proj_pos_good.setObjectName("proj_pos_good")
        self.gridLayout.addWidget(self.proj_pos_good, 3, 7, 1, 1)
        self.y = QtWidgets.QLabel(self.tab)
        self.y.setObjectName("y")
        self.gridLayout.addWidget(self.y, 2, 2, 1, 1, QtCore.Qt.AlignRight)
        self.valid_track_pts = QtWidgets.QLabel(self.tab)
        self.valid_track_pts.setWordWrap(True)
        self.valid_track_pts.setObjectName("valid_track_pts")
        self.gridLayout.addWidget(self.valid_track_pts, 1, 7, 1, 1)
        self.x_val = QtWidgets.QLCDNumber(self.tab)
        self.x_val.setAutoFillBackground(False)
        self.x_val.setFrameShape(QtWidgets.QFrame.Panel)
        self.x_val.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.x_val.setLineWidth(1)
        self.x_val.setMidLineWidth(1)
        self.x_val.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.x_val.setObjectName("x_val")
        self.gridLayout.addWidget(self.x_val, 1, 3, 1, 1)
        self.proj_pos_good_indicator = QLed(self.tab)
        self.proj_pos_good_indicator.setObjectName("proj_pos_good_indicator")
        self.gridLayout.addWidget(self.proj_pos_good_indicator, 3, 6, 1, 1)
        self.course_val = QtWidgets.QLCDNumber(self.tab)
        self.course_val.setAutoFillBackground(False)
        self.course_val.setFrameShape(QtWidgets.QFrame.Panel)
        self.course_val.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.course_val.setLineWidth(1)
        self.course_val.setMidLineWidth(1)
        self.course_val.setSmallDecimalPoint(False)
        self.course_val.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.course_val.setObjectName("course_val")
        self.gridLayout.addWidget(self.course_val, 3, 1, 1, 1)
        self.z = QtWidgets.QLabel(self.tab)
        self.z.setObjectName("z")
        self.gridLayout.addWidget(self.z, 3, 2, 1, 1, QtCore.Qt.AlignRight)
        self.Course = QtWidgets.QLabel(self.tab)
        self.Course.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Course.setObjectName("Course")
        self.gridLayout.addWidget(self.Course, 3, 0, 1, 1)
        self.x = QtWidgets.QLabel(self.tab)
        self.x.setObjectName("x")
        self.gridLayout.addWidget(self.x, 1, 2, 1, 1, QtCore.Qt.AlignRight)
        self.valid_trk_pts_indicator = QLed(self.tab)
        self.valid_trk_pts_indicator.setObjectName("valid_trk_pts_indicator")
        self.gridLayout.addWidget(self.valid_trk_pts_indicator, 1, 6, 1, 1)
        self.x_ok_indicator = QLed(self.tab)
        self.x_ok_indicator.setObjectName("x_ok_indicator")
        self.gridLayout.addWidget(self.x_ok_indicator, 1, 4, 1, 1)
        self.send_warn_tones = QtWidgets.QLabel(self.tab)
        self.send_warn_tones.setWordWrap(True)
        self.send_warn_tones.setObjectName("send_warn_tones")
        self.gridLayout.addWidget(self.send_warn_tones, 1, 9, 1, 1)
        self.y_ok_indicator = QLed(self.tab)
        self.y_ok_indicator.setObjectName("y_ok_indicator")
        self.gridLayout.addWidget(self.y_ok_indicator, 2, 4, 1, 1)
        self.y_ok = QtWidgets.QLabel(self.tab)
        self.y_ok.setObjectName("y_ok")
        self.gridLayout.addWidget(self.y_ok, 2, 5, 1, 1)
        self.sub_in_indicator = QLed(self.tab)
        self.sub_in_indicator.setObjectName("sub_in_indicator")
        self.gridLayout.addWidget(self.sub_in_indicator, 2, 6, 1, 1)
        self.ProjectedX = QtWidgets.QLabel(self.tab)
        self.ProjectedX.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.ProjectedX.setFrameShadow(QtWidgets.QFrame.Plain)
        self.ProjectedX.setScaledContents(False)
        self.ProjectedX.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ProjectedX.setObjectName("ProjectedX")
        self.gridLayout.addWidget(self.ProjectedX, 1, 0, 1, 1)
        self.z_ok_indicator = QLed(self.tab)
        self.z_ok_indicator.setObjectName("z_ok_indicator")
        self.gridLayout.addWidget(self.z_ok_indicator, 3, 4, 1, 1)
        self.alarm_enable = QtWidgets.QLabel(self.tab)
        self.alarm_enable.setObjectName("alarm_enable")
        self.gridLayout.addWidget(self.alarm_enable, 2, 9, 1, 1)
        self.tp_course_val = QtWidgets.QLCDNumber(self.tab)
        self.tp_course_val.setAutoFillBackground(False)
        self.tp_course_val.setFrameShape(QtWidgets.QFrame.Panel)
        self.tp_course_val.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tp_course_val.setLineWidth(1)
        self.tp_course_val.setMidLineWidth(1)
        self.tp_course_val.setSmallDecimalPoint(False)
        self.tp_course_val.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.tp_course_val.setObjectName("tp_course_val")
        self.gridLayout.addWidget(self.tp_course_val, 4, 1, 1, 1)
        self.sub_pos_good_indicator = QLed(self.tab)
        self.sub_pos_good_indicator.setObjectName("sub_pos_good_indicator")
        self.gridLayout.addWidget(self.sub_pos_good_indicator, 4, 6, 1, 1)
        self.alert_count = QtWidgets.QLabel(self.tab)
        self.alert_count.setObjectName("alert_count")
        self.gridLayout.addWidget(self.alert_count, 3, 10, 1, 1, QtCore.Qt.AlignRight)
        self.depth_violations = QtWidgets.QLabel(self.tab)
        self.depth_violations.setObjectName("depth_violations")
        self.gridLayout.addWidget(self.depth_violations, 4, 10, 1, 1, QtCore.Qt.AlignRight)
        self.alarm_on = QtWidgets.QLabel(self.tab)
        self.alarm_on.setObjectName("alarm_on")
        self.gridLayout.addWidget(self.alarm_on, 3, 9, 1, 1)
        self.y_val = QtWidgets.QLCDNumber(self.tab)
        self.y_val.setAutoFillBackground(False)
        self.y_val.setFrameShape(QtWidgets.QFrame.Panel)
        self.y_val.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.y_val.setLineWidth(1)
        self.y_val.setMidLineWidth(1)
        self.y_val.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.y_val.setObjectName("y_val")
        self.gridLayout.addWidget(self.y_val, 2, 3, 1, 1)
        self.speed_ok = QtWidgets.QLabel(self.tab)
        self.speed_ok.setObjectName("speed_ok")
        self.gridLayout.addWidget(self.speed_ok, 4, 5, 1, 1)
        self.seconds_to_alarm = QtWidgets.QLabel(self.tab)
        self.seconds_to_alarm.setObjectName("seconds_to_alarm")
        self.gridLayout.addWidget(self.seconds_to_alarm, 4, 8, 1, 1)
        self.seconds_to_alarm_val = QtWidgets.QLCDNumber(self.tab)
        self.seconds_to_alarm_val.setSmallDecimalPoint(False)
        self.seconds_to_alarm_val.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.seconds_to_alarm_val.setObjectName("seconds_to_alarm_val")
        self.gridLayout.addWidget(self.seconds_to_alarm_val, 4, 9, 1, 1)
        self.gridLayout.setColumnStretch(0, 3)
        self.gridLayout.setColumnStretch(1, 3)
        self.gridLayout.setColumnStretch(2, 3)
        self.gridLayout.setColumnStretch(3, 3)
        self.gridLayout.setColumnStretch(4, 5)
        self.gridLayout.setColumnStretch(5, 3)
        self.gridLayout.setColumnStretch(6, 5)
        self.gridLayout.setColumnStretch(7, 3)
        self.gridLayout.setColumnStretch(8, 5)
        self.gridLayout.setColumnStretch(9, 3)
        self.gridLayout.setColumnStretch(10, 3)
        self.gridLayout.setColumnStretch(11, 3)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.AutoAlarmToggle = QtWidgets.QPushButton(self.tab)
        self.AutoAlarmToggle.setAutoDefault(True)
        self.AutoAlarmToggle.setObjectName("AutoAlarmToggle")
        self.verticalLayout_2.addWidget(self.AutoAlarmToggle)
        self.AlarmInhibitor = QtWidgets.QPushButton(self.tab)
        self.AlarmInhibitor.setObjectName("AlarmInhibitor")
        self.verticalLayout_2.addWidget(self.AlarmInhibitor)
        self.ManualOverride = QtWidgets.QPushButton(self.tab)
        self.ManualOverride.setCheckable(False)
        self.ManualOverride.setAutoDefault(False)
        self.ManualOverride.setDefault(False)
        self.ManualOverride.setFlat(False)
        self.ManualOverride.setObjectName("ManualOverride")
        self.verticalLayout_2.addWidget(self.ManualOverride)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout.setStretch(0, 8)
        self.horizontalLayout.setStretch(1, 2)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tab_2)
        self.horizontalLayout_2.setSpacing(20)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gridFrame = QtWidgets.QFrame(self.tab_2)
        self.gridFrame.setFrameShape(QtWidgets.QFrame.Panel)
        self.gridFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.gridFrame.setLineWidth(1)
        self.gridFrame.setMidLineWidth(0)
        self.gridFrame.setObjectName("gridFrame")
        self.Timing_info = QtWidgets.QGridLayout(self.gridFrame)
        self.Timing_info.setObjectName("Timing_info")
        self.time_since_last_val = QtWidgets.QLabel(self.gridFrame)
        self.time_since_last_val.setFrameShape(QtWidgets.QFrame.Panel)
        self.time_since_last_val.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.time_since_last_val.setObjectName("time_since_last_val")
        self.Timing_info.addWidget(self.time_since_last_val, 0, 1, 1, 1)
        self.float_time = QtWidgets.QLabel(self.gridFrame)
        self.float_time.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.float_time.setObjectName("float_time")
        self.Timing_info.addWidget(self.float_time, 1, 0, 1, 1)
        self.float_time_val = QtWidgets.QLabel(self.gridFrame)
        self.float_time_val.setFrameShape(QtWidgets.QFrame.Panel)
        self.float_time_val.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.float_time_val.setObjectName("float_time_val")
        self.Timing_info.addWidget(self.float_time_val, 1, 1, 1, 1)
        self.time_since_last = QtWidgets.QLabel(self.gridFrame)
        self.time_since_last.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.time_since_last.setObjectName("time_since_last")
        self.Timing_info.addWidget(self.time_since_last, 0, 0, 1, 1)
        self.time_dilation_factor = QtWidgets.QLabel(self.gridFrame)
        self.time_dilation_factor.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.time_dilation_factor.setObjectName("time_dilation_factor")
        self.Timing_info.addWidget(self.time_dilation_factor, 2, 0, 1, 1)
        self.time_dilation_factor_val = QtWidgets.QLabel(self.gridFrame)
        self.time_dilation_factor_val.setFrameShape(QtWidgets.QFrame.Panel)
        self.time_dilation_factor_val.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.time_dilation_factor_val.setObjectName("time_dilation_factor_val")
        self.Timing_info.addWidget(self.time_dilation_factor_val, 2, 1, 1, 1)
        self.horizontalLayout_2.addWidget(self.gridFrame)
        self.frame = QtWidgets.QFrame(self.tab_2)
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.verticalLayout_5.addWidget(self.label)
        self.RawRSDF = QtWidgets.QTextBrowser(self.frame)
        self.RawRSDF.setFrameShape(QtWidgets.QFrame.Panel)
        self.RawRSDF.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.RawRSDF.setOpenLinks(False)
        self.RawRSDF.setObjectName("RawRSDF")
        self.verticalLayout_5.addWidget(self.RawRSDF)
        self.verticalLayout_5.setStretch(0, 1)
        self.verticalLayout_5.setStretch(1, 9)
        self.horizontalLayout_2.addWidget(self.frame)
        self.gridFrame_3 = QtWidgets.QFrame(self.tab_2)
        self.gridFrame_3.setFrameShape(QtWidgets.QFrame.Panel)
        self.gridFrame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.gridFrame_3.setObjectName("gridFrame_3")
        self.Network_Info = QtWidgets.QGridLayout(self.gridFrame_3)
        self.Network_Info.setObjectName("Network_Info")
        self.Port = QtWidgets.QLabel(self.gridFrame_3)
        self.Port.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Port.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Port.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Port.setObjectName("Port")
        self.Network_Info.addWidget(self.Port, 0, 0, 1, 1)
        self.IP_address = QtWidgets.QLabel(self.gridFrame_3)
        self.IP_address.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.IP_address.setFrameShadow(QtWidgets.QFrame.Raised)
        self.IP_address.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.IP_address.setObjectName("IP_address")
        self.Network_Info.addWidget(self.IP_address, 1, 0, 1, 1)
        self.ip_address_input = QtWidgets.QLineEdit(self.gridFrame_3)
        self.ip_address_input.setObjectName("ip_address_input")
        self.Network_Info.addWidget(self.ip_address_input, 1, 1, 1, 1)
        self.port_input = QtWidgets.QLineEdit(self.gridFrame_3)
        self.port_input.setObjectName("port_input")
        self.Network_Info.addWidget(self.port_input, 0, 1, 1, 1)
        self.Network_Info.setColumnStretch(0, 2)
        self.Network_Info.setColumnStretch(1, 1)
        self.horizontalLayout_2.addWidget(self.gridFrame_3)
        self.horizontalLayout_2.setStretch(0, 4)
        self.horizontalLayout_2.setStretch(1, 3)
        self.horizontalLayout_2.setStretch(2, 2)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.TrackingCanvas = Canvas(self.centralwidget)
        self.TrackingCanvas.setObjectName("TrackingCanvas")
        self.verticalLayout.addWidget(self.TrackingCanvas)
        self.verticalLayout.setStretch(1, 4)
        self.verticalLayout.setStretch(2, 7)
        UEWS_Tracking_GUI.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(UEWS_Tracking_GUI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1210, 21))
        self.menubar.setObjectName("menubar")
        UEWS_Tracking_GUI.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(UEWS_Tracking_GUI)
        self.statusbar.setObjectName("statusbar")
        UEWS_Tracking_GUI.setStatusBar(self.statusbar)

        self.retranslateUi(UEWS_Tracking_GUI)
        self.tabWidget.setCurrentIndex(0)
        self.StateReceiver.receivedState.connect(self.TrackingCanvas.new_state)
        self.StateReceiver.set_x['int'].connect(self.x_val.display)
        self.StateReceiver.set_y['int'].connect(self.y_val.display)
        self.StateReceiver.set_z['int'].connect(self.z_val.display)
        self.StateReceiver.set_proj_x['int'].connect(self.proj_x_val.display)
        self.StateReceiver.set_proj_y['int'].connect(self.proj_y_val.display)
        self.StateReceiver.set_course['int'].connect(self.course_val.display)
        self.StateReceiver.set_tp_course['int'].connect(self.tp_course_val.display)
        self.StateReceiver.set_sub_in_bounds['bool'].connect(self.sub_in_indicator.setValue)
        self.StateReceiver.set_speed['int'].connect(self.speed_val.display)
        self.StateReceiver.set_on_colour['int'].connect(self.speed_ok_indicator.setOnColour)
        self.StateReceiver.set_off_colour['int'].connect(self.speed_ok_indicator.setOffColour)
        self.StateReceiver.set_x_ok['bool'].connect(self.x_ok_indicator.setValue)
        self.StateReceiver.set_y_ok['bool'].connect(self.y_ok_indicator.setValue)
        self.StateReceiver.set_z_ok['bool'].connect(self.z_ok_indicator.setValue)
        self.StateReceiver.set_valid_consec_track['bool'].connect(self.valid_trk_pts_indicator.setValue)
        self.StateReceiver.set_proj_pos_good['bool'].connect(self.proj_pos_good_indicator.setValue)
        self.StateReceiver.set_sub_pos_good['bool'].connect(self.sub_pos_good_indicator.setValue)
        self.StateReceiver.set_send_warn_tones['bool'].connect(self.send_warn_tones_indicator.setValue)
        self.StateReceiver.set_alarm_enable['bool'].connect(self.alarm_enable_indicator.setValue)
        self.StateReceiver.set_alarm_on['bool'].connect(self.alarm_on_indicator.setValue)
        self.StateReceiver.set_valid_track_pts['int'].connect(self.valid_track_pts_val.display)
        self.StateReceiver.set_no_sub_data['int'].connect(self.no_sub_data_val.display)
        self.StateReceiver.set_alert_count['int'].connect(self.alert_count_val.display)
        self.StateReceiver.set_depth_violations['int'].connect(self.depth_violations_val.display)
        self.AutoAlarmToggle.toggled['bool'].connect(self.StateReceiver.auto_alarm)
        self.ManualOverride.clicked['bool'].connect(self.StateReceiver.manual_pressed)
        self.AlarmInhibitor.clicked['bool'].connect(self.StateReceiver.new_inhibit)
        QtCore.QMetaObject.connectSlotsByName(UEWS_Tracking_GUI)

    def retranslateUi(self, UEWS_Tracking_GUI):
        _translate = QtCore.QCoreApplication.translate
        UEWS_Tracking_GUI.setWindowTitle(_translate("UEWS_Tracking_GUI", "UEWS Tracking GUI"))
        self.valid_track_points.setText(_translate("UEWS_Tracking_GUI", "Valid Track Pts"))
        self.sub_in_bounds.setText(_translate("UEWS_Tracking_GUI", "Sub in Bounds"))
        self.ProjectedY.setText(_translate("UEWS_Tracking_GUI", "proj_y"))
        self.sub_pos_good.setText(_translate("UEWS_Tracking_GUI", "Sub Pos Good"))
        self.no_sub_data.setText(_translate("UEWS_Tracking_GUI", "No Sub Data"))
        self.x_ok.setText(_translate("UEWS_Tracking_GUI", "x ok"))
        self.tp_course.setText(_translate("UEWS_Tracking_GUI", "tp_course"))
        self.speed.setText(_translate("UEWS_Tracking_GUI", "speed"))
        self.z_ok.setText(_translate("UEWS_Tracking_GUI", "z ok"))
        self.proj_pos_good.setText(_translate("UEWS_Tracking_GUI", "Projected Pos Good"))
        self.y.setText(_translate("UEWS_Tracking_GUI", "y"))
        self.valid_track_pts.setText(_translate("UEWS_Tracking_GUI", "5 Valid Consec trk pts"))
        self.z.setText(_translate("UEWS_Tracking_GUI", "z"))
        self.Course.setText(_translate("UEWS_Tracking_GUI", "course"))
        self.x.setText(_translate("UEWS_Tracking_GUI", "x"))
        self.send_warn_tones.setText(_translate("UEWS_Tracking_GUI", "Send Warning Tones"))
        self.y_ok.setText(_translate("UEWS_Tracking_GUI", "y ok"))
        self.ProjectedX.setText(_translate("UEWS_Tracking_GUI", "proj_x"))
        self.alarm_enable.setText(_translate("UEWS_Tracking_GUI", "Alarm Enable"))
        self.alert_count.setText(_translate("UEWS_Tracking_GUI", "Alert Count"))
        self.depth_violations.setText(_translate("UEWS_Tracking_GUI", "Depth Violations"))
        self.alarm_on.setText(_translate("UEWS_Tracking_GUI", "Alarm On"))
        self.speed_ok.setText(_translate("UEWS_Tracking_GUI", "speed ok"))
        self.seconds_to_alarm.setText(_translate("UEWS_Tracking_GUI", "Seconds to Alarm"))
        self.AutoAlarmToggle.setText(_translate("UEWS_Tracking_GUI", "Auto Alarm"))
        self.AlarmInhibitor.setText(_translate("UEWS_Tracking_GUI", "Alarm Inhibitor"))
        self.ManualOverride.setText(_translate("UEWS_Tracking_GUI", "Manual Alarm"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("UEWS_Tracking_GUI", "Tab 1"))
        self.time_since_last_val.setText(_translate("UEWS_Tracking_GUI", "0.0"))
        self.float_time.setText(_translate("UEWS_Tracking_GUI", "Float Time"))
        self.float_time_val.setText(_translate("UEWS_Tracking_GUI", "0.0"))
        self.time_since_last.setText(_translate("UEWS_Tracking_GUI", "Time Since Last Message"))
        self.time_dilation_factor.setText(_translate("UEWS_Tracking_GUI", "Time Dilation Factor"))
        self.time_dilation_factor_val.setText(_translate("UEWS_Tracking_GUI", "0.0"))
        self.label.setText(_translate("UEWS_Tracking_GUI", "Raw RSDF string"))
        self.Port.setText(_translate("UEWS_Tracking_GUI", "Port"))
        self.IP_address.setText(_translate("UEWS_Tracking_GUI", "IP_address"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("UEWS_Tracking_GUI", "Tab 2"))
from QLed import QLed
from state_receiver import StateReceiver
from tracking_grid import Canvas

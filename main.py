import os
import sys
import mainwindow
import numpy as np
import cv2
from PyQt5 import QtWidgets, QtCore
from PyQt5.Qt import QTimer
from PyQt5.QtGui import QPixmap, QImage, qRgb, QPainter, QPen
from PyQt5.QtWidgets import QFileDialog, QDialog
import shutil

gray_color_table = [qRgb(i, i, i) for i in range(256)]

def compare(frame0, frame1):
    eq = np.equal(frame0, frame1).flatten().nonzero()
    share = len(eq[0]) / (frame1.shape[0]*frame1.shape[1]*frame1.shape[2])
    print(share)
    pass



def convert_ndarr_to_qimg(arr):
    if arr is None:
        return QImage()
    qim = None
    if arr.dtype is not np.uint8:
        arr = arr.astype(np.uint8)
    if arr.dtype == np.uint8:
        if len(arr.shape) == 2:
            qim = QImage(arr.data, arr.shape[1], arr.shape[0], arr.strides[0], QImage.Format_Indexed8)
            qim.setColorTable(gray_color_table)
        elif len(arr.shape) == 3:
            if arr.shape[2] == 3:
                qim = QImage(arr.data, arr.shape[1], arr.shape[0], arr.strides[0], QImage.Format_RGB888)
    return qim.copy()

class guiApp(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.init_data()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Video marker v.1')
        self.lineEdit_video_file_path.editingFinished.connect(self.lineedit_video_file_path_editing_finished)
        self.lineEdit_xml_dir_path.editingFinished.connect(self.lineedit_xml_dir_path_editing_finished)
        self.lineEdit_Proc_time.editingFinished.connect(self.lineEdit_Proc_time_editing_finished)
        self.lineEdit_freq_xmls.editingFinished.connect(self.lineEdit_freq_xmls_editing_finished)
        self.pushButton_play.clicked.connect(self.pushbutton_play_clicked)
        self.checkBox_create_xml.toggled.connect(self.checkBox_create_xml_toggled)
        self.pushButton_select_video_file.clicked.connect(self.pushbutton_select_video_file_clicked)
        self.pushButton_select_dir_xml.clicked.connect(self.pushbutton_select_dir_xml_clicked)
        self.pushButton_back.clicked.connect(self.pushbutton_back_clicked)
        self.pushButton_forward.clicked.connect(self.pushbutton_forward_clicked)
        self.lineEdit_name_object.editingFinished.connect(self.lineEdit_name_object_editing_finished)
        self.lineEdit_video_file_path.setText('3.mp4')
        self.lineEdit_xml_dir_path.setText('/media/aigul/Tom/Aigul/Narrow_field_tensorflow/ssd_tensorflow_dataset_maker/annotations/xmls/')
        self.lineEdit_freq_xmls.setText('2')
        self.lineEdit_Proc_time.setText('200')
        self.lineEdit_name_object.setText('phantom')
        self.lineedit_video_file_path_editing_finished()
        self.checkBox_tracker.toggled.connect(self.checkBox_tracker_toggled)
        self.checkBox_tracker.setChecked(True)
        self.checkBox_label_img.toggled.connect(self.checkBox_label_img_toggled)
        self.pushButton_save_xml.clicked.connect(self.pushButton_save_xml_clicked)
        pass

    def init_data(self):
        self.src_video_path = None
        self.video_len = None
        self.cur_frame_id = 0
        self.tmr = QTimer()
        self.proc_time = 200
        self.tmr.setInterval(self.proc_time)
        self.tmr.timeout.connect(self.timeout_handler)
        self.tmr.start()
        self.video_capturer = None
        self.frame = None
        self.prev_frame = None
        self.frame_draw = None
        self.proc_qimage = None
        self.proc_qpixmap = None
        self.amount_of_frames = None
        self.create_xml = False
        self.freq_xmls = 2

        self.dir_xmls = None
        self.select_left_corner = False
        self.select_right_corner = False
        self.left_corner = None
        self.right_corner = None
        self.tracker = None
        self.enable_playing_tracker = False

        self.bboxies = []
        self.object_classes = []
        self.dict_class_bbox = {}

        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()

        self.width = None
        self.height = None

        self.name_object = 'phantom'

        self.type_label = 'tracker'
        self.save_xml = False
        pass

    def lineedit_video_file_path_editing_finished(self):
        if os.path.isfile(self.lineEdit_video_file_path.text()):
            self.src_video_path = os.path.basename(self.lineEdit_video_file_path.text())
            self.video_capturer = cv2.VideoCapture(self.lineEdit_video_file_path.text())
            self.cur_frame_id = 0
            self.video_capturer.set(cv2.CAP_PROP_POS_FRAMES, self.cur_frame_id)
            self.amount_of_frames = self.video_capturer.get(cv2.CAP_PROP_FRAME_COUNT)
            self.enable_playing = False
            if self.type_label == 'tracker':
                self.refresh_image_tracker()
            if self.type_label == 'label_img':
                self.refresh_image_tracker_2()
        else:
            print('Error: path to video file is invalid!')
        pass

    def lineedit_xml_dir_path_editing_finished(self):
        if os.path.isdir(self.lineEdit_xml_dir_path.text()):
            self.dir_xmls = self.lineEdit_xml_dir_path.text() + '/'
        else:
            print('Error: path to directory with xmls is invalid')
        pass

    def lineEdit_Proc_time_editing_finished(self):
        self.proc_time = int(self.lineEdit_Proc_time.text())
        self.tmr.setInterval(self.proc_time)
        pass

    def lineEdit_freq_xmls_editing_finished(self):
        self.freq_xmls = int(self.lineEdit_freq_xmls.text())

        pass

    def lineEdit_name_object_editing_finished(self):
        self.name_object = self.lineEdit_name_object.text()
        pass

    def refresh_image_tracker(self):
        if self.type_label == 'tracker':
            self.label_xml.setText('')
            if self.create_xml and self.dir_xmls is None:
                print('Error: path to directory with xmls is invalid')
            if self.amount_of_frames is not None:
                ret, self.frame = self.video_capturer.read()
                if self.frame is not None:
                    a = self.frame.shape[1] / 960
                    b = self.frame.shape[0] / 540
                    if self.enable_playing_tracker:
                        self.frame_draw = self.frame
                        ok, bbox = self.tracker.update(self.frame)
                        if len(self.frame.shape) == 3:
                            self.frame_draw = cv2.cvtColor(self.frame_draw, cv2.COLOR_BGR2RGB)
                        self.frame_draw = cv2.resize(self.frame_draw, (960, 540), interpolation=cv2.INTER_CUBIC)
                        if ok:
                            p1 = (int(bbox[0] / a), int(bbox[1] / b))
                            p2 = (int(bbox[0] / a + bbox[2] / a), int(bbox[1] / b + bbox[3] / b))
                            self.frame_draw = cv2.rectangle(self.frame_draw, p1, p2, (0, 0, 255), 1)
                        self.proc_qimage = convert_ndarr_to_qimg(self.frame_draw)
                        self.proc_qpixmap = QPixmap.fromImage(self.proc_qimage)
                        self.label_video.setPixmap(self.proc_qpixmap)
                        self.label_cur_frame_id.setText(str(self.cur_frame_id))
                        if self.create_xml and int((self.frame.shape[1]-self.frame.shape[0]) / 2) < bbox[0] < (self.frame.shape[0] + int((self.frame.shape[1]-self.frame.shape[0]) / 2) - bbox[2]) and self.cur_frame_id % self.freq_xmls == 0 \
                                and (self.dir_xmls is not None) and 0 < bbox[1] < int(self.frame.shape[0] - bbox[3]):
                            shutil.copyfile('v1_816.xml', self.dir_xmls + self.src_video_path[:-4] + '_' + str(self.cur_frame_id) +'.xml')
                            with open(self.dir_xmls + self.src_video_path[:-4] + '_' + str(self.cur_frame_id) +'.xml', 'r+') as f:
                                lines = f.readlines()
                                string_2 = lines[2]
                                string_3 = lines[3]
                                string_8 = lines[8]
                                string_9 = lines[9]
                                string_10 = lines[10]
                                string_14 = lines[14]
                                string_19 = lines[19]
                                string_20 = lines[20]
                                string_21 = lines[21]
                                string_22 = lines[22]
                                new_str_2 = string_2.replace(string_2, '\t<filename>' + self.src_video_path[:-4] + '_' +
                                                             str(self.cur_frame_id) + '.jpg</filename>\n')
                                new_str_3 = string_3.replace(string_3, '\t<path>' + self.dir_xmls[:-18] + 'images/' +
                                                             self.src_video_path[:-4] + '_' + str(self.cur_frame_id) +
                                                             '.jpg</path>\n')
                                new_str_8 = string_8.replace(string_8, '\t\t<width>' + str(self.frame.shape[0]) +
                                                             '</width>\n')
                                new_str_9 = string_9.replace(string_9, '\t\t<height>' + str(self.frame.shape[0]) +
                                                             '</height>\n')
                                new_str_10 = string_10.replace(string_10, '\t\t<depth>' + str(self.frame.shape[2]) +
                                                               '</depth>\n')
                                new_str_14 = string_14.replace(string_14, '\t\t<name>' + self.name_object + '</name>\n')
                                new_str_19 = string_19.replace(string_19, '\t\t\t<xmin>' + str(int(bbox[0]) -
                                                                                               int((self.frame.shape[1] -
                                                                                                    self.frame.shape[0]) / 2)) +
                                                               '</xmin>\n')
                                new_str_20 = string_20.replace(string_20, '\t\t\t<ymin>' + str(int(bbox[1])) +
                                                               '</ymin>\n')
                                new_str_21 = string_21.replace(string_21, '\t\t\t<xmax>' +
                                                               str(int(bbox[0] + bbox[2] -
                                                                       int((self.frame.shape[1] -
                                                                            self.frame.shape[0]) / 2))) + '</xmax>\n')
                                new_str_22 = string_22.replace(string_22, '\t\t\t<ymax>' + str(int(bbox[1] + bbox[3])) +
                                                               '</ymax>\n')
                                lines[2] = new_str_2
                                lines[3] = new_str_3
                                lines[8] = new_str_8
                                lines[9] = new_str_9
                                lines[10] = new_str_10
                                lines[14] = new_str_14
                                lines[19] = new_str_19
                                lines[20] = new_str_20
                                lines[21] = new_str_21
                                lines[22] = new_str_22
                                f.seek(0)
                                f.writelines(lines)
                                f.close
                                cv2.imwrite(self.dir_xmls[:-18] + 'images/' + self.src_video_path[:-4] +
                                            '_' + str(self.cur_frame_id) +'.jpg', self.frame[0:self.frame.shape[0],
                                                                                  int((self.frame.shape[1] -
                                                                                       self.frame.shape[0]) / 2):
                                                                                  int((self.frame.shape[1] -
                                                                                       self.frame.shape[0]) / 2 +
                                                                                      self.frame.shape[0])])
                                cv2.imwrite(self.dir_xmls[:-18] + 'images_with_label/' + self.src_video_path[:-4] +
                                            '_' + str(self.cur_frame_id) +'.jpg',
                                            cv2.rectangle(self.frame,(int(bbox[0]), int(bbox[1])),
                                                          (int(bbox[0]+ bbox[2]), int(bbox[1] + bbox[3])), (0, 0, 255), 1))
                                print(self.src_video_path[:-4] + '_' + str(self.cur_frame_id) +
                                      '.jpg is saved in ' + self.dir_xmls[:-18] + 'images/')
                        if not self.create_xml or self.dir_xmls is None:
                            self.label_xml.setText("<font color = 'red'> XMLS_ARE_NOT_CREATING </font>")

                    if not self.enable_playing_tracker:
                        self.frame_draw = self.frame
                        if len(self.frame.shape) == 3:
                            self.frame_draw = cv2.cvtColor(self.frame_draw, cv2.COLOR_BGR2RGB)
                        self.frame_draw = cv2.resize(self.frame_draw, (960, 540), interpolation=cv2.INTER_CUBIC)
                        self.proc_qimage = convert_ndarr_to_qimg(self.frame_draw)
                        self.proc_qpixmap = QPixmap.fromImage(self.proc_qimage)
                        self.label_video.setPixmap(self.proc_qpixmap)
                        self.label_cur_frame_id.setText(str(self.cur_frame_id))
        pass

    def pushButton_save_xml_clicked(self):
        self.save_xml = True
        self.refresh_image_tracker_2()
        pass

    def refresh_image_tracker_2(self):
        if self.dir_xmls is None:
            print('Error: path to directory with xmls is invalid')
        if self.type_label == 'label_img':
            self.label_xml.setText('')
            if self.amount_of_frames is not None:
                self.video_capturer.set(cv2.CAP_PROP_POS_FRAMES, self.cur_frame_id)
                ret, self.frame = self.video_capturer.read()
                bboxies = []
                if self.frame is not None:
                    self.frame_draw = self.frame
                    a = self.frame.shape[1] / 960
                    b = self.frame.shape[0] / 540
                    if len(self.bboxies) > 0 and self.dir_xmls is not None:
                        cv2.imwrite(self.dir_xmls[:-18] + 'images/' + self.src_video_path[:-4] + '_' +
                                    str(self.cur_frame_id) + '.jpg',self.frame[0:self.frame.shape[0],
                                    int((self.frame.shape[1] - self.frame.shape[0]) / 2):int((self.frame.shape[1] -
                                                                                              self.frame.shape[0]) / 2 +
                                                                                             self.frame.shape[0])])
                        Image = self.frame[0:self.frame.shape[0],int((self.frame.shape[1] - self.frame.shape[0]) / 2):
                                                                 int((self.frame.shape[1] - self.frame.shape[0]) / 2 +
                                                                     self.frame.shape[0])]
                        for i in range(len(self.bboxies)):
                            self.frame = cv2.rectangle(self.frame, (int(self.bboxies[i][0]),int(self.bboxies[i][1])),
                                                (int(self.bboxies[i][2]), int(self.bboxies[i][3])), (255, 0, 0))
                        cv2.imwrite(self.dir_xmls[:-18] + 'images_with_label/' + self.src_video_path[:-4] + '_' +
                                    str(self.cur_frame_id) + '.jpg', self.frame)
                        print(self.src_video_path[:-4] + '_' + str(self.cur_frame_id) + '.jpg is saved in ' +
                              self.dir_xmls[:-18] + 'images/')
                        file = open(self.dir_xmls + self.src_video_path[:-4] + '_' + str(self.cur_frame_id) +'.xml', 'w')
                        lines = []
                        lines.append('<annotation>\n')
                        lines.append('\t<folder>images</folder>\n')
                        lines.append('\t<filename>' + self.src_video_path[:-4] + '_' + str(self.cur_frame_id) +
                                     '.jpg</filename>\n')
                        lines.append('\t<path>' + self.dir_xmls[:-18] + 'images/' + self.src_video_path[:-4] +
                                     '_' + str(self.cur_frame_id) +'.jpg</path>\n')
                        lines.append('\t<source>\n')
                        lines.append('\t\t<database>Unknown</database>\n')
                        lines.append('\t</source>\n')
                        lines.append('\t<size>\n')
                        lines.append('\t\t<width>' + str(self.frame.shape[0]) + '</width>\n')
                        lines.append('\t\t<height>' + str(self.frame.shape[0]) + '</height>\n')
                        lines.append('\t\t<depth>' + str(self.frame.shape[2]) + '</depth>\n')
                        lines.append('\t</size>\n')
                        lines.append('\t<segmented>0</segmented>\n')

                        for i in range(len(self.bboxies)):
                            if int((self.frame.shape[1] - self.frame.shape[0]) / 2) < self.bboxies[i][0] and \
                                    int((self.frame.shape[1] + self.frame.shape[0]) / 2) > self.bboxies[i][2]:
                                lines.append('\t<object>\n  ')
                                lines.append('\t\t<name>' + self.object_classes[i] + '</name>\n')
                                lines.append('\t\t<pose>Unspecified</pose>\n')
                                lines.append('\t\t<truncated>0</truncated>\n')
                                lines.append('\t\t<difficult>0</difficult>\n')
                                lines.append('\t\t<bndbox>\n')
                                lines.append('\t\t\t<xmin>' + str(int(self.bboxies[i][0]) -
                                                                  int((self.frame.shape[1]-self.frame.shape[0]) / 2)) +
                                             '</xmin>\n')
                                lines.append('\t\t\t<ymin>' + str(int(self.bboxies[i][1])) + '</ymin>\n')
                                lines.append('\t\t\t<xmax>' + str(int(self.bboxies[i][2] -
                                                                      int((self.frame.shape[1] -
                                                                           self.frame.shape[0]) / 2))) + '</xmax>\n')
                                lines.append('\t\t\t<ymax>' + str(int(self.bboxies[i][3])) + '</ymax>\n')
                                lines.append('\t\t</bndbox>\n')
                                lines.append('\t</object>\n')
                                bboxi = (int(self.bboxies[i][0]) - int((self.frame.shape[1] - self.frame.shape[0]) / 2),
                                         int(self.bboxies[i][1]),
                                         int(self.bboxies[i][2]) - int((self.frame.shape[1] - self.frame.shape[0]) / 2),
                                         int(self.bboxies[i][3]))
                                bboxies.append(bboxi)
                            if int((self.frame.shape[1] - self.frame.shape[0]) / 2) < int(self.bboxies[i][0]) < \
                                    int((self.frame.shape[1] + self.frame.shape[0]) / 2) and \
                                    int(self.bboxies[i][2]) > int((self.frame.shape[1] + self.frame.shape[0]) / 2):
                                lines.append('\t<object>\n')
                                lines.append('\t\t<name>' + self.object_classes[i] + '</name>\n')
                                lines.append('\t\t<pose>Unspecified</pose>\n')
                                lines.append('\t\t<truncated>0</truncated>\n')
                                lines.append('\t\t<difficult>0</difficult>\n')
                                lines.append('\t\t<bndbox>\n')
                                lines.append('\t\t\t<xmin>' + str(int(self.bboxies[i][0]) - int((self.frame.shape[1] -
                                                                                                 self.frame.shape[0]) / 2)) +
                                             '</xmin>\n')
                                lines.append('\t\t\t<ymin>' + str(int(self.bboxies[i][1])) + '</ymin>\n')
                                lines.append('\t\t\t<xmax>' + str(int(self.frame.shape[0])) + '</xmax>\n')
                                lines.append('\t\t\t<ymax>' + str(int(self.bboxies[i][3])) + '</ymax>\n')
                                lines.append('\t\t</bndbox>\n')
                                lines.append('\t</object>\n')
                                bboxi = (int(self.bboxies[i][0]) - int((self.frame.shape[1] - self.frame.shape[0]) / 2),
                                         int(self.bboxies[i][1]), int(self.frame.shape[0]),
                                int(self.bboxies[i][3]))
                                bboxies.append(bboxi)

                            if int(self.bboxies[i][0]) < int((self.frame.shape[1] - self.frame.shape[0]) / 2) and \
                                    int((self.frame.shape[1] - self.frame.shape[0]) / 2) < int(self.bboxies[i][2]) < \
                                    int((self.frame.shape[1] + self.frame.shape[0]) / 2):
                                lines.append('\t<object>\n')
                                lines.append('\t\t<name>' + self.object_classes[i] + '</name>\n')
                                lines.append('\t\t<pose>Unspecified</pose>\n')
                                lines.append('\t\t<truncated>0</truncated>\n')
                                lines.append('\t\t<difficult>0</difficult>\n')
                                lines.append('\t\t<bndbox>\n')
                                lines.append('\t\t\t<xmin>' + str(0) + '</xmin>\n')
                                lines.append('\t\t\t<ymin>' + str(int(self.bboxies[i][1])) + '</ymin>\n')
                                lines.append('\t\t\t<xmax>' + str(int(self.bboxies[i][2]) - int((self.frame.shape[1] - self.frame.shape[0]) / 2)) + '</xmax>\n')
                                lines.append('\t\t\t<ymax>' + str(int(self.bboxies[i][3])) + '</ymax>\n')
                                lines.append('\t\t</bndbox>\n')
                                lines.append('\t</object>\n')
                                bboxi = (0, int(self.bboxies[i][1]), int(self.bboxies[i][2]) - int((self.frame.shape[1] - self.frame.shape[0]) / 2),
                                         int(self.bboxies[i][3]))
                                bboxies.append(bboxi)
                            if int(self.bboxies[i][0]) < int((self.frame.shape[1] - self.frame.shape[0]) / 2) and int(self.bboxies[i][2]) > int((self.frame.shape[1] + self.frame.shape[0]) / 2):  # объект выходит за пределы квадрата
                                lines.append('\t<object>\n')
                                lines.append('\t\t<name>' + self.object_classes[i] + '</name>\n')
                                lines.append('\t\t<pose>Unspecified</pose>\n')
                                lines.append('\t\t<truncated>0</truncated>\n')
                                lines.append('\t\t<difficult>0</difficult>\n')
                                lines.append('\t\t<bndbox>\n')
                                lines.append('\t\t\t<xmin>' + str(0) + '</xmin>\n')
                                lines.append('\t\t\t<ymin>' + str(int(self.bboxies[i][1])) + '</ymin>\n')
                                lines.append('\t\t\t<xmax>' + str(int(self.frame.shape[0])) + '</xmax>\n')
                                lines.append('\t\t\t<ymax>' + str(int(self.bboxies[i][3])) + '</ymax>\n')
                                lines.append('\t\t</bndbox>\n')
                                lines.append('\t</object>\n')
                                bboxi = (0, int(self.bboxies[i][1]), int(self.frame.shape[0]), int(self.bboxies[i][3]))
                                bboxies.append(bboxi)
                        lines.append('</annotation>\n')
                        file.writelines(lines)
                        file.close()
                    if self.dir_xmls is None or len(self.bboxies) == 0:
                        self.label_xml.setText("<font color = 'red'> XMLS_ARE_NOT_CREATING </font>")
                    if len(self.bboxies) == 0:
                        print('Error: Label image')
                    for i in range(len(bboxies)):
                        self.frame = cv2.rectangle(Image, (bboxies[i][0], bboxies[i][1]),(bboxies[i][2], bboxies[i][3]),
                                                   (255, 0, 0))
                    if len(bboxies) != 0:
                        cv2.imwrite(self.dir_xmls[:-18] + 'images_with_label/' + self.src_video_path[:-4] + '_' + str(
                        self.cur_frame_id) + '.jpg', self.frame)
                    self.cur_frame_id += 1
                    self.video_capturer.set(cv2.CAP_PROP_POS_FRAMES, self.cur_frame_id)
                    ret, self.frame = self.video_capturer.read()
                    self.frame_draw = self.frame
                    if len(self.frame.shape) == 3:
                        self.frame_draw = cv2.cvtColor(self.frame_draw, cv2.COLOR_BGR2RGB)
                    self.frame_draw = cv2.resize(self.frame_draw, (960, 540), interpolation=cv2.INTER_CUBIC)
                    self.proc_qimage = convert_ndarr_to_qimg(self.frame_draw)
                    self.proc_qpixmap = QPixmap.fromImage(self.proc_qimage)
                    self.label_video.setPixmap(self.proc_qpixmap)
                    self.label_cur_frame_id.setText(str(self.cur_frame_id))
                    self.bboxies = []
                    self.object_classes = []
                pass




    def labeling_image(self):
        self.left_corner = (self.begin.x() - 20, self.begin.y() - 20)
        self.right_corner = (self.end.x() - 20, self.end.y() - 20)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        a = self.frame.shape[1] / 960
        b = self.frame.shape[0] / 540
        bbox = (int(self.left_corner[0] * a), int(self.left_corner[1] * b), int(self.right_corner[0] * a),
                int(self.right_corner[1] * b))
        self.video_capturer.set(cv2.CAP_PROP_POS_FRAMES,
                                self.cur_frame_id)
        self.object_classes.append(self.name_object)
        self.bboxies.append(bbox)
        self.frame_draw = cv2.rectangle(self.frame_draw, (int((self.frame.shape[1] / a - self.frame.shape[0] / b) / 2), 0), (int((self.frame.shape[1] / a + self.frame.shape[0] / b) / 2), int(self.frame.shape[0] / b)),(0, 255, 0), 1)
        for i in range(len(self.bboxies)):
            self.frame_draw = cv2.rectangle(self.frame_draw, (int(self.bboxies[i][0] / a),int(self.bboxies[i][1] / b)),
                                            (int(self.bboxies[i][2] / a), int(self.bboxies[i][3] / b)), (255, 0, 0), 1)
        self.proc_qimage = convert_ndarr_to_qimg(self.frame_draw)
        self.proc_qpixmap = QPixmap.fromImage(self.proc_qimage)
        self.label_video.setPixmap(self.proc_qpixmap)
        self.label_cur_frame_id.setText(str(self.cur_frame_id))
        pass


    def pushbuttone_init_tracker_clicked(self):
        self.initialize_tracker(cv2.TrackerCSRT_create())
        pass


    def initialize_tracker(self, tracker_type):
        self.left_corner = (self.begin.x() - 20, self.begin.y() - 20)
        self.right_corner = (self.end.x() - 20, self.end.y() - 20)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.tracker = tracker_type
        bbox = (self.left_corner[0], self.left_corner[1], self.right_corner[0] - self.left_corner[0], self.right_corner[1] - self.left_corner[1])
        a = self.frame.shape[1] / 960
        b = self.frame.shape[0] / 540
        print(int(bbox[0] * a), int(bbox[1] * b), int(bbox[2] * a), int(bbox[3] * b))
        self.video_capturer.set(cv2.CAP_PROP_POS_FRAMES, self.cur_frame_id)
        ok, self.init_frame = self.video_capturer.read()
        if ok:

            if len(self.init_frame.shape) == 3:
                self.frame_draw = cv2.cvtColor(self.init_frame, cv2.COLOR_BGR2RGB)
            self.frame_draw = cv2.resize(self.frame_draw, (960, 540), interpolation=cv2.INTER_CUBIC)
            self.frame_draw = cv2.rectangle(self.frame_draw, self.left_corner, self.right_corner, (255, 0, 0), 1)
            self.proc_qimage = convert_ndarr_to_qimg(self.frame_draw)
            self.proc_qpixmap = QPixmap.fromImage(self.proc_qimage)
            self.label_video.setPixmap(self.proc_qpixmap)
            self.label_cur_frame_id.setText(str(self.cur_frame_id))
            self.ok = self.tracker.init(self.init_frame, (int(bbox[0] * a), int(bbox[1] * b), int(bbox[2] * a), int(bbox[3] * b)))
        if not ok:
            print('Cannot read video!')
        pass



    def pushbutton_play_clicked(self):
        self.enable_playing_tracker = not self.enable_playing_tracker
        if self.enable_playing_tracker:
            self.pushButton_play.setText('Pause')
        else:
            self.pushButton_play.setText('Play')
        pass

    def pushbutton_forward_clicked(self):
        self.video_capturer.set(cv2.CAP_PROP_POS_FRAMES, self.cur_frame_id)
        if self.type_label == 'tracker':
            self.cur_frame_id += 1
            self.refresh_image_tracker()
        elif self.type_label == 'label_img':
            self.bboxies = []
            self.object_classes = []
            self.refresh_image_tracker_2()

        pass

    def pushbutton_back_clicked(self):
        self.video_capturer.set(cv2.CAP_PROP_POS_FRAMES, self.cur_frame_id)
        if self.type_label == 'tracker':
            self.cur_frame_id -= 1
            self.refresh_image_tracker()
        elif self.type_label == 'label_img':
            self.bboxies = []
            self.object_classes = []
            self.cur_frame_id -= 2
            self.refresh_image_tracker_2()
        pass

    def timeout_handler(self):
        if self.enable_playing_tracker and self.type_label == 'tracker':
            self.cur_frame_id += 1

            self.refresh_image_tracker()
        pass

    def checkBox_create_xml_toggled(self, checked):
        self.create_xml = checked
        pass

    def pushbutton_select_video_file_clicked(self):
        fname = QFileDialog.getOpenFileName(self, 'Select video file', '')[0]
        if fname is not None:
            self.src_video_path = os.path.basename(fname)
            self.lineEdit_video_file_path.setText(fname)
            self.lineedit_video_file_path_editing_finished()
        pass

    def pushbutton_select_dir_xml_clicked(self):
        fname = None
        dialog = QFileDialog(self, 'Select directory to xmls:')
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        if dialog.exec_() == QDialog.Accepted:
            fname = dialog.selectedFiles()[0] + '/'
        if fname is not None:
            self.lineEdit_xml_dir_path.setText(fname)
            self.lineedit_xml_dir_path_editing_finished()
        pass

    def checkBox_tracker_toggled(self, checked):
        if checked:
            self.type_label = 'tracker'
            self.refresh_image_tracker_2()
        else:
            self.type_label = 'none'
        self.switch_type_of_labeling(self.type_label)
        pass

    def checkBox_label_img_toggled(self, checked):
        if checked:
            self.type_label = 'label_img'
        else:
            self.type_label = 'none'
        self.switch_type_of_labeling(self.type_label)
        pass

    def switch_type_of_labeling(self, type_label):
        if type_label == 'tracker':
            self.checkBox_tracker.setChecked(True)
            self.checkBox_label_img.setChecked(False)
        elif type_label == 'label_img':
            self.checkBox_tracker.setChecked(False)
            self.checkBox_label_img.setChecked(True)
        else:
            self.checkBox_tracker.setChecked(False)
            self.checkBox_label_img.setChecked(False)
        pass

    def paintEvent(self, event):
        qp = QPainter()
        pen = QPen(QtCore.Qt.red, 1)
        width = self.end.x() - self.begin.x()
        height = self.end.y() - self.begin.y()
        if self.frame is not None:

            qp.begin(self.label_video.pixmap())
            qp.setPen(pen)
            qp.drawRect(self.begin.x() - 20, self.begin.y() - 20, width, height)
            qp.end()

    def mousePressEvent(self, event):
        self.video_capturer.set(cv2.CAP_PROP_POS_FRAMES, self.cur_frame_id)
        self.refresh_image_tracker()
        self.begin = event.pos()
        self.end = event.pos()
        self.update()

        pass

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()
        self.left_corner = (self.begin.x() - 20, self.begin.y() - 20)
        self.right_corner = (self.end.x() - 20, self.end.y() - 20)
        if len(self.frame.shape) == 3:
            self.frame_draw = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        self.frame_draw = cv2.resize(self.frame_draw, (960, 540), interpolation=cv2.INTER_CUBIC)
        self.frame_draw = cv2.rectangle(self.frame_draw, self.left_corner, self.right_corner, (255, 0, 0), 1)
        self.proc_qimage = convert_ndarr_to_qimg(self.frame_draw)
        self.proc_qpixmap = QPixmap.fromImage(self.proc_qimage)
        self.label_video.setPixmap(self.proc_qpixmap)

    def mouseReleaseEvent(self, event):
        self.end = event.pos()
        self.update()
        if 20 < self.begin.x() < 980 and 20 < self.end.x() < 980 and 20 < self.begin.y() < 560 and 20 < self.end.y() < 560 and self.end.x() != self.begin.x() and self.end.y() != self.begin.y():
            if self.type_label == 'tracker':
                self.pushbuttone_init_tracker_clicked()
            elif self.type_label == 'label_img':
                self.labeling_image()
        pass


    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.pushbutton_play_clicked()
        if event.key() == QtCore.Qt.Key_F12:
            self.checkBox_create_xml.setChecked(not self.create_xml)
        if event.key() == QtCore.Qt.Key_F11:
            self.pushButton_save_xml_clicked()
        pass


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = guiApp()
    window.show()
    sys.exit(app.exec_())
    pass

if __name__ == '__main__':
    main()
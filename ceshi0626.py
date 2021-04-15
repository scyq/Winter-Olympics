from test0625 import Ui_MainWindow
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QTimer,QCoreApplication
from PyQt5.QtGui import *
import cv2
import qimage2ndarray
import time
import numpy as np
import os
from scipy.spatial.distance import pdist
import matplotlib.pyplot as plt # plt 用于显示图片
import matplotlib.image as mpimg
# import glob
# from natsort import natsorted
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
# from matplotlib import pyplot as plt
# import scipy.cluster.hierarchy as sch
# from matplotlib import pyplot as plt
# import natsort
# from scipy.cluster.vq import kmeans, whiten
np.seterr(divide='ignore', invalid='ignore')

class CamShow(QMainWindow,Ui_MainWindow):
    def __del__(self):
        try:
            self.camera.release()  # 释放资源
        except:
            return
    def __init__(self,parent=None):
        super(CamShow,self).__init__(parent)
        self.setupUi(self)
        self.PrepWidgets()
        self.PrepParameters()
        self.CallBackFunctions()
        self.time_map = {}
        self.map1={}
        self.map1[3] = 3
        self.map1[8] = 8
        self.map1[16] = 16
        self.map1[21] = 21
        self.map1[24] = 24
        self.map1[41] = 41
        self.map1[43] = 43
        self.map1[45] = 45
        # 设置数据层次结构，4行4列
        self.setWindowTitle('冰壶比赛辅助转播系统-BJUT')
        self.model = QStandardItemModel(0, 4)
        # 设置水平方向四个头标签文本内容
        self.model.setHorizontalHeaderLabels(['镜头', '起始帧', '终止帧', '帧数'])
        # 设置每个位置的文本值
        self.Timer=QTimer()
        self.Timer.timeout.connect(self.TimerOutFun)
        self.Timer1 = QTimer()
        self.Timer1.timeout.connect(self.showd)
        self.hLay = QHBoxLayout()
        self.hLay1 = QHBoxLayout()
        self.cen1 = []
    def PrepWidgets(self):
        self.StopBt.setEnabled(False)
        self.RecordBt.setEnabled(False)
        self.ShowBt.setEnabled(False)
        self.pushButton.setEnabled(False)
    def PrepCamera(self):
        try:
            x = self.RecordPath_2
            self.camera=cv2.VideoCapture(x)
            self.number = self.camera.get(cv2.CAP_PROP_FRAME_COUNT)
            self.progressBar.setMaximum(self.number)
            self.cap = cv2.VideoCapture(x)
            self.ret, self.img1 = self.camera.read()
            self.ret, self.img2 = self.camera.read()
            self.ret, self.img3 = self.camera.read()
            self.ret, self.img4 = self.camera.read()
            self.ret, self.img5 = self.camera.read()
            self.ret, self.img6 = self.camera.read()
            self.ret, self.img7 = self.camera.read()
            size = self.img1.shape
            self.h = size[0]
            self.w = size[1]
            self.cols = 50
            self.rows = 50
            self.a = int(self.h / self.cols) * int(self.w / self.rows)
            self.MsgTE.clear()
            self.MsgTE.append(self.RecordPath_2)
            self.MsgTE.setPlainText()
        except Exception as e:
            self.MsgTE.clear()
            self.MsgTE.append(str(e))
    def PrepParameters(self):
        self.RecordFlag=0
        self.RecordPath=''
        self.RecordPath_2 = ''
        self.FilePathLE.setText(self.RecordPath)
        self.FilePathLE_2.setText(self.RecordPath_2)
        self.Image_num=2
        self.MsgTE.clear()
        self.pre = 0
        self.num1 = 0
    def CallBackFunctions(self):
        self.FilePathBt.clicked.connect(self.SetFilePath)
        self.FilePathBt_2.clicked.connect(self.SetFilePath1)
        self.ShowBt.clicked.connect(self.StartCamera)
        self.StopBt.clicked.connect(self.StopCamera)
        self.RecordBt.clicked.connect(self.RecordCamera)
        self.ExitBt.clicked.connect(self.ExitApp)
        self.pushButton.clicked.connect(self.push)
    def StartCamera(self):
        if self.ShowBt.text() == '开始':
            self.ShowBt.setText('结束')
            self.StopBt.setEnabled(True)
            self.RecordBt.setEnabled(True)
            self.RecordBt.setText('录像')
            self.Timer.start(1)
            self.timelb=time.clock()
            self.MsgTE.setPlainText('开始')
            self.numlist = []
            for i in range(self.hLay.count()):
                self.hLay.itemAt(i).widget().deleteLater()
            for i in range(self.hLay1.count()):
                self.hLay1.itemAt(i).widget().deleteLater()
        else:
            self.ShowBt.setText('开始')
            self.StopBt.setText('暂停')
            self.RecordBt.setText('录像')
            self.StopBt.setEnabled(False)
            self.RecordBt.setEnabled(False)
            self.ShowBt.setEnabled(False)
            self.camera.release()
            cv2.destroyAllWindows()
            self.Timer.stop()
            self.MsgTE.setPlainText('结束')
            self.Image_num = 2
    def SetFilePath(self):
        dirname = QFileDialog.getExistingDirectory(self, '浏览', '.')
        if dirname:
            self.FilePathLE.setText(dirname)
            self.RecordPath=dirname+'/'
            self.MsgTE.setPlainText(dirname)
    def SetFilePath1(self):
        dirname = QFileDialog.getOpenFileName(self, '浏览2','', 'Video files(*.avi *.mp4 *.wmv *.MOV)')
        if dirname:
            self.FilePathLE_2.setText(dirname[0])
            self.RecordPath_2=dirname[0]
            self.PrepCamera()
            self.MsgTE.clear()
            self.ShowBt.setEnabled(True)
            self.model.removeRows(0, self.num1)
            self.Image_num = 2
            self.ShowBt.setText('开始')
            self.StopBt.setText('暂停')
            self.RecordBt.setText('录像')
            self.StopBt.setEnabled(False)
            self.RecordBt.setEnabled(False)
            self.ShowBt.setEnabled(True)
            self.MsgTE.setPlainText(dirname[0])

    def mouseMoveEvent(self, event):
        s = event.windowPos()
        snum = int(s.x()) - 431
        if snum in self.cen1 and 524 < int(s.y()) < 546 and self.StopBt.text() == '继续':
            xnum = snum/600*self.number
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, xnum)
            x,y = self.cap.read()
            self.Image1 = y
            self.DispImg1()
    def push(self):
        a = self.textEdit.toPlainText()
        try:
            b = self.time_map[int(a)]
            startnum = int(b[0])
            self.countnum = int(b[1]) - int(b[0])
            self.count = 0
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, startnum)
            self.Timer1.start(1)
        except Exception as e:
            self.MsgTE.clear()
            self.MsgTE.append(str(e))
    def showd(self):
        self.count += 1
        x, y = self.cap.read()
        self.Image1 = y
        self.DispImg1()
        if self.count > self.countnum:
            self.Timer1.stop()

    def insertButton(self,i):
        if  i == 3 or i == 8  or i == 16 or i == 21  or i == 41 or i == 43 or i == 45 :
            widget = QWidget()
            self.updateBtn = QPushButton('镜头'+str(i)+'冰壶轨迹',self)
            self.updateBtn.clicked.connect(lambda: self.on_click(self.sender().text()))
            hLayout = QHBoxLayout()
            hLayout.addWidget(self.updateBtn)
            widget.setLayout(hLayout)
            return widget

    def on_click(self,i):
        self.MsgTE.setPlainText("位置数据生成成功")
        self.time_list = []
        arr1 = []
        number = filter(str.isdigit, i)
        number = list(number)
        number = int(''.join(number))
        self.time_list = self.time_map[number]
        self.cap.set(cv2.CAP_PROP_POS_FRAMES,int(self.time_list[0]))
        num = int(self.time_list[1])-int(self.time_list[0])+1
        for i in range(num):
            a, b = self.cap.read()
            if i % 3 == 0:
                hist_h1 = cv2.calcHist([b], [0], None, [256], [0, 255])
                hist_h2 = cv2.calcHist([b], [1], None, [256], [0, 255])
                hist_h3 = cv2.calcHist([b], [2], None, [256], [0, 255])
                hist = np.vstack((hist_h1, hist_h2, hist_h3))
                arr1.append(hist)
            # cv2.imwrite('C:\\Users\\dd\\Desktop\\tt\\%04d.jpeg'%(i+1), b)
        temp = self.map1[number]
        frame_img = cv2.imread('C:\\Users\\dd\\Desktop\\cutshow\\%d.jpeg' % temp, 1);
        cv2.namedWindow("result", 0);

        cv2.resizeWindow("result", 240, 6000);

        cv2.imshow('result', frame_img)

        # os.system('''conda.bat activate "C:\ProgramData\Anaconda3"&\
        #                   python C:/Users/dd/Desktop/temp/test%d.py --url wss://kirnu-ws2.stereye.tech --password kirnu&''' % temp)

        cv2.waitKey(0)
        # frame_img =cv2.imread('C:\\Users\\dd\\Desktop\\cutshow\\%d.jpeg'%temp,1);
        # cv2.namedWindow("result",0);
        #
        # cv2.resizeWindow("result", 240, 6000);
        #
        # cv2.imshow('result',frame_img)
        # cv2.waitKey(0)


        arr = np.array(arr1)
        arr = np.squeeze(arr)
        c, r = arr.shape
        for i in range(r):
            for j in range(i, c):
                if arr[i][j] != arr[j][i]:
                    arr[i][j] = arr[j][i]
        for i in range(r):
            for j in range(i, c):
                if arr[i][j] != arr[j][i]:
                    print(arr[i][j], arr[j][i])

        num_clusters, indices = self.hierarchy_cluster(arr)

        print("%d clusters" % num_clusters)
        cen = []
        for k, ind in enumerate(indices):
            if len(ind) >= 10:
                ind3 = []
                ind1 = [arr1[i] for i in range(min(ind), max(ind))]
                for j in ind1:
                    ind2 = [np.linalg.norm(j - i) for i in ind1]
                    d = sum(ind2)
                    ind3.append(d)
                center = ind3.index(min(ind3))
                center = center*3 + int(self.time_list[0])
                cen.append(center)
                self.cen1.append(round(center/self.number*600))
                # print("cluster", k + 1, "is", ind)
        self.tableWidget_2.setColumnCount(1)
        self.tableWidget_2.setRowCount(1)
        self.tableWidget_2.setColumnWidth(0, 320)
        self.tableWidget_2.setItem(0, 0, QTableWidgetItem('关键帧为:' + ",".join(str(x) for x in cen)))
        QTableWidget.resizeRowsToContents(self.tableWidget_2)
        self.area1 = Paintarea1()
        self.area1.getnum(self.cen1)
        for i in range(self.hLay1.count()):
            self.hLay1.itemAt(i).widget().deleteLater()
        self.hLay1.addWidget(self.area1)
        self.widget_2.setLayout(self.hLay1)
        for i in cen:
            widget = QWidget()
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            res, frame = self.cap.read()
            label = QLabel(widget)
            xy = frame.shape[0]/frame.shape[1]
            frame = cv2.resize(frame,(300,round(300*xy)),interpolation=cv2.INTER_AREA)
            img2 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # label.setText(str(i))
            img = QImage(img2[:], frame.shape[1], frame.shape[0], frame.shape[1]*3 ,QImage.Format_RGB888)
            label.setPixmap(QPixmap(img))
            rows = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(rows)
            self.tableWidget_2.setRowHeight(rows, round(300*xy))
            self.tableWidget_2.setCellWidget(rows, 0, widget)

    def TimerOutFun(self):

        success, img = self.camera.read()

        if success:
            self.Image=self.img5
            self.DispImg()
            self.Image_num += 1

            if self.RecordFlag:
                self.video_writer.write(img)
            # if self.Image_num%10==9:
                # frame_rate=10/(time.clock()-self.timelb)
            num = self.Image_num
            self.FmRateLCD.display(num)
            self.timelb=time.clock()
            self.ImgWidthLCD.display(self.camera.get(3))
            self.ImgHeightLCD.display(self.camera.get(4))

            if self.barMinus(self.img4,self.img5)>=0.15:
                if self.barMinus(self.img1, img) >= 0.16:
                    imga = self.crop(self.img4)
                    imgb = self.crop(self.img5)
                    if self.barMinus_crop(imga, imgb) <= 30:
                        if self.Image_num-(self.pre+1)>=10:
                            self.num1 += 1
                            if self.num1 == 3 or self.num1 == 8 or self.num1 == 16 or self.num1 == 21 or self.num1 == 41 or self.num1 == 43 or self.num1 == 45 :
                                self.StopBt.setText('继续')
                                self.RecordBt.setText('保存')
                                self.Timer.stop()
                                # self.MsgTE.setPlainText("暂停")
                                self.pushButton.setEnabled(True)
                            self.time_map[self.num1] = [self.pre + 1, self.Image_num]
                            self.model.appendRow([
                                QStandardItem('镜头'+str(self.num1)),
                                QStandardItem(str(self.pre+1)),
                                QStandardItem(str(self.Image_num)),
                                QStandardItem(str(self.Image_num - self.pre)),
                            ])
                            self.row_cnt = self.tableWidget.rowCount()
                            self.tableWidget.insertRow(self.row_cnt)
                            self.tableWidget.setItem(self.num1 - 1, 0, QTableWidgetItem('镜头'+str(self.num1)))
                            self.tableWidget.setCellWidget(self.num1-1, 1, self.insertButton(self.num1))
                            QTableWidget.resizeRowsToContents(self.tableWidget)
                            # hists=[]
                            # for i in range(self.pre+2,self.Image_num,5):
                            #     self.cap.set(cv2.CAP_PROP_POS_FRAMES, i)
                            #     a, b = self.cap.read()
                            #     if a:
                            #         hsv = cv2.cvtColor(b, cv2.COLOR_BGR2HSV)
                            #         color_histgrams2 = [cv2.calcHist([hsv], [c], None, [16], [0, 256]) for c in
                            #                             range(3)]
                            #         color_histgrams = np.array(
                            #             [chist / float(sum(chist)) for chist in color_histgrams2])
                            #         hists.append(color_histgrams.flatten())
                            # KF=self.feature_cluster(hists)
                            #
                            # print(KF)
                            self.pre = self.Image_num
                            self.numlist.append(self.Image_num/self.number*600)
                            self.area = Paintarea()
                            self.area.getnum(self.numlist)
                            for i in range(self.hLay.count()):
                                self.hLay.itemAt(i).widget().deleteLater()
                            self.hLay.addWidget(self.area)
                            self.widget.setLayout(self.hLay)
                        else:
                            self.pre = self.Image_num

            self.img1 = self.img2
            self.img2 = self.img3
            self.img3 = self.img4
            self.img4 = self.img5
            self.img5 = self.img6
            self.img6 = self.img7
            self.img7 = img
            self.progressBar.setValue(self.Image_num)
            self.tableView.setModel(self.model)
            self.tableView.setColumnWidth(0, 80)
            self.tableView.setColumnWidth(1, 80)
            self.tableView.setColumnWidth(2, 80)
            self.tableView.setColumnWidth(3, 80)
            layout = QVBoxLayout()
            layout.addWidget(self.tableView)
            self.setLayout(layout)
            self.tableWidget.setColumnCount(2)
            self.tableWidget.setColumnWidth(0, 160)
            self.tableWidget.setColumnWidth(1, 160)
            self.tableWidget.setHorizontalHeaderLabels(['镜头', '冰壶轨迹'])
            layout1 = QVBoxLayout()
            layout1.addWidget(self.tableWidget)
            self.setLayout(layout1)
        else:
            self.MsgTE.clear()
            self.MsgTE.setPlainText('Image obtaining failed.')
    def DispImg(self):
        img = cv2.cvtColor(self.Image, cv2.COLOR_BGR2RGB)
        qimg = qimage2ndarray.array2qimage(img)
        self.DispLb.setPixmap(QPixmap(qimg))
        self.DispLb.show()
    def DispImg1(self):
        img = cv2.cvtColor(self.Image1, cv2.COLOR_BGR2RGB)
        qimg = qimage2ndarray.array2qimage(img)
        self.DispLb.setPixmap(QPixmap(qimg))
        self.DispLb.show()
    def StopCamera(self):
        if self.StopBt.text()=='暂停':
            self.StopBt.setText('继续')
            self.RecordBt.setText('保存')
            self.Timer.stop()
            self.MsgTE.setPlainText("暂停")
            self.pushButton.setEnabled(True)
        elif self.StopBt.text()=='继续':
            self.StopBt.setText('暂停')
            self.RecordBt.setText('录像')
            self.Timer.start(1)
            self.MsgTE.setPlainText('开始')
            self.pushButton.setEnabled(False)
    def RecordCamera(self):
        tag=self.RecordBt.text()
        if tag=='保存':
            try:
                image_name=self.RecordPath+'image'+time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+'.jpg'
                # print(image_name)
                cv2.imwrite(image_name, self.Image)
                self.MsgTE.clear()
                self.MsgTE.setPlainText('Image saved.')
            except Exception as e:
                self.MsgTE.clear()
                self.MsgTE.setPlainText(str(e))
        elif tag=='录像':
            self.RecordBt.setText('停止')

            video_name = self.RecordPath + 'video' + time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + '.avi'
            fps = self.FmRateLCD.value()
            size = (self.Image.shape[1],self.Image.shape[0])
            fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
            self.video_writer = cv2.VideoWriter(video_name, fourcc,self.camera.get(5), size)
            self.RecordFlag=1
            self.MsgTE.setPlainText('Video recording...')
            self.StopBt.setEnabled(False)
            self.ExitBt.setEnabled(False)
        elif tag == '停止':
            self.RecordBt.setText('录像')
            self.video_writer.release()
            self.RecordFlag = 0
            self.MsgTE.setPlainText('Video saved.')
            self.StopBt.setEnabled(True)
            self.ExitBt.setEnabled(True)
    def ExitApp(self):
        self.Timer.Stop()
        self.camera.release()
        self.MsgTE.setPlainText('Exiting the application..')
        QCoreApplication.quit()

    def diffimage(self,src_1, src_2):
        X = np.vstack([src_1, src_2])
        d2 = pdist(X)
        return d2

    def convertImage(self,src):
        color_histgrams2 = [cv2.calcHist([src], [c], None, [16], [0, 256]) \
                            for c in range(3)]
        color_histgrams = np.array([chist / float(sum(chist)) for chist in color_histgrams2])
        hist = color_histgrams.flatten()
        return hist

    def barMinus(self,src_1, src_2):
        src_1 = self.convertImage(src_1)
        src_2 = self.convertImage(src_2)
        return np.sum(self.diffimage(src_1, src_2))

    def crop(self,src):
        box_list = []
        for i in range(int(self.h / self.cols)):
            for j in range(int(self.w / self.rows)):
                box = src[j * self.rows:(j + 1) * self.rows, i * self.cols:(i + 1) * self.cols]
                box_list.append(box)
        return box_list

    def barMinus_crop(self,src_1, src_2):
        b = 0
        for i in range(0, self.a):
            src_11 = self.convertImage(src_1[i])
            src_22 = self.convertImage(src_2[i])
            if np.sum(self.diffimage(src_11, src_22)) <= 0.15:
                b += 1
        return b

    def hierarchy_cluster(self, data, method='average', threshold=35000.0):
        '''层次聚类

        Arguments:
            data [[0, float, ...], [float, 0, ...]] -- 文档 i 和文档 j 的距离

        Keyword Arguments:
            method {str} -- [linkage的方式： single、complete、average、centroid、median、ward] (default: {'average'})
            threshold {float} -- 聚类簇之间的距离
        Return:
            cluster_number int -- 聚类个数
            cluster [[idx1, idx2,..], [idx3]] -- 每一类下的索引
        '''
        data = np.array(data)

        Z = linkage(data, method=method)
        cluster_assignments = fcluster(Z, threshold, criterion='distance')
        # print(type(cluster_assignments))
        num_clusters = cluster_assignments.max()
        indices = self.get_cluster_indices(cluster_assignments)

        return num_clusters, indices

    def get_cluster_indices(self,cluster_assignments):
        '''映射每一类至原数据索引

        Arguments:
            cluster_assignments 层次聚类后的结果

        Returns:
            [[idx1, idx2,..], [idx3]] -- 每一类下的索引
        '''
        n = cluster_assignments.max()
        indices = []
        for cluster_number in range(1, n + 1):
            indices.append(np.where(cluster_assignments == cluster_number)[0])

        return indices

    # def feature_cluster(self,feature_h):
    #     KF = []
    #     points_a = np.array(feature_h).astype(np.float32)
    #     disMat = sch.distance.pdist(points_a, 'euclidean')
    #     th = np.mean(disMat)
    #     if th <= 0.1:
    #         KF.append((len(feature_h)) / 2)
    #         return KF
    #     else:
    #         try:
    #             Z = sch.linkage(disMat, method='average', metric='euclidean')
    #             plt.ylim(0, 1)
    #             cluster = sch.fcluster(Z, t=1.5 * th, criterion='distance')
    #             cluster_one = self.quchong(cluster)  # 标签去重复
    #             # 将原始数据做归一化处理
    #             points_white = whiten(points_a)
    #             # 聚类中心点
    #             centroid = kmeans(points_white, max(cluster))[0]
    #             index = 0
    #             temp = 200
    #             for i in range(len(cluster_one)):
    #                 for k in range(len(cluster)):
    #                     if cluster[k] == cluster_one[i]:
    #                         distance = self.calEuclideanDistance(points_white[k], centroid[i])
    #                         if distance < temp:
    #                             temp = distance
    #                             index = k
    #                 KF.append(index)
    #                 index = 0
    #                 temp = 200
    #         except ValueError:
    #             pass
    #         return KF
    #
    # def quchong(self,list1):
    #     list2 = [];
    #     for i in list1:
    #         if i not in list2:
    #             list2.append(i)
    #     return (list2)

    # def calEuclideanDistance(self,vec1, vec2):
    #     dist = np.sqrt(np.sum(np.square(vec1 - vec2)))
    #     return dist
class Paintarea(QWidget):
    def __init__(self):
        super(Paintarea, self).__init__()

    def getnum(self,n):
        self.fnum = n
    def paintEvent(self,QPaintEvent):
        p = QPainter(self)
        p.begin(self)
        p.setPen(QColor(0,0,255))
        for i in self.fnum:
            points = [QPoint(i, 0), QPoint(i, 31)]
            p.drawPolyline(QPolygon(points))
        p.end()

class Paintarea1(QWidget):
    def __init__(self):
        super(Paintarea1, self).__init__()

    def getnum(self,n):
        self.fnum = n
    def paintEvent(self,QPaintEvent):
        p = QPainter(self)
        p.begin(self)
        p.setPen(QColor(255,0,0))
        for i in self.fnum:
            points = [QPoint(i, 0), QPoint(i, 31)]
            p.drawPolyline(QPolygon(points))
        p.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui=CamShow()
    ui.show()
    sys.exit(app.exec_())
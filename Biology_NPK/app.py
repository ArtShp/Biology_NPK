# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem
from functions import *
from exceptions import *
from config import *
from xlsxwriter import Workbook
from time import sleep


class CalcThread(QtCore.QThread):
    #running = False

    def __init__(self, window, multi_oper=False, parent=None):
        super(CalcThread, self).__init__(parent)
        self.multi_operation = multi_oper

        self.align_func = window.choice_box_1.currentIndex()
        self.mode = window.choice_box_2.currentIndex()
        self.window = window
        self.res = ''
        if not multi_oper:
            self.s1 = window.s1.toPlainText()
            self.s2 = window.s2.toPlainText()
        else:
            self.s1 = window.s.toPlainText()
            self.s2 = ''

    def stop(self):
        self.wait()

    def run(self):
        self.window.status.setText('Статус: В процессе.')
        #self.window.status.repaint()

        if self.align_func == 0:
            self.res = sequence_global_alignment(self.s1, self.s2, self.mode)
        elif self.align_func == 1:
            self.res = sequence_local_alignment(self.s1, self.s2, self.mode)

        self.window.status.setText('Статус: Завершено!')

        data = [self.s1, self.s2, self.res]

        #self.window.clear_table()
        self.window.show_results(data)

        #self.quit()
        #self.stop()



class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.length = 35

        self.horizontalHeaders = [''] * 3

        self.setHeaderData(0, Qt.Horizontal, 'Последовательность 1')
        self.setHeaderData(1, Qt.Horizontal, 'Последовательность 2')
        self.setHeaderData(2, Qt.Horizontal, 'Результат')

        self._full_data = []
        self._data = []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def get_data(self):
        return self._full_data

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return 3

    def addRow(self, data):
        self._full_data.append(data)
        self._data.append([])

        if len(data[0]) <= self.length:
            self._data[-1].append(data[0])
        else:
            self._data[-1].append(data[0][:self.length] + '...')
        if len(data[1]) <= self.length:
            self._data[-1].append(data[1])
        else:
            self._data[-1].append(data[1][:self.length] + '...')
        self._data[-1].append(data[2])

        self.layoutChanged.emit()

    def clear(self):
        self._data = []
        self._full_data = []

    def setHeaderData(self, section, orientation, data, role=Qt.EditRole):
        if orientation == Qt.Horizontal and role in (Qt.DisplayRole, Qt.EditRole):
            try:
                self.horizontalHeaders[section] = data
                return True
            except:
                return False
        return super().setHeaderData(section, orientation, data, role)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            try:
                return self.horizontalHeaders[section]
            except:
                pass
        return super().headerData(section, orientation, role)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        """----------SETUP----------"""

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(723, 673)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")

        self.choice_box_1 = QtWidgets.QComboBox(self.centralwidget)
        self.choice_box_1.setEnabled(True)
        self.choice_box_1.setGeometry(QtCore.QRect(0, 0, 161, 31))
        self.choice_box_1.setObjectName("choice_box_1")
        self.choice_box_1.addItem("")
        self.choice_box_1.addItem("")


        self.align_tab = QtWidgets.QTabWidget(self.centralwidget)
        self.align_tab.setGeometry(QtCore.QRect(0, 30, 711, 141))
        self.align_tab.setObjectName("align_tab")

        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")

        self.count_bt = QtWidgets.QPushButton(self.tab_1)
        self.count_bt.setGeometry(QtCore.QRect(290, 50, 75, 23))
        self.count_bt.setObjectName("count_bt")

        self.s1 = QtWidgets.QPlainTextEdit(self.tab_1)
        self.s1.setGeometry(QtCore.QRect(10, 30, 121, 71))
        self.s1.setObjectName("s1")

        self.s2 = QtWidgets.QPlainTextEdit(self.tab_1)
        self.s2.setGeometry(QtCore.QRect(150, 30, 121, 71))
        self.s2.setObjectName("s2")

        self.s1_sign = QtWidgets.QLabel(self.tab_1)
        self.s1_sign.setGeometry(QtCore.QRect(10, 10, 121, 16))
        self.s1_sign.setObjectName("s1_sign")

        self.s2_sign = QtWidgets.QLabel(self.tab_1)
        self.s2_sign.setGeometry(QtCore.QRect(150, 10, 121, 16))
        self.s2_sign.setObjectName("s2_sign")

        self.status = QtWidgets.QLabel(self.tab_1)
        self.status.setGeometry(QtCore.QRect(380, 50, 141, 21))
        self.status.setObjectName("status")

        self.align_tab.addTab(self.tab_1, "")


        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.s = QtWidgets.QPlainTextEdit(self.tab_2)
        self.s.setGeometry(QtCore.QRect(10, 30, 121, 71))
        self.s.setObjectName("s")

        self.infile_bt = QtWidgets.QPushButton(self.tab_2)
        self.infile_bt.setGeometry(QtCore.QRect(140, 50, 101, 23))
        self.infile_bt.setObjectName("infile_bt")

        self.count_bt_2 = QtWidgets.QPushButton(self.tab_2)
        self.count_bt_2.setGeometry(QtCore.QRect(260, 50, 75, 23))
        self.count_bt_2.setObjectName("count_bt_2")

        self.progress_bar = QtWidgets.QProgressBar(self.tab_2)
        self.progress_bar.setGeometry(QtCore.QRect(500, 50, 118, 23))
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setObjectName("progress_bar")

        self.s_sign = QtWidgets.QLabel(self.tab_2)
        self.s_sign.setGeometry(QtCore.QRect(10, 10, 121, 16))
        self.s_sign.setObjectName("s_sign")

        self.status_2 = QtWidgets.QLabel(self.tab_2)
        self.status_2.setGeometry(QtCore.QRect(350, 50, 141, 21))
        self.status_2.setObjectName("status_2")

        self.align_tab.addTab(self.tab_2, "")


        self.table = QtWidgets.QTableView(self.centralwidget)
        self.table.setEnabled(True)
        self.table.setMinimumSize(700, 50)
        self.table.setMaximumSize(700, 200)
        self.table.setGeometry(QtCore.QRect(0, 170, self.table.minimumWidth(), self.table.minimumHeight()))
        self.table.setObjectName("table")

        self.model = TableModel()

        self.write_file_bt = QtWidgets.QPushButton(self.centralwidget)
        self.write_file_bt.setGeometry(QtCore.QRect(10, 370, 91, 23))
        self.write_file_bt.setObjectName("write_file_bt")

        self.choice_box_2 = QtWidgets.QComboBox(self.centralwidget)
        self.choice_box_2.setGeometry(QtCore.QRect(160, 0, 171, 31))
        self.choice_box_2.setObjectName("choice_box_2")
        self.choice_box_2.addItem("")
        self.choice_box_2.addItem("")

        #self.calc_thread = CalcThread('', '', 0, 0)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.align_tab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        """----------Functions Setup----------"""
        self.add_actions()

    def add_actions(self):
        self.count_bt.clicked.connect(self.count_align)
        self.count_bt_2.clicked.connect(self.test)
        self.write_file_bt.clicked.connect(self.write_file)

    def test(self):
        self.model.addRow(['AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 'BBB', 100])
        self.table.setModel(self.model)

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.adjustSize()

    def count_align(self):
        self.calc_thread = CalcThread(self, False)
        self.calc_thread.start()

    def show_results(self, data):
        self.model.addRow(data)
        self.table.setModel(self.model)

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.adjustSize()

    def clear_table(self):
        self.model.clear()

    def write_file(self):
        f_name = 'C:/Users/Admin/PycharmProjects/Biology_NPK/output/res.xlsx'
        #f_name = QtWidgets.QFileDialog.getSaveFileName(MainWindow, "Open file", "C:/Users/Admin/PycharmProjects/Biology_NPK/output", "Excel File (*.xlsx)")[0]
        if f_name != '':
            data = self.model.get_data()

            wb = Workbook(f_name)
            ws1 = wb.add_worksheet('Shorted')
            #ws2 = wb.add_worksheet('Full')

            title_f = wb.add_format({'font_size': 18, 'align': 'center'})
            subtitle_f = wb.add_format({'font_size': 14, 'align': 'center'})
            #data_f = wb.add_format({'align': 'center'})
            data_f = wb.add_format({})

            ws1.merge_range('A1:N1', 'Результат выравнивания генетических последовательностей (Сокращённо)', title_f)
            #ws2.merge_range('A1:N1', 'Результат выравнивания генетических последовательностей (Полностью)', title_f)

            ws1.merge_range('A2:G2', 0, subtitle_f)
            ws1.merge_range('H2:N2', 0, subtitle_f)

            ws1.merge_range('A3:F3', 'Последовательность 1', subtitle_f)
            ws1.merge_range('G3:L3', 'Последовательность 2', subtitle_f)
            ws1.merge_range('M3:N3', 'Результат', subtitle_f)

            for i in range(len(data)):
                if len(data[i][0]) <= 50:
                    ws1.merge_range(f'A{4+i}:F{4+i}', data[i][0], data_f)
                else:
                    ws1.merge_range(f'A{4+i}:F{4+i}', data[i][0][:50]+'...', data_f)
                if len(data[i][1]) <= 50:
                    ws1.merge_range(f'G{4+i}:L{4+i}', data[i][1], data_f)
                else:
                    ws1.merge_range(f'G{4+i}:L{4+i}', data[i][1][:50] + '...', data_f)
                ws1.merge_range(f'M{4+i}:N{4+i}', data[i][2], data_f)

            wb.close()
        else:
            print('Error')


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.choice_box_1.setItemText(0, _translate("MainWindow", "Глобальное выравнивание"))
        self.choice_box_1.setItemText(1, _translate("MainWindow", "Локальное выравнивание"))
        self.count_bt.setText(_translate("MainWindow", "Посчитать"))
        self.s1_sign.setText(_translate("MainWindow", "<html><head/><body><p>Последовательность 1</p></body></html>"))
        self.s2_sign.setText(_translate("MainWindow", "Последовательность 2"))
        self.status.setText(_translate("MainWindow", "Статус: Работа не начата."))
        self.align_tab.setTabText(self.align_tab.indexOf(self.tab_1), _translate("MainWindow", "1 + 1"))
        self.infile_bt.setText(_translate("MainWindow", "Выбрать файл"))
        self.count_bt_2.setText(_translate("MainWindow", "Посчитать"))
        self.s_sign.setText(_translate("MainWindow", "Последовательность 1"))
        self.status_2.setText(_translate("MainWindow", "Статус: работа не начата"))
        self.align_tab.setTabText(self.align_tab.indexOf(self.tab_2), _translate("MainWindow", "1 + many"))
        self.write_file_bt.setText(_translate("MainWindow", "Запись в файл"))
        self.choice_box_2.setItemText(0, _translate("MainWindow", "По BLOSUM62"))
        self.choice_box_2.setItemText(1, _translate("MainWindow", "По стандартной (Тестовой)"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

# -*- coding: utf-8 -*-
import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from config import NAMES
from exceptions import *
from functions import *
from xlsxwriter import Workbook


class CalcHandler(QtCore.QObject):
    """Calculations thread(object) class"""
    """Signals"""
    change_status = QtCore.pyqtSignal(bool, bool)
    show_data = QtCore.pyqtSignal(list)
    show_used_align = QtCore.pyqtSignal(list)
    configure_progress_bar = QtCore.pyqtSignal(int)
    update_progress_bar = QtCore.pyqtSignal(int)

    data = []
    #align = []

    def start(self):
        if not len(self.data):
            print('Error')
        else:
            is_multi = self.data[0]
            if not is_multi:
                align_func = self.data[1]
                align_mode = self.data[2]
                s1 = self.data[3]
                s2 = self.data[4]

                res = 0

                self.change_status.emit(0, False)
                self.show_used_align.emit([align_func, align_mode])

                if align_func == 0:
                    res = sequence_global_alignment(s1, s2, align_mode)
                elif align_func == 1:
                    res = sequence_local_alignment(s1, s2, align_mode)

                self.show_data.emit([s1, s2, res])

                self.change_status.emit(1, False)
            else:
                align_func = self.data[1]
                align_mode = self.data[2]
                s1 = self.data[3]
                input_file_path = self.data[4]
                file = open(input_file_path, 'r+')

                data = file.readlines()
                data_amount = len(data)

                res = 0

                self.configure_progress_bar.emit(data_amount)
                self.change_status.emit(0, True)
                self.show_used_align.emit([align_func, align_mode])

                for i in range(data_amount):
                    if i+1 != data_amount:
                        s2 = data[i][:-1]
                    else:
                        s2 = data[i]

                    if align_func == 0:
                        res = sequence_global_alignment(s1, s2, align_mode)
                    elif align_func == 1:
                        res = sequence_local_alignment(s1, s2, align_mode)

                    self.update_progress_bar.emit(i+1)
                    self.show_data.emit([s1, s2, res])

                file.close()

                self.change_status.emit(1, True)

    @QtCore.pyqtSlot(list)
    def get_data(self, data):
        self.data = data
        self.start()


class TableModel(QtCore.QAbstractTableModel):
    """Table data model class"""
    def __init__(self, parent=None):
        super().__init__(parent)

        self.length = 35  # Temporary: max length of data

        """Horizontal headers"""
        self.horizontalHeaders = [''] * 3
        for i in range(len(self.horizontalHeaders)):
            self.setHeaderData(i, Qt.Horizontal, NAMES['table_headers'][i])

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
        #return len(self.horizontalHeaders)
        return 3

    def add_row(self, data):
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


class MainWindow(QtWidgets.QMainWindow):
    """Main window class"""
    """Signals"""
    transmit_data = QtCore.pyqtSignal(list)

    """SETUP"""
    def __init__(self):
        super(MainWindow, self).__init__()
        self._ui_setup()
        self._other_setup()
        self._actions_setup()

    def _ui_setup(self):
        """User interface setup"""
        self.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))

        """Main window"""
        self.setWindowTitle(NAMES['WindowTitle'])
        self.resize(723, 400)
        self.move(1280+0, 10)

        """Combo/Choice boxes"""
        self.choice_box_1 = QtWidgets.QComboBox(self)
        self.choice_box_1.setGeometry(0, 0, 161, 31)
        self.choice_box_1.addItem(NAMES['align_name_1'])
        self.choice_box_1.addItem(NAMES['align_name_2'])

        self.choice_box_2 = QtWidgets.QComboBox(self)
        self.choice_box_2.setGeometry(160, 0, 171, 31)
        self.choice_box_2.addItem(NAMES['align_type_1'])
        self.choice_box_2.addItem(NAMES['align_type_2'])

        """Tabs"""
        self.align_tab = QtWidgets.QTabWidget(self)
        self.align_tab.setGeometry(0, 30, 711, 141)

        self.tab_1 = QtWidgets.QWidget()
        self.tab_2 = QtWidgets.QWidget()

        self.align_tab.addTab(self.tab_1, NAMES['tab_name_1'])
        self.align_tab.addTab(self.tab_2, NAMES['tab_name_2'])

        """Tab 1 fill"""
        self.s1 = QtWidgets.QPlainTextEdit(self.tab_1)
        self.s1.setGeometry(10, 30, 121, 71)

        self.s2 = QtWidgets.QPlainTextEdit(self.tab_1)
        self.s2.setGeometry(150, 30, 121, 71)

        self.s1_sign = QtWidgets.QLabel(self.tab_1)
        self.s1_sign.setGeometry(10, 10, 121, 16)
        self.s1_sign.setText(NAMES['s1_sign'])

        self.s2_sign = QtWidgets.QLabel(self.tab_1)
        self.s2_sign.setGeometry(150, 10, 121, 16)
        self.s2_sign.setText(NAMES['s2_sign'])

        self.count_bt = QtWidgets.QPushButton(self.tab_1)
        self.count_bt.setGeometry(290, 50, 75, 23)
        self.count_bt.setText(NAMES['count_bt_sign'])

        self.status = QtWidgets.QLabel(self.tab_1)
        self.status.setGeometry(380, 50, 141, 21)
        self.status.setText(NAMES['status_default_sign'])

        """Tab 2 fill"""
        self.s = QtWidgets.QPlainTextEdit(self.tab_2)
        self.s.setGeometry(10, 30, 121, 71)

        self.s_sign = QtWidgets.QLabel(self.tab_2)
        self.s_sign.setGeometry(10, 10, 121, 16)
        self.s_sign.setText(NAMES['s_sign'])

        self.infile_bt = QtWidgets.QPushButton(self.tab_2)
        self.infile_bt.setGeometry(140, 50, 101, 23)
        self.infile_bt.setText(NAMES['infile_bt_sign'])

        self.count_bt_2 = QtWidgets.QPushButton(self.tab_2)
        self.count_bt_2.setGeometry(260, 50, 75, 23)
        self.count_bt_2.setText(NAMES['count_bt_sign'])

        self.status_2 = QtWidgets.QLabel(self.tab_2)
        self.status_2.setGeometry(350, 50, 141, 21)
        self.status_2.setText(NAMES['status_default_sign'])

        self.progress_bar = QtWidgets.QProgressBar(self.tab_2)
        self.progress_bar.setGeometry(500, 50, 118, 23)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setValue(0)

        """Table"""
        self.table = QtWidgets.QTableView(self)
        self.table.setMinimumSize(700, 50)
        self.table.setMaximumSize(700, 200)
        self.table.setGeometry(0, 170, self.table.minimumWidth(), self.table.minimumHeight())

        """Write file"""
        self.write_file_bt = QtWidgets.QPushButton(self)
        self.write_file_bt.setGeometry(10, 370, 91, 23)
        self.write_file_bt.setText(NAMES['write_file_bt_sign'])

        """Labels with used align mode and type(in table)"""
        self.used_align_1 = QtWidgets.QLabel(self)
        self.used_align_1.setGeometry(150, 370, 161, 21)
        self.used_align_1.setText(NAMES['used_align_default_sign'])

        self.used_align_2 = QtWidgets.QLabel(self)
        self.used_align_2.setGeometry(320, 370, 171, 21)
        self.used_align_2.setText(NAMES['used_align_default_sign'])

    def _other_setup(self):
        """Other objects setup"""
        self.is_running = False  # Is running any calculations
        self.input_file = ''  # Path to input data file

        self.model = TableModel()  # Data model for table

        """Creating thread for calculating operations"""
        self.worker = CalcHandler()
        self.thread = QtCore.QThread(self)
        self.worker.moveToThread(self.thread)

    def _actions_setup(self):
        """Actions setup"""
        """Connecting button clicks to functions"""
        self.count_bt.clicked.connect(lambda: self.count_align(0))
        self.count_bt_2.clicked.connect(lambda: self.count_align(1))
        self.infile_bt.clicked.connect(self.choose_input_file)
        self.write_file_bt.clicked.connect(self.write_file)

        """Connecting signals to functions"""
        self.transmit_data.connect(self.worker.get_data)

        """Connecting slots to functions"""
        self.worker.change_status.connect(self.change_status)
        self.worker.show_data.connect(self.show_results)
        self.worker.show_used_align.connect(self.show_used_align)
        self.worker.configure_progress_bar.connect(self.configure_progress_bar)
        self.worker.update_progress_bar.connect(self.update_progress_bar)

    """SIMPLE FUNCTIONS"""
    def count_align(self, is_multi):
        if not self.is_running:
            if not is_multi:
                if self.s1.toPlainText() and self.s2.toPlainText():
                    self.is_running = True
                    self.clear_table()
                    self.thread.start()
                    self.transmit_data.emit([0, self.choice_box_1.currentIndex(), self.choice_box_2.currentIndex(), self.s1.toPlainText(), self.s2.toPlainText()])
                else:
                    print('Not all fields filled!')
            else:
                if self.input_file:
                    if self.s.toPlainText():
                        self.is_running = True
                        self.clear_table()
                        self.thread.start()
                        self.transmit_data.emit([1, self.choice_box_1.currentIndex(), self.choice_box_2.currentIndex(), self.s.toPlainText(), self.input_file])
                    else:
                        print('Not all fields filled!')
                else:
                    print('No file chosen!')
        else:
            print('Process is running now!')

    def clear_table(self):
        self.model.clear()
        self.table.setModel(self.model)
        self.table.repaint()

    def choose_input_file(self):
        self.input_file = QtWidgets.QFileDialog.getOpenFileName(self, "Open file", "C:/Users/user/Desktop/Biology_NPK/input", "Text file (*.txt)")[0]
        #self.input_file = QtWidgets.QFileDialog.getOpenFileName(self, "Open file", "C:/Users/Admin/PycharmProjects/Biology_NPK/input", "Text file (*.txt)")[0]

    def write_file(self):
        if not self.is_running:
            if self.model.get_data():
                f_name = 'C:/Users/user/Desktop/Biology_NPK/output/res.xlsx'
                #f_name = 'C:/Users/Admin/PycharmProjects/Biology_NPK/output/res.xlsx'
                #f_name = QtWidgets.QFileDialog.getSaveFileName(self, "Open file", "C:/Users/Admin/PycharmProjects/Biology_NPK/output", "Excel File (*.xlsx)")[0]
                if f_name != '':
                    self.is_running = True
                    data = self.model.get_data()

                    wb = Workbook(f_name)
                    ws1 = wb.add_worksheet('Shorted')
                    #ws2 = wb.add_worksheet('Full')

                    title_f = wb.add_format({'font_size': 18, 'align': 'center'})
                    subtitle_f = wb.add_format({'font_size': 14, 'align': 'center'})
                    #data_f = wb.add_format({'align': 'center'})
                    data_f = wb.add_format({})

                    ws1.set_column_pixels('N:N', 85)

                    ws1.merge_range('A1:N1', 'Результат выравнивания генетических последовательностей (Сокращённо)', title_f)
                    #ws2.merge_range('A1:N1', 'Результат выравнивания генетических последовательностей (Полностью)', title_f)

                    ws1.merge_range('A2:G2', self.used_align_1.text(), subtitle_f)
                    ws1.merge_range('H2:N2', self.used_align_2.text(), subtitle_f)

                    ws1.write('A3', 'ID', subtitle_f)
                    ws1.merge_range('B3:G3', 'Последовательность 1', subtitle_f)
                    ws1.merge_range('H3:M3', 'Последовательность 2', subtitle_f)
                    ws1.write('N3', 'Результат', subtitle_f)

                    for i in range(len(data)):
                        ws1.write(f'A{4+i}', i+1, data_f)
                        if len(data[i][0]) <= 50:
                            ws1.merge_range(f'B{4+i}:G{4+i}', data[i][0], data_f)
                        else:
                            ws1.merge_range(f'B{4+i}:G{4+i}', data[i][0][:50]+'...', data_f)
                        if len(data[i][1]) <= 50:
                            ws1.merge_range(f'H{4+i}:M{4+i}', data[i][1], data_f)
                        else:
                            ws1.merge_range(f'H{4+i}:M{4+i}', data[i][1][:50]+'...', data_f)
                        ws1.write(f'N{4+i}', data[i][2], data_f)

                    wb.close()
                    print('File written successfully')
                    self.is_running = False
                else:
                    print('Error')
            else:
                print('No data to write!')
        else:
            print('Process is running!')

    """SLOTS"""
    @QtCore.pyqtSlot(bool, bool)
    def change_status(self, text, is_multi):
        if not is_multi:
            if not text:
                # self.clear_table()
                self.status.setText('Статус: В процессе.')
            else:
                self.status.setText('Статус: Завершено!')
                self.thread.quit()
                self.is_running = False
        else:
            if not text:
                # self.clear_table()
                self.status_2.setText('Статус: В процессе.')
            else:
                self.status_2.setText('Статус: Завершено!')
                self.thread.quit()
                self.is_running = False

    @QtCore.pyqtSlot(list)
    def show_results(self, data):
        self.model.add_row(data)
        self.table.setModel(self.model)

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.adjustSize()

    @QtCore.pyqtSlot(list)
    def show_used_align(self, align):
        self.used_align_1.setText(self.choice_box_1.itemText(align[0]))
        self.used_align_2.setText(self.choice_box_2.itemText(align[1]))

    @QtCore.pyqtSlot(int)
    def configure_progress_bar(self, maximum):
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(maximum)

    @QtCore.pyqtSlot(int)
    def update_progress_bar(self, val):
        self.progress_bar.setValue(val)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

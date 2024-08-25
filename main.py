from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QMainWindow,QApplication, QFileDialog, QWidget, QGridLayout, 
							 QHBoxLayout, QLabel, QComboBox, QPushButton, QSpacerItem,
							 QSizePolicy, QVBoxLayout, QMessageBox, QTableView)

from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant, QModelIndex

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as Navi
from matplotlib.figure import Figure
import seaborn as sns
import pandas as pd
import sip 
import sys
import os
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


import platform



class MatplotlibCanvas(FigureCanvasQTAgg):
	def __init__(self,parent=None, dpi = 120):
		fig = Figure(dpi = dpi)
		self.axes = fig.add_subplot(111)
		super(MatplotlibCanvas,self).__init__(fig)
		fig.tight_layout()


class PandasModel(QAbstractTableModel):
	def __init__(self, df=pd.DataFrame(), parent=None):
		super().__init__(parent)
		self._df = df

	def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
		if role != Qt.ItemDataRole.DisplayRole:
			return QVariant()
		if orientation == Qt.Orientation.Horizontal:
			try:
				return self._df.columns.tolist()[section]
			except IndexError:
				return QVariant()
		elif orientation == Qt.Orientation.Vertical:
			try:
				return self._df.index.tolist()[section]
			except IndexError:
				return QVariant()

	def rowCount(self, parent=QModelIndex()):
		return self._df.shape[0]

	def columnCount(self, parent=QModelIndex()):
		return self._df.shape[1]

	def data(self, index, role=Qt.ItemDataRole.DisplayRole):
		if role != Qt.ItemDataRole.DisplayRole:
			return QVariant()
		if not index.isValid():
			return QVariant()
		return QVariant(str(self._df.iloc[index.row(), index.column()]))
		
		

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		
		self.setObjectName("MainWindow")
		self.resize(1440, 1000)
		
        #1--
		self.centralwidget = QWidget(self)
		self.centralwidget.setObjectName("centralwidget")
		
        #2--
		self.gridLayout = QGridLayout(self.centralwidget)
		self.gridLayout.setObjectName("gridLayout")
		
        #3-- 1st layer - label, file selection, plot type, clear button
		self.v1 = QVBoxLayout()
		self.v1.setObjectName("horizontalLayout")
		
		self.label = QLabel(self.centralwidget)
		self.label.setObjectName("label")
		self.v1.addWidget(self.label)
		
		self.comboBox = QComboBox(self.centralwidget)
		self.comboBox.setObjectName("comboBox")
		self.v1.addWidget(self.comboBox)
		
		self.pushButton = QPushButton(self.centralwidget)
		self.pushButton.setObjectName("pushButton")
		self.v1.addWidget(self.pushButton)

		self.clearButton = QPushButton(self.centralwidget)
		self.clearButton.setObjectName("clearButton")
		self.v1.addWidget(self.clearButton)

		self.label2 = QLabel(self.centralwidget)
		self.label2.setObjectName("label2")
		self.v1.addWidget(self.label2)

		
		self.gridLayout.addLayout(self.v1, 0, 0, 1, 1)

		# self.gridLayout.addLayout(spacerItem)

		self.v2 = QVBoxLayout()
		self.v2.setObjectName("verticalLayout2")
		
        #adding spacer below file select and above the plot
		self.spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
		self.v2.addItem(self.spacerItem1)
		self.gridLayout.addLayout(self.v2, 1, 1, 1, 1)


		self.v3 = QVBoxLayout()
		self.v3.setObjectName("verticalLayout3")
		self.table = QTableView()
		self.table.setSortingEnabled(True)
		self.table.horizontalHeader().setSectionsMovable(True)
		self.v3.addWidget(self.table)

		# self.spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
		# self.v3.addItem(self.spacerItem1)
		self.gridLayout.addLayout(self.v3, 1, 0, 1, 1)


		#setting ui
		self.setCentralWidget(self.centralwidget)

		self.retranslateUi()
		QtCore.QMetaObject.connectSlotsByName(self)
		
		self.filename = ''
		self.canv = MatplotlibCanvas(self)
		self.df = []
		
		self.toolbar = Navi(self.canv,self.centralwidget)
		self.v2.addWidget(self.toolbar)
		
		self.plots = ['line', 'bar', 'barh','hist','box','area']
		 
		self.comboBox.addItems(self.plots)
		
		self.pushButton.clicked.connect(self.getFile)
		self.clearButton.clicked.connect(self.Clear)
		self.comboBox.currentIndexChanged['QString'].connect(self.Update)

		
	def Update(self,value):
		print("Value from Combo Box:",value)
		plt.clf()

		try:
			self.v2.removeWidget(self.toolbar)
			self.v2.removeWidget(self.canv)
			self.v3.removeWidget(self.table)
			

			
			sip.delete(self.toolbar)
			sip.delete(self.canv)
			sip.delete(self.table)
			
			self.toolbar = None
			self.canv = None
			self.table = None
			self.v2.removeItem(self.spacerItem1)


		except Exception as e:
			print(e)
			self.error1("Error encountered!",e)
			pass
			# self.Clear()
		self.canv = MatplotlibCanvas(self)
		self.toolbar = Navi(self.canv,self.centralwidget)

		self.table = QTableView()
		self.table.setSortingEnabled(True)
		self.table.horizontalHeader().setSectionsMovable(True)
		

		self.model = PandasModel(self.df)
		self.table.setModel(self.model)
		
		self.v2.addWidget(self.toolbar)
		self.v2.addWidget(self.canv)
		self.v3.addWidget(self.table)
		
		self.canv.axes.cla()
		ax = self.canv.axes
		self.df.plot(ax = self.canv.axes, kind=value)
		legend = ax.legend()
		legend.set_draggable(True)

		# print(ax.legend()[0],ax.legend()[1])
		
		ax.set_xlabel('X axis')
		ax.set_ylabel('Y axis')
		ax.set_title(self.Title)
		
		self.canv.draw()

	def Clear(self):
		
		self.label2.setText(self._translate("MainWindow", "Selected File: None"))
		plt.clf()

		try:
			self.v2.removeWidget(self.toolbar)
			self.v2.removeWidget(self.canv)
			self.v3.removeWidget(self.table)
			

			
			sip.delete(self.toolbar)
			sip.delete(self.canv)
			sip.delete(self.table)
			
			self.toolbar = None
			self.canv = None
			self.table = None
			self.v2.removeItem(self.spacerItem1)


		except Exception as e:
			print(e)
			self.error1("Error encountered!",e)
			pass
			# self.Clear()
		self.canv = MatplotlibCanvas(self)
		self.toolbar = Navi(self.canv,self.centralwidget)

		self.table = QTableView()
		self.table.setSortingEnabled(True)
		self.table.horizontalHeader().setSectionsMovable(True)
		

		self.model = PandasModel(pd.DataFrame())
		self.table.setModel(self.model)
		
		self.v2.addWidget(self.toolbar)
		self.v2.addWidget(self.canv)
		self.v3.addWidget(self.table)

		

	def error1(self,title, message, moreinfo=''):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Critical)
		msg.setText(message)
		if moreinfo!='':
			msg.setInformativeText('More information: '+moreinfo)
		msg.setWindowTitle(title)
		msg.exec_()

	def getFile(self):

		self.filename = QFileDialog.getOpenFileName(filter = "csv (*.csv)")[0]
		print("File :", self.filename)
		self.readData()
	
	def readData(self):

		try:
			base_name = os.path.basename(self.filename)
			self.Title = os.path.splitext(base_name)[0]
			print('FILE',self.Title )
			self.df = pd.read_csv(self.filename,encoding = 'utf-8').fillna(0)
			self.label2.setText(self._translate("MainWindow", "Selected File: "+self.filename))
			print(self.filename+" gives error")
			self.model = PandasModel(self.df)
			self.table.setModel(self.model)

			self.Update(self.plots[0]) # 0th plot is default
		except Exception as e:
			print(e)
			self.error1("Error encountered!","Must choose a file!",str(e))
			
			# self.Clear()

	def retranslateUi(self):
		self._translate = QtCore.QCoreApplication.translate
		self.setWindowTitle(self._translate("MainWindow", "Plot Visualizer"))
		self.setWindowIcon(QIcon('./icon/plot.png'))
		self.label.setText(self._translate("MainWindow", "Select Plot Type:"))
		self.pushButton.setText(self._translate("MainWindow", "Select File"))
		self.clearButton.setText(self._translate("MainWindow", "Clear"))
		self.label2.setText(self._translate("MainWindow", "Selected File: None"))

if __name__ == "__main__":
	
	app = QApplication(sys.argv)
	ui = MainWindow()
	ui.show()
	sys.exit(app.exec_())



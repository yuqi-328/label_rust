# -*- encoding: utf-8 -*-
from qtpy import QtCore
from qtpy.QtCore import Qt
from qtpy import QtWidgets

from .escapable_qlist_widget import EscapableQListWidget


#class UniqueLabelQListWidget(EscapableQListWidget):
class UniqueLabelQListWidget(QtWidgets.QListWidget):

#class UniqueLabelQListWidget(QtWidgets.QListView):

    def mousePressEvent(self, event):
        super(UniqueLabelQListWidget, self).mousePressEvent(event)
        if not self.indexAt(event.pos()).isValid():
            self.clearSelection()

    def findItemsByLabel(self, label):
        items = []
        for row in range(self.count()):
            item = self.item(row)
            if item.data(Qt.UserRole) == label:
                items.append(item)
        return items

    def createItemFromLabel(self, label):
        item = QtWidgets.QListWidgetItem()
        item.setData(Qt.UserRole, label)
        return item

    def setItemLabel(self, item, label, color=None):
        qlabel = QtWidgets.QLabel()  # 用于显示文本或图像，不提供用户交互功能
        if color is None:
            qlabel.setText("{}".format(label))
        else:
            qlabel.setText(
                '{} <font color="#{:02x}{:02x}{:02x}">●</font>'.format(
                    label, *color
                )
            )
        qlabel.setAlignment(Qt.AlignBottom)  # 消除布局中的空隙

        item.setSizeHint(qlabel.sizeHint())

        self.setItemWidget(item,qlabel)
"""

class UniqueLabelQListWidget(QtWidgets.QListView):
    def createItemFromLabel(self, label):
        item = QtWidgets.QListWidgetItem()
        item.setData(Qt.UserRole, label)
        return item
"""


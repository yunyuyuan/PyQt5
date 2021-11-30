from PyQt5.Qt import *

from frames.util import ResizeLabel
from frames.Editor import MdEdit, HtmlEdit, MdShow


class Work(QFrame):
    def __init__(self, top):
        super(Work, self).__init__(top)
        self.top = top
        self.setObjectName("work")

        self.ipt = MdEdit(self)
        self.label_1 = ResizeLabel(self, 0, 2)
        self.html = HtmlEdit(self, self.label_1)
        self.label_2 = ResizeLabel(self, 2, 4)
        self.md = MdShow(self, self.label_2)

        self.all_text = [self.ipt, 0, self.html, 0, self.md]

    def init(self):
        layout = QGridLayout(self)
        layout.setSpacing(0)
        layout.addWidget(self.ipt, 0, 0)
        layout.addWidget(self.label_1, 0, 1)
        layout.addWidget(self.html, 0, 2)
        layout.addWidget(self.label_2, 0, 3)
        layout.addWidget(self.md, 0, 4)
        self.setLayout(layout)
        self.md.setVisible(False)

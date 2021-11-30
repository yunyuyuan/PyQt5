from re import sub

from PyQt5.Qt import *
from markdown import markdown

from frames import all_ext


class WorkEdit(QTextEdit):
    def __init__(self, work):
        super().__init__(work)
        self.work = work
        self.top = work.top
        self.setMinimumWidth(50)

class MdEdit(WorkEdit):
    def __init__(self, work):
        super(MdEdit, self).__init__(work)
        self.setPlainText('input something')
        self.ext_list = ['attr_list', 'tables', 'fenced_code', 'sane_lists', 'toc']
        self.ext_list.extend(all_ext)
        self.textChanged.connect(self.do_parse)

    def do_parse(self):
        content = self.toPlainText()
        content = markdown(content, extensions=self.ext_list)
        old_value = self.work.html.verticalScrollBar().value()
        self.work.html.setPlainText(content)
        self.work.html.verticalScrollBar().setValue(old_value)

    def setVisible(self, b):
        if not b:
            self.work.layout().setColumnStretch(0, 0)
        super().setVisible(b)

class HtmlEdit(WorkEdit):
    def __init__(self, work, rel_label):
        super(HtmlEdit, self).__init__(work)
        self.rel_label = rel_label
        self.textChanged.connect(self.do_parse)

    def setVisible(self, b):
        if not b:
            self.work.layout().setColumnStretch(2, 0)
        super().setVisible(b)
        self.rel_label.setVisible(b)

    def do_parse(self):
        old_value = self.work.md.verticalScrollBar().value()
        self.work.md.setText("<style>%s</style>" % self.top.css + sub(r'([\d.]*)rem', lambda m: str(int(float(m.group(1))*self.top.conf['font-size']))+'px', self.toPlainText()))
        self.work.md.verticalScrollBar().setValue(old_value)

class MdShow(WorkEdit):
    def __init__(self, work, rel_label):
        super().__init__(work)
        self.setReadOnly(True)
        self.rel_label = rel_label
        self.setStyleSheet("QTextEdit{background: transparent}")

    def setVisible(self, b):
        if not b:
            self.work.layout().setColumnStretch(4, 0)
        super().setVisible(b)
        self.rel_label.setVisible(b)

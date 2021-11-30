from PyQt5.Qt import *
from re import sub


class Head(QFrame):
    def __init__(self, top):
        super(Head, self).__init__(top)
        self.top = top
        self.setObjectName("head")

        self.md_list = []
        self.btn_list = [[0xe8f5, "h"],
                         [0xe60b, "b"],
                         [0xe60c, "i"],
                         [0xe929, "del_"],
                         [0xe790, "link"],
                         [0xebc5, "img"],
                         [0xe858, "code"],
                         [0xe600, "ul"],
                         [0xe60d, "ol"],
                         [0xe683, "table"]]
        self.work_ipt = None

    def init(self):
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignLeft)
        for i in self.btn_list:
            btn = QPushButton(chr(i[0]), self)
            info = self.top.conf["md"][i[1]]
            btn.setToolTip(info["tip"])
            btn.content = info["content"]
            btn.type = info["type"]
            btn.setProperty("what", i[1])
            btn.setProperty("class", "md-btn")
            btn.setCursor(Qt.PointingHandCursor)

            self.md_list.append(btn)
            layout.addWidget(btn)
        layout.addStretch(100)
        frm = QFrame(self)
        frm.setObjectName('switch')
        f_layout = QGridLayout(self)
        f_layout.setSpacing(0)
        f_layout.setContentsMargins(0, 0, 0, 0)
        idx = 0
        for b in ['md', 'html', '预览']:
            btn = QPushButton(b, frm)
            f_layout.addWidget(btn, 0, idx)
            idx += 1
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(self.switch_frame)
            if b == '预览':
                btn.setProperty('class', 'deactive')
                btn.setObjectName('swt_pre')
            else:
                btn.setProperty('class', 'active')
                btn.setObjectName('swt_' + b)
        frm.setLayout(f_layout)
        layout.addWidget(frm)

        self.setLayout(layout)
        # 绑定事件
        for btn in self.md_list:
            if btn.type == "add":
                btn.clicked.connect(self.ipt_add)
            elif btn.type == "decorate":
                btn.clicked.connect(self.ipt_decorate)

        self.work_ipt = self.top.frame_work.ipt

    def ipt_add(self):
        content = self.sender().content
        self.work_ipt.insertPlainText(content)

    def ipt_decorate(self):
        content = self.sender().content
        text = self.work_ipt.toPlainText()
        start = min(self.work_ipt.textCursor().position(), self.work_ipt.textCursor().anchor())
        end = max(self.work_ipt.textCursor().position(), self.work_ipt.textCursor().anchor())
        if start == end:
            return
        middle = text[start:end]
        text = text[0:start] + sub(r"([^\\])%", "\\1" + middle, content) + text[end:]
        self.work_ipt.setText(text)

    def switch_frame(self):
        el = self.sender()
        if el.text() == 'html':
            e = self.top.frame_work.html
        elif el.text() == 'md':
            e = self.top.frame_work.ipt
        else:
            e = self.top.frame_work.md
        e.setVisible((True if el.property('class') != 'active' else False))
        el.setProperty('class', 'active' if el.property('class') != 'active' else 'deactive')
        self.top.setStyleSheet(self.top.styleSheet())

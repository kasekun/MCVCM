import matplotlib
import tkinter

matplotlib.use("TkAgg")

import matplotlib
if matplotlib.get_backend() != 'TkAgg':
    raise Exception('current matplotlib backend <\'%s\'> might result in a crash when used with <tkinter>, please use <\'TkAgg\'> backend' %matplotlib.get_backend())


class _ConstrainedEntry(tkinter.Entry):
    def __init__(self, charlimit=12, *args, **kwargs):
        tkinter.Entry.__init__(self, *args, **kwargs)

        vcmd = (self.register(self.on_validate),"%P")
        self.configure(validate="all", validatecommand=vcmd)
        self.charlimit = charlimit

    def disallow(self):
        self.bell()

    def on_validate(self, new_value):
        try:
            # print(new_value) # for testing
            if len(new_value) <= self.charlimit: return True
            if len(new_value) > self.charlimit:
                self.disallow()
                return False
        except ValueError:
            self.disallow()
            return False


class tkComment(object):

    def __init__(self):
        root = self.root = tkinter.Toplevel()
        self.comment = ''
        root.geometry("500x50+600+600")
        tkinter.Button(root,text="save comment",command=lambda: self._assign(entryVar)).pack(anchor=tkinter.S,side=tkinter.BOTTOM)
        root.title('comment for this source:')

        root.bind('<Escape>', lambda e: self._assign(entryVar))
        root.bind('<Return>', lambda e: self._assign(entryVar))

        entryVar = self.entryVar = tkinter.StringVar()
        entry = self.entry = _ConstrainedEntry(charlimit = 53, master=root, width=60, textvariable=self.entryVar)
        entry.pack(side=tkinter.TOP)

        root.attributes("-topmost", True)
        root.attributes("-topmost", False)

    def _assign(self,var):
        self.comment=var.get()
        # print(self.comment) # for testing
        self.root.destroy()


if __name__ == '__main__':
    tkC = tkComment()
    tkC.root.mainloop()

    print(tkC.comment)
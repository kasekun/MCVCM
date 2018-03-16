from __future__ import print_function

import time
import shutil


def print_center(*args):
    '''
        Determine size of terminal and center printed text
        e.g.,
            print_center('='*18,'damn term,','you lookin good','='*18)
    '''
    import subprocess
    trows, tcolumns = list(map(int,subprocess.check_output(['stty', 'size']).decode().split()))
    for arg in args:
        print(arg.center(tcolumns))


# goo.gl/8jAuN5c
def make_folder(path):
    ''' Makes folder if it doesn't exist '''
    import os, errno
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    return os.path.abspath(path)


def file_accessible(filepath, mode='r'):
    '''
        Check if a file exists and is accessible (read by default)
    '''
    try:
        f = open(filepath, mode)
        f.close()
    except IOError as e:
        return False
    return True


def version_control(filename):
    '''
        Primative version control:

        Checks for instance of a file,
        Creates numbered copy of that file,
        Numbers file appropriately if numbered file already exists
    '''
    try:
        import shutil
    except Exception as e:
        print('Import failed: ', e)

    path, format = filename.split('.')
    bkup_int = 1
    bkup_path = path + '-bkp-%s' % ('{:02d}'.format(bkup_int))

    print('Found a preexisting file: %s' % (filename))

    while file_accessible(bkup_path + '.%s' % (format)):
        print('also found %s' % (bkup_path + '.%s' % (format)))
        bkup_int += 1
        bkup_path = path + '-bkp-%s' % ('{:02d}'.format(bkup_int))

    print('Backing up file to: %s' % (bkup_path + '.%s' % (format)))
    shutil.copy2(filename, bkup_path + '.%s' % (format))


class Crosshair(object):

    '''
        draws a crosshair at the desired location on your axis
        Crossair is scaled to plotted axis size
        **kwargs are arguments of ax.hline and ax.vline

        could probably write a better help section than this,
        but the functions are pretty self-explanatory
    '''

    def __init__(self,xloc,yloc,axis, size = 0.1, gap = 0.025, **kwargs):
        self.xloc = xloc
        self.yloc = yloc
        self.axis = axis
        self.size = size
        self.gap = gap
        self.hline = None
        self.vline = None

        if size > 1 or size < 0:
            print('please specify cursor size from 0 to 1 (0 to 100% of plot dimensions)')
            return
        if gap > 1 or gap < 0:
            print('please specify cursor gap from 0 to 1 (0 to 100% of plot dimensions)')
            return
        if gap > size or gap == size:
            print('ensure that the cursor gap is smaller than the cursor size')
            return
        self.draw(**kwargs)

    def draw(self,**kwargs):
        y0, y1 = self.axis.get_ybound()
        x0, x1 = self.axis.get_xbound()

        dx = x1 - x0
        dy = y1 - y0
        self.hline = self.axis.hlines([self.yloc,self.yloc],
                                      [self.xloc - self.size * dx, self.xloc + self.size * dx],
                                      [self.xloc - self.gap * dx, self.xloc + self.gap * dx], **kwargs)
        self.vline = self.axis.vlines([self.xloc,self.xloc],
                                      [self.yloc - self.size * dy, self.yloc + self.size * dy],
                                      [self.yloc - self.gap * dy, self.yloc + self.gap * dy], **kwargs)

    def remove(self):
        if self.hline is None or self.vline is None:
            print('Nothing to remove')
            return
        else:
            self.hline.remove()
            self.hline = None
            self.vline.remove()
            self.vline = None

    def redraw(self):
        self.remove()
        self.draw()

    def toggle_visible(self):
        self.hline.set_visible(not self.hline.get_visible())
        self.vline.set_visible(not self.vline.get_visible())



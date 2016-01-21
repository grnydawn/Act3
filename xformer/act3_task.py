# act3_task.py

import os
import sys
from act3_common import runcmd

class A3Task(object):
    def perform_sync(self):
        if not hasattr(self, 'retval'): self.retval = { 'error': True }
        return self._perform()

    def perform_async(self):
        if not hasattr(self, 'retval'): self.retval = { 'error': True }
        # create thread
        return self._perform()

    def _perform(self):
        raise Exception('Subclass should implement _perform function')

    def pack_error(self, msg):
        self.retval['error'] = True
        self.retval['msg'] = msg


class TaskFileCheckFortran(A3Task):
    def __init__(self, filepath):
        self.filepath = str(filepath)
        self.abspath = os.path.abspath(self.filepath)
        self.dirname, self.basename = os.path.split(self.abspath)

    def _perform(self):
        self.retval['error'] = True
        self.retval['filetype'] = 'Unknown'
        try:
            for form, std, extra in [('fixed', 'legacy', ''), ('free', 'f95', ''), \
                    ('free', 'f2003', ''), ('free', 'f2008', '-fcoarray=single')]:
                tmpfile = '%s/.__tmpfile'%self.dirname 
                stdout, stderr = runcmd('gfortran -c -std=%s -f%s-form -o %s %s %s'%\
                    (std, form, tmpfile, extra, self.abspath))
                #print '%s STDOUT: '%std, stdout
                #print '%s STDERR: '%std, stderr
                if os.path.exists(tmpfile): os.remove(tmpfile)
                if stderr: continue
                self.retval['error'] = False
                self.retval['filetype'] = 'Fortran Source Code: %s standard'%std
                break
        except: pass
 
        return self.retval

class TaskFileCheckMakefile(A3Task):
    def __init__(self, filepath):
        self.filepath = str(filepath)
        self.abspath = os.path.abspath(self.filepath)
        self.dirname, self.basename = os.path.split(self.abspath)

    def _perform(self):
        self.retval['error'] = True
        self.retval['filetype'] = 'Unknown'
        stdout, stderr = runcmd('make --just-print -f %s'% self.abspath)
        #print 'make STDOUT: ', stdout
        #print 'make STDERR: ', stderr
        if stderr:
            return self.retval
        else:
            self.retval['error'] = False
            self.retval['filetype'] = 'GNU Makefile'
            return self.retval

class TaskFileCheckExt(A3Task):
    checkmap= {
        ('.f', '.f90', '.f95', '.f03', '.f08', '.F', '.F90', '.F95', '.F03', '.F08'): TaskFileCheckFortran
    }

    def __init__(self, filepath):
        self.filepath = str(filepath)
        self.abspath = os.path.abspath(self.filepath)
        self.dirname, self.basename = os.path.split(self.abspath)
        if self.basename:
            self.fileroot, self.fileext = os.path.splitext(self.basename)
        else:
            self.fileroot, self.fileext = ('', '')

    def has_ext(self, ext):
        for exts in self.checkmap:
            if ext in exts: return True
        return False

    def get_checker(self, ext):
        for exts, checker in self.checkmap.items():
            if ext in exts: return checker
        return None

    def _perform(self):
        if not os.path.exists(self.abspath):
            self.pack_error('%s does not exist.'%self.basename)
            return self.retval

        if self.has_ext(self.fileext):
            task1 = self.get_checker(self.fileext)(self.abspath)
            task1_retval = task1.perform_sync()

            if not task1_retval['error']:
                self.retval['error'] = False
                self.retval['filetype'] = task1_retval['filetype']
        else:
            self.retval['error'] = True
            self.pack_error('%s extension is not supported.'%self.fileext)

        return self.retval

class TaskFileCheckName(A3Task):
    checkmap= {
        ('Makefile', 'makefile'): TaskFileCheckMakefile
    }

    def __init__(self, filepath):
        self.filepath = str(filepath)
        self.abspath = os.path.abspath(self.filepath)
        self.dirname, self.basename = os.path.split(self.abspath)

    def has_filename(self, filename):
        for filenames in self.checkmap:
            if filename in filenames: return True
        return False

    def get_checker(self, filename):
        for filenames, checker in self.checkmap.items():
            if filename in filenames: return checker
        return None

    def _perform(self):
        if not os.path.exists(self.abspath):
            self.pack_error('%s does not exist.'%self.basename)
            return self.retval

        if self.has_filename(self.basename):
            task = self.get_checker(self.basename)(self.abspath)
            task_retval = task.perform_sync()

            if not task_retval['error']:
                self.retval['error'] = False
                self.retval['filetype'] = task_retval['filetype']
        else:
            self.retval['error'] = True
            self.pack_error('%s is not supported.'%self.basename)

        return self.retval

class TaskFileCheck(A3Task):
    def __init__(self, filepath):
        self.filepath = str(filepath)
        self.abspath = os.path.abspath(self.filepath)
        self.dirname, self.basename = os.path.split(self.abspath)

    def _perform(self):

        if not os.path.exists(self.abspath):
            self.pack_error('%s does not exist.'%self.basename)
            return self.retval

        # check based on extension
        task = TaskFileCheckExt(self.abspath)
        task_retval = task.perform_sync()

        if not task_retval['error']:
            self.retval['error'] = False
            self.retval['filetype'] = task_retval['filetype']
            return self.retval

        # check based on filename
        task = TaskFileCheckName(self.abspath)
        task_retval = task.perform_sync()

        if not task_retval['error']:
            self.retval['error'] = False
            self.retval['filetype'] = task_retval['filetype']
            return self.retval


        return self.retval


#include <Python.h>
#include <fcntl.h>
#include <stdio.h>
#include <asm-generic/unistd.h>
#include <sys/mount.h>

static PyObject *
chfscontext(PyObject *self, PyObject *args)
{
    const char *filepath;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &filepath))
        return NULL;

    int fd = open(filepath, O_RDONLY);
    if (fd < 0) {
	    //printf("Could not open ns file\n");
        sts = -1;
        goto out;
    }
    
    if (setns(fd, 666)) {
        sts = -1;
    }
    close(fd);

out:
    return Py_BuildValue("i", sts);
}

static PyObject *
proc_mount(PyObject *self, PyObject *args)
{
    int sts; 
    sts = mount("none","/proc","proc",0,NULL);

    return Py_BuildValue("i", sts);
}

static PyObject *
proc_umount(PyObject *self, PyObject *args)
{
    int sts; 
    sts = umount("/proc");

    return Py_BuildValue("i", sts);

}

static PyObject *
chcontext(PyObject *self, PyObject *args)
{
    const char *filepath;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &filepath))
        return NULL;

    int fd = open(filepath, O_RDONLY);
    if (fd < 0) {
//	printf("Could not open ns file\n");
        sts = -1;
        goto out;
    }
    
    if (setns(fd, 0)) {
        sts = -1;
    }
    close(fd);

out:
    return Py_BuildValue("i", sts);
}

static PyMethodDef SetnsMethods[] =
{
         {"proc_mount", proc_mount, METH_VARARGS, "Mount a volume via the mount system call."},
         {"proc_umount", proc_umount, METH_VARARGS, "Umount a volume via the umount system call."},
         {"chcontext", chcontext, METH_VARARGS, "Switch into an lxc container."},
         {"chfscontext", chfscontext, METH_VARARGS, "Switch into an lxc container."},
              {NULL, NULL, 0, NULL}
};
 
PyMODINIT_FUNC
 
initsetns(void)
{
         (void) Py_InitModule("setns", SetnsMethods);
}

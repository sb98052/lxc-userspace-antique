#include <Python.h>
#include <fcntl.h>
#include <stdio.h>
#include <asm/unistd.h>
#include <sys/mount.h>
#include <errno.h>
#include <sys/prctl.h>
#include <linux/capability.h>

static PyObject *
drop_caps(PyObject *self, PyObject *args)
{
	unsigned int to_drop[128] = {CAP_NET_ADMIN,CAP_SYS_ADMIN,CAP_SYS_BOOT,CAP_MKNOD,CAP_MAC_ADMIN,CAP_SYS_MODULE};
	unsigned int i;
	for (i = 0;i<6;i++) {
		if (prctl(PR_CAPBSET_DROP, to_drop[i], 0, 0, 0) == -1) {
			perror("prctl");
			return Py_BuildValue("i", 2);
		}
	}
	return Py_BuildValue("i", 0);
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
chfscontext(PyObject *self, PyObject *args)
{
    const char *filepath;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &filepath))
        return NULL;

    int fd = open(filepath, O_RDONLY);
    if (fd < 0) {
        sts = -errno;
        goto out;
    }
    
    if (setns(fd, 0)) {
        sts = -errno;
    }
    close(fd);
    sts = 0;

out:
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
        sts = -errno;
        goto out;
    }
    
    if (setns(fd, 0)) {
        sts = -errno;
    }
    close(fd);
    sts = 0;

out:
    return Py_BuildValue("i", sts);
}

static PyMethodDef SetnsMethods[] =
{
         {"proc_mount", proc_mount, METH_VARARGS, "Mount a volume via the mount system call."},
         {"proc_umount", proc_umount, METH_VARARGS, "Umount a volume via the umount system call."},
         {"chcontext", chcontext, METH_VARARGS, "Switch into an lxc container."},
         {"drop_caps", drop_caps, METH_VARARGS, "Drop dangerous capabilities."},
         {"chfscontext", chfscontext, METH_VARARGS, "Switch into an lxc container."},
              {NULL, NULL, 0, NULL}
};
 
PyMODINIT_FUNC
 
initsetns(void)
{
         (void) Py_InitModule("setns", SetnsMethods);
}

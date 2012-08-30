from distutils.core import setup, Extension
 
module1 = Extension('setns', sources = ['setns.c'])
 
setup (name = 'Setns',
        version = '1.0',
        description = 'Enter an lxc container',
        ext_modules = [module1])

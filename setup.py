from distutils.core import setup, Extension
import subprocess

# ---- edit these variables to configure -----
mpg123_enabled = False # default off, problematic on too many systems
mpg123_include_dirs = []
mpg123_lib_dirs = []
mpg123_libs = ['mpg123']
# --------------------------------------------
# note: it may be necessary to swap #include <Python.h> and #include <mpg123.h>
#       depending on your architecture
# --------------------------------------------

if not mpg123_enabled:
    mpg123_include_dirs, mpg123_lib_dirs, mpg123_libs = [], [], []

p = subprocess.Popen(['MagickWand-config', '--cflags'], stdout=subprocess.PIPE)
extra_compile_args = p.communicate()[0].strip().split()

p = subprocess.Popen(['MagickWand-config', '--ldflags', '--libs'], stdout=subprocess.PIPE)
extra_link_args = p.communicate()[0].strip().split()

cwaveform = Extension(
    'cwaveformmodule',
    sources = [
        'cwaveformmodule.c',
    ],
    define_macros = [] if mpg123_enabled else [('WITHOUT_MPG123', '1')],
    undef_macros = [],
    include_dirs=['/usr/lib'] + mpg123_include_dirs,
    library_dirs=['/usr/include/'] + mpg123_lib_dirs,
    libraries=['sndfile'] + mpg123_libs,
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
)

setup(
    name='waveform',
    version='0.4',
    author="Andrew Kelley",
    author_email="superjoe30@gmail.com",
    description='Create an image of the waveform of an audio file.',
    py_modules=["waveform"],
    ext_modules=[cwaveform],
)


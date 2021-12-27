project('icu', 'c', 'cpp', default_options : ['c_std=c11', 'cpp_std=c++11'])

# How to run python3
python_exec = import('python').find_installation()

# Get version numbers
icu_version = run_command(python_exec,
                          'meson' / 'version_number.py',
                          'common' / 'unicode' / 'uvernum.h',
                          'U_ICU_VERSION').stdout().strip()
icu_lib_major_version = icu_version.split('.')[0]
unicode_version = run_command(python_exec,
                              'meson' / 'version_number.py',
                              'common' / 'unicode' / 'uchar.h',
                              'U_UNICODE_VERSION').stdout().strip()

# C++ compiler
cpp_compiler = meson.get_compiler('cpp')

# Threads
# TODO: Figure out weak threads (--enable-weak-threads in autotools)
thread_dep = dependency('threads')

# Math library
libm_dep = cpp_compiler.find_library('m', required : false)

# How to add defines for the compiler
cpp_def = (cpp_compiler.get_argument_syntax() == 'msvc') ? '/D' : '-D'

# DL library
# This level of checking works for POSIX and Windows, because there are checks
# in common/putil.cpp for DL-related stuff, and the only thing that Windows
# needs to know is whether U_ENABLE_DYLOAD is on.
if get_option('enable_dyload')
  # This is not necessary on POSIX, because you only need to turn it off. But
  # Windows will need it set.
  add_project_arguments(cpp_def + 'U_ENABLE_DYLOAD=1', language : [ 'cpp', 'c' ])
  libdl_dep = cpp_compiler.find_library('dl', required : false)
  if libdl_dep.found()
    cpp_compiler.check_header('dlfcn.h', required : true)
    if not cpp_compiler.has_function('dlopen', dependencies : [ libdl_dep ])
      add_project_arguments(cpp_def + 'HAVE_DLOPEN=0', language : [ 'cpp', 'c' ])
    endif
  endif
else
  add_project_arguments(cpp_def + 'U_ENABLE_DYLOAD=0', language : [ 'cpp', 'c' ])
  libdl_dep = dependency('')
endif

# Whether to enable renaming
if not get_option('enable_renaming')
  add_project_arguments(cpp_def + 'U_DISABLE_RENAMING=1', language : [ 'cpp', 'c' ])
endif

# Whether to enable tracing
if get_option('enable_tracing')
  add_project_arguments(cpp_def + 'U_ENABLE_TRACING=1', language : [ 'cpp', 'c' ])
endif

# elf.h
if cpp_compiler.check_header('elf.h', required : false)
  add_project_arguments(cpp_def + 'U_HAVE_ELF_H=1', language : [ 'cpp', 'c' ])
endif

# Whether to enable plugins
if get_option('enable_plugins')
  add_project_arguments(cpp_def + 'UCONFIG_ENABLE_PLUGINS=1', language : [ 'cpp', 'c' ])
endif

# TODO: Figure out genccode assembly language

# inttypes.h
if not cpp_compiler.check_header('inttypes.h', required : false)
  add_project_arguments(cpp_def + 'U_HAVE_INTTYPES_H=0', language : [ 'cpp', 'c' ])
endif

# dirent.h
if not cpp_compiler.check_header('dirent.h', required : false)
  add_project_arguments(cpp_def + 'U_HAVE_DIRENT_H=0', language : [ 'cpp', 'c' ])
endif

# Endianness
# There is a fairly complete check for this in common/unicode/platform.h, but
# this macro is used in stubdata/stubdata.cpp, so it must be set here. It would
# be possible to set it only for stubdata and let platform.h take care of it for
# other targets, but it seems more prudent to set it on one place.
add_project_arguments(cpp_def + 'U_IS_BIG_ENDIAN=' + (target_machine.endian() == 'big' ? '1' : '0'), language : [ 'cpp', 'c' ])

# nl_langinfo CODESET
if cpp_compiler.check_header('langinfo.h') and cpp_compiler.has_function('nl_langinfo')
  langinfo_tmpl = '''#include <langinfo.h>
int main()
{
  nl_langinfo(@0@);
  return 0;
}'''
  if cpp_compiler.links(langinfo_tmpl.format('CODESET'))
    # Do nothing. This is the normal case.
  elif cpp_compiler.links(langinfo_tmpl.format('_NL_CTYPE_CODESET_NAME'))
    add_project_arguments(cpp_def + 'NL_LANGINFO_CODESET=_NL_CTYPE_CODESET_NAME', language : [ 'cpp', 'c' ])
  else
    add_project_arguments(cpp_def + 'U_HAVE_NL_LANGINFO_CODESET=0', language : [ 'cpp', 'c' ])
  endif
endif

# Validate data packaging
if not [ 'files', 'archive', 'library', 'static' ].contains(get_option('data_packaging'))
  error('Invalid data_packaging "' + get_option('data_packaging') + '". Must be one of: files, archive, library or static.')
endif

# Library suffix
library_suffix = get_option('library_suffix')
if library_suffix != ''
  lib_suffix_cname = run_command(python_exec, '-c', 'import re; print(re.sub("[^A-Za-z0-9_]", "_", r"' + library_suffix + '"))').stdout().strip()
  add_project_arguments(cpp_def + 'U_HAVE_LIB_SUFFIX=1', cpp_def + 'U_LIB_SUFFIX_C_NAME=' + lib_suffix_cname, language : [ 'cpp', 'c' ])
endif

# Windows debug suffix
if target_machine.system() == 'windows' and get_option('buildtype').contains('debug')
  library_suffix += 'd'
endif

# Subdirectories
subdir('stubdata')
subdir('common')
subdir('i18n')
if get_option('enable_icuio')
  subdir('io')
endif
# TODO: Put layoutex here

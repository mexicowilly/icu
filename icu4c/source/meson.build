project('icu', 'c', 'cpp', default_options : ['c_std=c11', 'cpp_std=c++11'])

# Validate data packaging
if not [ 'files', 'archive', 'library', 'static' ].contains(get_option('data_packaging'))
  error('Invalid data_packaging "' + get_option('data_packaging') + '". Must be one of: files, archive, library or static.')
endif

# How to run python3
python_exec = import('python').find_installation()

# TODO: Figure out best way to set output/installation directories: prefix, bindir,
# datadir, etc....

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
  libdl_dep = dependency('', required : false)
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
# TODO: tools (toolutil, genccode) ONLY
if cpp_compiler.check_header('elf.h')
  add_project_arguments(cpp_def + 'U_HAVE_ELF_H=1', language : [ 'cpp', 'c' ])
endif

# Whether to enable plugins
if get_option('enable_plugins')
  add_project_arguments(cpp_def + 'UCONFIG_ENABLE_PLUGINS=1', language : [ 'cpp', 'c' ])
endif

# TODO: Figure out genccode assembly language

# Endianness
# There is a fairly complete check for this in common/unicode/platform.h, but
# this macro is used in stubdata/stubdata.cpp, so it must be set here. It would
# be possible to set it only for stubdata and let platform.h take care of it for
# other targets, but it seems more prudent to set it on one place.
add_project_arguments(cpp_def + 'U_IS_BIG_ENDIAN=' + (target_machine.endian() == 'big' ? '1' : '0'), language : [ 'cpp', 'c' ])

# popen
if not cpp_compiler.has_function('popen')
  add_project_arguments(cpp_def + 'U_HAVE_POPEN=0', language : [ 'cpp', 'c' ])
endif

# NOTE: U_HAVE_STRTOD_L is set but never referenced in the autotools build

# TODO: U_HAVE_STRING_VIEW is only used in test/intltest/strtest.cpp

# stdint.h
zero_or_one = '0'
stdint_inc_def = ''
if cpp_compiler.check_header('stdint.h')
  zero_or_one = '1'
  stdint_inc_def = cpp_def + 'U_HAVE_STDINT_H'
endif
add_project_arguments(cpp_def + 'U_HAVE_STDINT_H=' + zero_or_one, language : [ 'cpp', 'c' ])

# inttypes.h
zero_or_one = '0'
inttypes_inc_def = ''
if cpp_compiler.check_header('inttypes.h')
  zero_or_one = '1'
  inttypes_inc_def = cpp_def + 'U_HAVE_INTTYPES_H'
endif
add_project_arguments(cpp_def + 'U_HAVE_INTTYPES_H=' + zero_or_one, language : [ 'cpp', 'c' ])

# Integer types
int_type_pfx = '''#ifdef U_HAVE_STDINT_H
#include <stdint.h>
#endif
#ifdef U_HAVE_INTTYPES_H
#include <inttypes.h>
#endif'''
foreach integer_type : [ 'int8_t', 'uint8_t', 'int16_t', 'int32_t', 'uint32_t', 'int64_t', 'uint64_t' ]
  if not cpp_compiler.has_type(integer_type, args : [ stdint_inc_def, inttypes_inc_def ], prefix : int_type_pfx)
    add_project_arguments(cpp_def + 'U_HAVE_' + integer_type.to_upper() + '=0', language : [ 'cpp', 'c' ])
  endif
endforeach

# wchar_t
if cpp_compiler.check_header('wchar.h')
  add_project_arguments(cpp_def + 'U_HAVE_WCHAR_H=1', language : [ 'cpp', 'c' ])
  wcs_dep = cpp_compiler.find_library('wcs', required : false)
  w_dep = cpp_compiler.find_library('w', required : false)
  if cpp_compiler.has_function('wcscpy', dependencies : [ wcs_dep, w_dep ])
    add_project_arguments(cpp_def + 'U_HAVE_WCSCPY=1', language : [ 'cpp', 'c' ])
  else
    add_project_arguments(cpp_def + 'U_HAVE_WCSCPY=0', language : [ 'cpp', 'c' ])
  endif
  wchar_pfx = '''#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <wchar.h>'''
  wchar_t_size = cpp_compiler.sizeof('wchar_t', dependencies : [ wcs_dep, w_dep ], prefix : wchar_pfx)
  if wchar_t_size == -1
    error('Could not determine size of wchar_t')
  endif
  add_project_arguments(cpp_def + 'U_SIZEOF_WCHAR_T=' + wchar_t_size.to_string(), language : [ 'cpp', 'c' ])
else
  add_project_arguments([ cpp_def + 'U_HAVE_WCHAR_H=0', cpp_def + 'U_HAVE_WCSCPY=0' ], language : [ 'cpp', 'c' ])
endif

# Find out if we need to use compiler arguments to get UTF16 literal strings
# IBM's compiler
if cpp_compiler.has_argument('-qutf')
  if not cpp_compiler.links('int main() { const unsigned short hello[] = u"hello"; return 0; }', args : [ '-qutf' ])
    error('Compiler argument -qutf is supported but does not link')
  endif
  add_project_arguments('-qutf', language : [ 'cpp', 'c' ])
# Sun/Oracle's compiler
elif cpp_compiler.has_argument('-xustr=ascii_utf16_ushort')
  if not cpp_compiler.links('int main() { const unsigned short hello[] = U"hello"; return 0; }', args : [ '-xustr=ascii_utf16_ushort' ])
    error('Compiler argument -xustr=ascii_utf16_ushort is supported but does not link')
  endif
  add_project_arguments('-xustr=ascii_utf16_ushort', language : [ 'cpp', 'c' ])
endif

# Library suffix
library_suffix = get_option('library_suffix')
if library_suffix != ''
  lib_suffix_cname = library_suffix.underscorify()
  add_project_arguments(cpp_def + 'U_HAVE_LIB_SUFFIX=1', cpp_def + 'U_LIB_SUFFIX_C_NAME=' + lib_suffix_cname, language : [ 'cpp', 'c' ])
endif

# Windows debug suffix
if target_machine.system() == 'windows' and get_option('buildtype').contains('debug')
  library_suffix += 'd'
endif

# Convenience variables for deciding which libraries to build
default_library_option = get_option('default_library')
build_shared = default_library_option == 'shared' or default_library_option == 'both'
build_static = default_library_option == 'static' or default_library_option == 'both'

# Subdirectories
subdir('stubdata')
subdir('common')
subdir('i18n')
if get_option('enable_icuio')
  subdir('io')
endif
# TODO: Put layoutex here
subdir('tools')

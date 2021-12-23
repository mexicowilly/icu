project('icu', 'c', 'cpp', default_options : ['c_std=c11', 'cpp_std=c++11'])

# How to run python3
python_exec = import('python').find_installation()

# Get version numbers
icu_version = run_command(python_exec,
                          meson.current_source_dir() / 'meson' / 'version_number.py',
                          meson.current_source_dir() / 'common' / 'unicode' / 'uvernum.h',
                          'U_ICU_VERSION').stdout().strip()
icu_lib_major_version = icu_version.split('.')[0]
unicode_version = run_command(python_exec,
                              meson.current_source_dir() / 'meson' / 'version_number.py',
                              meson.current_source_dir() / 'common' / 'unicode' / 'uchar.h',
                              'U_UNICODE_VERSION').stdout().strip()

# C++ compiler
cpp_compiler = meson.get_compiler('cpp')

# Threads
thread_dep = dependency('threads')

# Math library
libm_dep = cpp_compiler.find_library('m', required : false)

# Dl library
if get_option('enable_dyload')
  libdl_dep = cpp_compiler.find_library('dl', required : false)
else
  add_global_arguments('-DU_ENABLE_DYLOAD=0', language : [ 'cpp', 'c' ])
  libdl_dep = dependency('')
endif

# Endianness: There is a fairly complete check for this in common/unicode/platform.h, but
# this macro is used in stubdata/stubdata.cpp, so it must be set here.
add_global_arguments('-DU_IS_BIG_ENDIAN=' + (build_machine.endian() == 'big' ? '1' : '0'), language : [ 'cpp', 'c' ])

# Validate data packaging
if not [ 'files', 'archive', 'library', 'static' ].contains(get_option('data_packaging'))
  error('Invalid data_packaging "' + get_option('data_packaging') + '". Must be one of: files, archive, library or static.')
endif

# Subdirectories
subdir('stubdata')
subdir('common')
subdir('i18n')

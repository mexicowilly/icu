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

# Subdirectories
subdir('stubdata')
subdir('common')

toolutil_shared_name = 'icutu'
if target_machine.system() == 'windows'
  toolutil_shared_name += icu_lib_major_version
endif
toolutil_shared_name += library_suffix
toolutil_static_name = 's' + toolutil_shared_name

toolutil_sources = run_command(python_exec,
                               '..' / '..' / 'meson' / 'lines_as_string.py',
                               'sources.txt').stdout().strip().split(' ')

# This library wants the paths of the compilers
cc_path = run_command(python_exec, '-c', 'import shutil; print(shutil.which("' + meson.get_compiler('c').cmd_array()[0] + '"))').stdout().strip()
cpp_path = run_command(python_exec, '-c', 'import shutil; print(shutil.which("' + cpp_compiler.cmd_array()[0] + '"))').stdout().strip()

toolutil_args = [
  cpp_def + 'U_TOOLUTIL_IMPLEMENTATION',
  cpp_def + 'U_BUILD="' + build_machine.system() + '"',
  cpp_def + 'U_HOST="' + host_machine.system() + '"',
  cpp_def + 'U_CC="' + cc_path + '"',
  cpp_def + 'U_CXX="' + cpp_path + '"',
  cpp_def + 'UNISTR_FROM_CHAR_EXPLICIT=explicit',
  cpp_def + 'UNISTR_FROM_STRING_EXPLICIT=explicit'
]

if cpp_compiler.check_header('elf.h')
  toolutil_args += [ cpp_def + 'U_HAVE_ELF_H=1' ]
endif

if build_shared
  toolutil_shared = shared_library(toolutil_shared_name,
                                   toolutil_sources,
                                   cpp_args : toolutil_args,
                                   dependencies : i18n_shared_dep,
                                   version : icu_version)
  toolutil_shared_dep = declare_dependency(include_directories : include_directories('.'),
                                           dependencies : i18n_shared_dep,
                                           link_with : toolutil_shared)
else
  toolutil_shared_dep = dependency('', required : false)
endif

if build_static
  toolutil_static = static_library(toolutil_static_name,
                                   toolutil_sources,
                                   cpp_args : toolutil_args + [ cpp_def + 'U_STATIC_IMPLEMENTATION' ],
                                   dependencies : i18n_shared_dep)
  toolutil_static_dep = declare_dependency(include_directories : include_directories('.'),
                                           dependencies : i18n_static_dep,
                                           link_with : toolutil_static)
else
  toolutil_static_dep = dependency('', required : false)
endif

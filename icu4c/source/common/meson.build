common_shared_name = 'icuuc'
if build_machine.system() == 'windows'
  common_shared_name += icu_lib_major_version
endif
common_static_name = 's' + common_shared_name

common_sources = run_command(python_exec,
                             '..' / 'meson' / 'lines_as_string.py',
                             'sources.txt').stdout().strip().split(' ')

common_args = [
  '-DU_COMMON_IMPLEMENTATION',
  '-DDEFAULT_ICU_PLUGINS=' + get_option('prefix') / get_option('libdir')
]
if get_option('data_packaging') == 'archive'
  common_args += '-DICU_DATA_DEFAULT_DIR=' + get_option('prefix') / get_option('datadir')
endif

common_deps = [ thread_dep, libdl_dep, libm_dep ]

common_shared = shared_library(common_shared_name,
                               common_sources,
                               cpp_args : common_args,
                               link_with : stubdata_shared,
                               dependencies : common_deps,
                               version : icu_version)
common_shared_dep = declare_dependency(dependencies : common_deps,
                                       include_directories : include_directories('.'),
                                       link_with : common_shared)
common_static = static_library(common_static_name,
                               common_sources,
                               cpp_args : common_args + [ '-DU_STATIC_IMPLEMENTATION' ],
                               link_with : stubdata_static,
                               dependencies : common_deps)
common_static_dep = declare_dependency(dependencies : common_deps,
                                       include_directories : include_directories('.'),
                                       link_with : common_static)

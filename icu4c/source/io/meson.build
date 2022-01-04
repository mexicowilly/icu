io_shared_name = 'icuio'
if target_machine.system() == 'windows'
  io_shared_name += icu_lib_major_version
endif
io_shared_name += library_suffix
io_static_name = 's' + io_shared_name

io_sources = run_command(python_exec,
                         '..' / 'meson' / 'lines_as_string.py',
                         'sources.txt').stdout().strip().split(' ')

io_shared = shared_library(io_shared_name,
                           io_sources,
                           cpp_args : [ cpp_def + 'U_IO_IMPLEMENTATION' ],
                           dependencies : i18n_shared_dep,
                           version : icu_version)
io_shared_dep = declare_dependency(include_directories : include_directories('.'),
                                   dependencies : i18n_shared_dep,
                                   link_with : io_shared)
io_static = static_library(io_static_name,
                           io_sources,
                           cpp_args : [ cpp_def + 'U_IO_IMPLEMENTATION', cpp_def + 'U_STATIC_IMPLEMENTATION' ],
                           dependencies : i18n_static_dep)
io_static_dep = declare_dependency(include_directories : include_directories('.'),
                                   dependencies : i18n_static_dep,
                                   link_with : io_static)

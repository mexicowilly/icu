if target_machine.system() == 'windows'
  i18n_shared_name = 'icuin' + icu_lib_major_version
else
  i18n_shared_name = 'icui18n'
endif
i18n_shared_name += library_suffix
i18n_static_name = 's' + i18n_shared_name

i18n_sources = run_command(python_exec,
                           '..' / 'meson' / 'lines_as_string.py',
                           'sources.txt').stdout().strip().split(' ')

if build_shared
  i18n_shared = shared_library(i18n_shared_name,
                               i18n_sources,
                               cpp_args : [ cpp_def + 'U_I18N_IMPLEMENTATION' ],
                               dependencies : common_shared_dep,
                               version : icu_version)
  i18n_shared_dep = declare_dependency(include_directories : include_directories('.'),
                                       dependencies : common_shared_dep,
                                       link_with : i18n_shared)
else
  i18n_shared_dep = dependency('', required : false)
endif

if build_static
  i18n_static = static_library(i18n_static_name,
                               i18n_sources,
                               cpp_args : [ cpp_def + 'U_I18N_IMPLEMENTATION', cpp_def + 'U_STATIC_IMPLEMENTATION' ],
                               dependencies : common_static_dep)
  i18n_static_dep = declare_dependency(include_directories : include_directories('.'),
                                       dependencies : common_static_dep,
                                       link_with : i18n_static)
else
  i18n_static_dep = dependency('', required : false)
endif

if build_machine.system() == 'windows'
  i18n_shared_name = 'icuin' + icu_lib_major_version
else
  i18n_shared_name = 'icui18n'
endif
i18n_static_name = 's' + i18n_shared_name

i18n_sources = run_command(python_exec,
                           '..' / 'meson' / 'lines_as_string.py',
                           'sources.txt').stdout().strip().split(' ')

i18n_shared = shared_library(i18n_shared_name,
                             i18n_sources,
                             cpp_args : [ '-DU_I18N_IMPLEMENTATION' ],
                             include_directories : '..' / 'common',
                             link_with : common_shared,
                             version : icu_version)
i18n_static = static_library(i18n_static_name,
                             i18n_sources,
                             cpp_args : [ '-DU_I18N_IMPLEMENTATION', '-DU_STATIC_IMPLEMENTATION' ],
                             include_directories : '..' / 'common',
                             link_with : common_static)

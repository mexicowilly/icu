ctestfw_shared_name = 'icutest'
if target_machine.system() == 'windows'
  ctestfw_shared_name += icu_lib_major_version
endif
ctestfw_shared_name += library_suffix
ctestfw_static_name = 's' + ctestfw_shared_name

ctestfw_sources = run_command(python_exec,
                              '..' / '..' / 'meson' / 'lines_as_string.py',
                              'sources.txt').stdout().strip().split(' ')

if build_shared
  ctestfw_shared = shared_library(ctestfw_shared_name,
                                  ctestfw_sources,
                                  cpp_args : [ cpp_def + 'T_CTEST_IMPLEMENTATION' ],
                                  c_args : [ cpp_def + 'T_CTEST_IMPLEMENTATION' ],
                                  dependencies : toolutil_shared_dep,
                                  version : icu_version)
  ctestfw_shared_dep = declare_dependency(include_directories : include_directories('.'),
                                          dependencies : toolutil_shared_dep,
                                          link_with : ctestfw_shared)
else
  ctestfw_shared_dep = dependency('', required : false)
endif

if build_static
  ctestfw_static = static_library(ctestfw_static_name,
                                  ctestfw_sources,
                                  cpp_args : [ cpp_def + 'T_CTEST_IMPLEMENTATION', cpp_def + 'U_STATIC_IMPLEMENTATION' ],
                                  c_args : [ cpp_def + 'T_CTEST_IMPLEMENTATION', cpp_def + 'U_STATIC_IMPLEMENTATION' ],
                                  dependencies : toolutil_shared_dep)
  ctestfw_static_dep = declare_dependency(include_directories : include_directories('.'),
                                          dependencies : toolutil_static_dep,
                                          link_with : ctestfw_static)
else
  ctestfw_static_dep = dependency('', required : false)
endif

if target_machine.system() == 'windows'
  data_shared_name = 'icudt' + icu_lib_major_version
else
  data_shared_name = 'icudata'
endif
data_shared_name += library_suffix
data_static_name = 's' + data_shared_name

if build_shared
  if target_machine.system() == 'linux'
    stubdata_link_args = [ '-nodefaultlibs', '-nostdlib' ]
  else
    stubdata_link_args = [ ]
  endif
  stubdata_shared = shared_library(data_shared_name,
                                   'stubdata.cpp',
                                   include_directories : '..' / 'common',
                                   version : icu_version,
                                   link_args : stubdata_link_args)
  stubdata_shared_dep = declare_dependency(link_with : stubdata_shared)
else
  stubdata_shared_dep = dependency('', required : false)
endif

if build_static
  stubdata_static = static_library(data_static_name,
                                   'stubdata.cpp',
                                   include_directories : '..' / 'common')
  stubdata_static_dep = declare_dependency(link_with : stubdata_static)
else
  stubdata_static_dep = dependency('', required : false)
endif

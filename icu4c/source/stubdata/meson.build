if build_machine.system() == 'windows'
  data_shared_name = 'icudt' + icu_lib_major_version
else
  data_shared_name = 'icudata'
endif
data_static_name = 's' + data_shared_name

shared_library(data_shared_name,
               'stubdata.cpp',
               version : icu_version)
static_library(data_static_name,
               'stubdata.cpp')

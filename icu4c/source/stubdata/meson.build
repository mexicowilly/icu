if target_machine.system() == 'windows'
  data_shared_name = 'icudt' + icu_lib_major_version
else
  data_shared_name = 'icudata'
endif
data_shared_name += library_suffix
data_static_name = 's' + data_shared_name

stubdata_shared = shared_library(data_shared_name,
                                 'stubdata.cpp',
                                 include_directories : '..' / 'common',
                                 version : icu_version)
stubdata_static = static_library(data_static_name,
                                 'stubdata.cpp',
                                 include_directories : '..' / 'common')

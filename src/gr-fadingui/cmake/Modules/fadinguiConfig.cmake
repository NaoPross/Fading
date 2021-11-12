INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_FADINGUI fadingui)

FIND_PATH(
    FADINGUI_INCLUDE_DIRS
    NAMES fadingui/api.h
    HINTS $ENV{FADINGUI_DIR}/include
        ${PC_FADINGUI_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    FADINGUI_LIBRARIES
    NAMES gnuradio-fadingui
    HINTS $ENV{FADINGUI_DIR}/lib
        ${PC_FADINGUI_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/fadinguiTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(FADINGUI DEFAULT_MSG FADINGUI_LIBRARIES FADINGUI_INCLUDE_DIRS)
MARK_AS_ADVANCED(FADINGUI_LIBRARIES FADINGUI_INCLUDE_DIRS)

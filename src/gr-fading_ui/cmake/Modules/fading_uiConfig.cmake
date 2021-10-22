INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_FADING_UI fading_ui)

FIND_PATH(
    FADING_UI_INCLUDE_DIRS
    NAMES fading_ui/api.h
    HINTS $ENV{FADING_UI_DIR}/include
        ${PC_FADING_UI_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    FADING_UI_LIBRARIES
    NAMES gnuradio-fading_ui
    HINTS $ENV{FADING_UI_DIR}/lib
        ${PC_FADING_UI_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/fading_uiTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(FADING_UI DEFAULT_MSG FADING_UI_LIBRARIES FADING_UI_INCLUDE_DIRS)
MARK_AS_ADVANCED(FADING_UI_LIBRARIES FADING_UI_INCLUDE_DIRS)

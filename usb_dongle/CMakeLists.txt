cmake_minimum_required(VERSION 3.13)

include(pico_sdk_import.cmake)
# initialize pico-sdk from submodule
# note: this must happen before project()

project(Ripxospeech_controller_firmware)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# initialize the Raspberry Pi Pico SDK
pico_sdk_init()

include_directories(
    ./
    ../interface
)

set(Sources
    main.c
    hid.c
    cdc.c
    usb.c
    usb_descriptors.c
    pc_protocol.c
    controller.c
    keyboard.c
    keyboard_helper.c
    )

add_executable(Ripxospeech_controller_firmware ${Sources})
add_executable(Ripxospeech_controller_firmware_no_boot ${Sources})

set(Libs
    pico_sync
    pico_multicore
    pico_stdlib
    hardware_i2c
    tinyusb_device
    tinyusb_board
    )


# Add pico_stdlib library which aggregates commonly used features
target_link_libraries(Ripxospeech_controller_firmware ${Libs})
target_link_libraries(Ripxospeech_controller_firmware_no_boot ${Libs})

# create map/bin/hex/uf2 file in addition to ELF.
pico_add_extra_outputs(Ripxospeech_controller_firmware)
pico_add_extra_outputs(Ripxospeech_controller_firmware_no_boot)

set_target_properties(Ripxospeech_controller_firmware PROPERTIES COMPILE_FLAGS "-Wall")
pico_set_linker_script(Ripxospeech_controller_firmware ${CMAKE_CURRENT_SOURCE_DIR}/app.ld)

# Generate from build with: cmake -LA .. -DCMAKE_CXX_FLAGS_RELEASE="-O3 -DNDEBUG"

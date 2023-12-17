cmake_minimum_required(VERSION 3.13)

include(pico_sdk_import.cmake)
# initialize pico-sdk from submodule
# note: this must happen before project()

project(ripxospeech_controller_firmware)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# initialize the Raspberry Pi Pico SDK
pico_sdk_init()

include_directories(
    ./
)

set(Sources
    main.c
    hid.c
    cdc.c
    usb.c
    usb_descriptors.c
    app.c
    )

add_executable(ripxospeech_controller_firmware ${Sources})

set(Libs
    pico_sync
    pico_multicore
    pico_stdlib
    hardware_i2c
    tinyusb_device
    tinyusb_board
    )


# Add pico_stdlib library which aggregates commonly used features
target_link_libraries(ripxospeech_controller_firmware ${Libs})

# create map/bin/hex/uf2 file in addition to ELF.
pico_add_extra_outputs(ripxospeech_controller_firmware)

set_target_properties(ripxospeech_controller_firmware PROPERTIES COMPILE_FLAGS "-Wall")

# Generate from build with: cmake -LA .. -DCMAKE_CXX_FLAGS_RELEASE="-O3 -DNDEBUG"

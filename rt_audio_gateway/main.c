#include <stdio.h>
#include <stdlib.h>
#include <alsa/asoundlib.h>
#include <math.h> // Include math.h for sin and M_PI
#include <unistd.h> // Include unistd.h for sleep

#define SAMPLE_RATE 48000
#define BUFFER_SIZE 256
#define PERIOD_SIZE 128

snd_pcm_t *pcm_handle;
short *buffer;
double phase = 0.0;
double phase_step = 2 * M_PI * 440.0 / SAMPLE_RATE; // Calculate phase step for 440 Hz

void callback(snd_async_handler_t *handler) {
    (void)handler; // Suppress unused variable warning (handler is used in the callback signature
    int err;

    for (snd_pcm_uframes_t i = 0; i < BUFFER_SIZE * 2; i += 2) { // 2 channels
        short sample = (short)(32767.0 * sin(phase));
        buffer[i] = sample; // left channel
        buffer[i + 1] = sample; // right channel
        phase += phase_step;
        if (phase > 2 * M_PI) phase -= 2 * M_PI; // Keep phase within [0, 2*pi]
    }

    // Write data to PCM device
    if ((err = snd_pcm_writei(pcm_handle, buffer, BUFFER_SIZE)) < 0) {
        fprintf(stderr, "Write to PCM device failed: %s\n", snd_strerror(err));
    }
}

int main() {
    int err;
    snd_pcm_hw_params_t *params;
    unsigned int rate = SAMPLE_RATE;
    snd_pcm_uframes_t buffer_size = BUFFER_SIZE;
    snd_pcm_uframes_t period_size = PERIOD_SIZE;

    // Open PCM device for playback
    if ((err = snd_pcm_open(&pcm_handle, "hw:1,0", SND_PCM_STREAM_PLAYBACK, 0)) < 0) {
        fprintf(stderr, "Cannot open PCM device: %s\n", snd_strerror(err));
        exit(1);
    }

    // Allocate hardware parameters object
    if ((err = snd_pcm_hw_params_malloc(&params)) < 0) {
        fprintf(stderr, "Cannot allocate hardware parameter structure: %s\n", snd_strerror(err));
        exit(1);
    }

    // Initialize hardware parameters with default values
    if ((err = snd_pcm_hw_params_any(pcm_handle, params)) < 0) {
        fprintf(stderr, "Cannot initialize hardware parameter structure: %s\n", snd_strerror(err));
        exit(1);
    }

    // Set access type
    if ((err = snd_pcm_hw_params_set_access(pcm_handle, params, SND_PCM_ACCESS_RW_INTERLEAVED)) < 0) {
        fprintf(stderr, "Cannot set access type: %s\n", snd_strerror(err));
        exit(1);
    }

    // Set sample format
    if ((err = snd_pcm_hw_params_set_format(pcm_handle, params, SND_PCM_FORMAT_S16_LE)) < 0) {
        fprintf(stderr, "Cannot set sample format: %s\n", snd_strerror(err));
        exit(1);
    }

    // Set sample rate
    if ((err = snd_pcm_hw_params_set_rate_near(pcm_handle, params, &rate, 0)) < 0) {
        fprintf(stderr, "Cannot set sample rate: %s\n", snd_strerror(err));
        exit(1);
    }

    // Set buffer size
    if ((err = snd_pcm_hw_params_set_buffer_size_near(pcm_handle, params, &buffer_size)) < 0) {
        fprintf(stderr, "Cannot set buffer size: %s\n", snd_strerror(err));
        exit(1);
    }

    // Set period size
    if ((err = snd_pcm_hw_params_set_period_size_near(pcm_handle, params, &period_size, 0)) < 0) {
        fprintf(stderr, "Cannot set period size: %s\n", snd_strerror(err));
        exit(1);
    }

    // Apply hardware parameters
    if ((err = snd_pcm_hw_params(pcm_handle, params)) < 0) {
        fprintf(stderr, "Cannot set hardware parameters: %s\n", snd_strerror(err));
        exit(1);
    }

    // Allocate buffer
    buffer = (short *)malloc(buffer_size * 2 * sizeof(short)); // 2 channels, 2 bytes per channel

    // Create and set up the asynchronous handler
    snd_async_handler_t *handler;
    snd_async_add_pcm_handler(&handler, pcm_handle, callback, NULL);

    callback(handler);

    // Main loop
    while (1) {
        sleep(1);
    }

    // Cleanup
    free(buffer);
    snd_pcm_close(pcm_handle);
    snd_pcm_hw_params_free(params);

    return 0;
}
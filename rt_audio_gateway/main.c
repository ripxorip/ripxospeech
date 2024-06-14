#include <math.h>

#include <spa/param/audio/format-utils.h>

#include <pthread.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>

#include <pipewire/pipewire.h>

#define M_PI_M2 ( M_PI + M_PI )

#define DEFAULT_RATE            48000
#define DEFAULT_CHANNELS        2
#define DEFAULT_VOLUME          0.7

#define SAMPLES_PER_BUFFER 256

#define STREAM_PORT 8321

struct data {
        struct pw_main_loop *loop;
        struct pw_stream *stream;
        double accumulator;
};

typedef struct {
    uint16_t n_samples;
    uint64_t seq;
    uint64_t timestamp;
    uint16_t samples[SAMPLES_PER_BUFFER];
} rt_stream_packet_t;

struct {
    rt_stream_packet_t packet;
} internal = {0};

void* stream_thread(void* arg) {
    int sockfd;
    struct sockaddr_in servaddr;

    // Create socket
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);

    // Bind socket to the specified PORT
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    servaddr.sin_port = htons(STREAM_PORT);
    bind(sockfd, (struct sockaddr*)&servaddr, sizeof(servaddr));

    while (1) {
        rt_stream_packet_t packet;

        // Receive packet
        recvfrom(sockfd, &packet, sizeof(packet), 0, NULL, NULL);
        printf("Received packet with %d samples\n", packet.n_samples);
        memcpy(&internal.packet, &packet, sizeof(packet));

        // Process packet
        // ...
    }

    close(sockfd);

    return NULL;
}

/* [on_process] */
static void on_process(void *userdata)
{
        struct data *data = userdata;
        struct pw_buffer *b;
        struct spa_buffer *buf;
        int i, c, n_frames, stride;
        int16_t *dst, val;

        if ((b = pw_stream_dequeue_buffer(data->stream)) == NULL) {
                pw_log_warn("out of buffers: %m");
                return;
        }

        buf = b->buffer;
        if ((dst = buf->datas[0].data) == NULL)
                return;

        stride = sizeof(int16_t) * DEFAULT_CHANNELS;
        n_frames = buf->datas[0].maxsize / stride;
        if (b->requested)
                n_frames = SPA_MIN(b->requested, n_frames);

        #if 0
        for (i = 0; i < n_frames; i++) {
                data->accumulator += M_PI_M2 * 440 / DEFAULT_RATE;
                if (data->accumulator >= M_PI_M2)
                        data->accumulator -= M_PI_M2;

                /* sin() gives a value between -1.0 and 1.0, we first apply
                 * the volume and then scale with 32767.0 to get a 16 bits value
                 * between [-32767 32767].
                 * Another common method to convert a double to
                 * 16 bits is to multiple by 32768.0 and then clamp to
                 * [-32768 32767] to get the full 16 bits range. */
                val = sin(data->accumulator) * DEFAULT_VOLUME * 32767.0;
                for (c = 0; c < DEFAULT_CHANNELS; c++)
                        *dst++ = val;
        }
        #endif

        for (i = 0; i < n_frames; i++) {
            for (c = 0; c < DEFAULT_CHANNELS; c++) {
                *dst++ = internal.packet.samples[i];
            }
        }


        buf->datas[0].chunk->offset = 0;
        buf->datas[0].chunk->stride = stride;
        buf->datas[0].chunk->size = n_frames * stride;

        pw_stream_queue_buffer(data->stream, b);
}
/* [on_process] */

static const struct pw_stream_events stream_events = {
        PW_VERSION_STREAM_EVENTS,
        .process = on_process,
};

int main(int argc, char *argv[])
{
        struct data data = { 0, };
        const struct spa_pod *params[1];
        uint8_t buffer[1024];
        struct spa_pod_builder b = SPA_POD_BUILDER_INIT(buffer, sizeof(buffer));
        pthread_t thread_id;

        /* Not the most elegant way of doing this, but it will do for now, will PoC if this will
           even turn out to work or not haha */
        char latency[20];
        sprintf(latency, "%d/48000", SAMPLES_PER_BUFFER);
        setenv("PIPEWIRE_LATENCY", latency, 1);

        pw_init(&argc, &argv);

        data.loop = pw_main_loop_new(NULL);

        data.stream = pw_stream_new_simple(
                        pw_main_loop_get_loop(data.loop),
                        "audio-src",
                        pw_properties_new(
                                PW_KEY_MEDIA_TYPE, "Audio",
                                PW_KEY_MEDIA_CATEGORY, "Playback",
                                PW_KEY_MEDIA_ROLE, "Music",
                                PW_KEY_TARGET_OBJECT, "alsa_output.pci-0000_09_00.6.analog-stereo",  // Specify your desired audio interface here
                                NULL),
                        &stream_events,
                        &data);

        params[0] = spa_format_audio_raw_build(&b, SPA_PARAM_EnumFormat,
                        &SPA_AUDIO_INFO_RAW_INIT(
                                .format = SPA_AUDIO_FORMAT_S16,
                                .channels = DEFAULT_CHANNELS,
                                .rate = DEFAULT_RATE ));

        pw_stream_connect(data.stream,
                          PW_DIRECTION_OUTPUT,
                          PW_ID_ANY,
                          PW_STREAM_FLAG_AUTOCONNECT |
                          PW_STREAM_FLAG_MAP_BUFFERS |
                          PW_STREAM_FLAG_RT_PROCESS,
                          params, 1);

        pthread_create(&thread_id, NULL, stream_thread, NULL);

        pw_main_loop_run(data.loop);

        pw_stream_destroy(data.stream);
        pw_main_loop_destroy(data.loop);
        pthread_join(thread_id, NULL);

        return 0;
}

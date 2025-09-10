#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <math.h>
#include <alsa/asoundlib.h>


#define A4 440.00
#define B4 493.88
#define C5 523.25
#define D5 587.33
#define E5 659.26
#define F5 698.46
#define G5 783.99
#define A6 880.00


typedef struct {
    // PCM = Pulse Code Modulation
    // snd_pcm_t is a handle for controlling the sound device
    snd_pcm_t *pcm_handle;

    // The ALSA parameters for the sound.
    snd_pcm_hw_params_t *params;

    // Some parameters we track
    unsigned int channels;
    snd_pcm_uframes_t frames;
    unsigned int sample_rate;
} Audio;


void create_audio(Audio *audio) {
    // Allocate the snd_pcm_t object.
    // Note that the first parameter is **pcm_handle.
    // We clean this up with snd_pcm_close(pcm_handle).
    //
    // mode is a bitmask of flags:
    // 0 = default (blocking mode)
    // SND_PCM_NONBLOCK = set non-blocking mode
    // SND_PCM_ASYNC = enables async notification via signals (rarely used)
    int mode = 0;

    if (snd_pcm_open(&audio->pcm_handle, "default", SND_PCM_STREAM_PLAYBACK, mode) < 0) {
        perror("snd_pcm_open");
        exit(1);
    }

    // Allocate parameters object and fill it with default values
    snd_pcm_hw_params_alloca(&audio->params);
    snd_pcm_hw_params_any(audio->pcm_handle, audio->params);

    // Set parameters
    audio->channels = 1;
    snd_pcm_hw_params_set_channels(audio->pcm_handle, audio->params, audio->channels);

    // Interleaved, for stereo, means the samples are packed LRLRLRLR... in memory.
    // Eg, it interleaves the left and right speaker samples.
    // By the way, a "sample" in ALSA, means one reading of the sound pressure *in a channel*.
    snd_pcm_hw_params_set_access(audio->pcm_handle, audio->params, SND_PCM_ACCESS_RW_INTERLEAVED);

    // signed 16-bit integer, little endian is pretty standard.
    snd_pcm_hw_params_set_format(audio->pcm_handle, audio->params, SND_PCM_FORMAT_S16_LE);

    // The rounding direction is a convention used by ALSA.
    // 0 = round to the nearest
    // +1 = round up, if you have to
    // -1 = round down, if you have to
    // These functions will update this parameter *in place* to indicate the actual direction rounded.
    // These functions also modify the incoming parameter passed (here, audio->sample_rate)
    // to the exact value that was ultimately chosen.
    int sample_rate_rounding_dir = 0;
    audio->sample_rate = 44100;
    snd_pcm_hw_params_set_rate_near(audio->pcm_handle, audio->params, &audio->sample_rate, &sample_rate_rounding_dir);

    // a "frame" is a collection which has one sample per channel.
    // So 1 frame for stereo = 2 samples
    // The period is the number of frames that ALSA reads or writes at once.
    int frame_rounding_dir = 0;
    audio->frames = 32;
    snd_pcm_hw_params_set_period_size_near(audio->pcm_handle, audio->params, &audio->frames, &frame_rounding_dir);

    // Write parameters to driver
    if (snd_pcm_hw_params(audio->pcm_handle, audio->params) < 0) {
        perror("snd_pcm_hw_params");
        exit(1);
    }
}


void destroy_audio(Audio *audio) {
    snd_pcm_close(audio->pcm_handle);
}


double trianglewave(double t, double freq, double amplitude) {
    double period = 1.0 / freq;
    while (t > period) {
        t -= period;
    }
    return (2 * M_PI * t * freq - M_PI) * INT16_MAX * amplitude;
}


double squarewave(double t, double freq, double amplitude) {
    double period = 1.0 / freq;
    while (t > period) {
        t -= period;
    }

    if (t < period / 2.0) {
        return INT16_MAX * amplitude;
    } else {
        return -INT16_MAX * amplitude;
    }
}


double sinwave(double t, double freq, double amplitude) {
    return sin(2 * M_PI * t * freq) * INT16_MAX * amplitude;
}

int main() {
    Audio audio;
    create_audio(&audio);

    int16_t *buffer = (int16_t *)malloc(audio.frames * audio.channels * sizeof(int16_t));

    double duration_secs = 1.0;
    uint32_t num_periods = (int)(audio.sample_rate / audio.frames * duration_secs);

    double t = 0.0;

    // for each period
    for (int i = 0; i < num_periods; i++) {
        for (int j = 0; j < audio.frames; j++) {
            buffer[j] = (int16_t)(
//                sinwave(t, A4, 0.02)
//                squarewave(t, A4, 0.02)
                trianglewave(t, A4, 0.01)
            );
            t += 1.0 / audio.sample_rate;
        }

        // Actually write the buffer to ALSA.
        // The "i" in "writei" stands for interleaved.
        // This blocks until all the bytes are written to the buffer
        // unless nonblocking mode is selected.
        snd_pcm_sframes_t result = snd_pcm_writei(audio.pcm_handle, buffer, audio.frames);
        if (result < 0) {
            if (result == -EPIPE) {
                // If the buffer ran out of samples,
                // but the device is ready to play
                snd_pcm_prepare(audio.pcm_handle);
                printf("Underrun on period %d\n", i);
            } else {
                perror("snd_pcm_writei");
                exit(1);
            }
        }
    }


    // Block until the whole buffer is drained into the sink.
    // Forgetting to do this will cause the program to exit
    // before the whole buffer has been played.
    snd_pcm_drain(audio.pcm_handle);

    free(buffer);
    destroy_audio(&audio);

    return 0;
}

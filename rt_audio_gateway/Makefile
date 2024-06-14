CC = gcc
CFLAGS += $(shell pkg-config --cflags libpipewire-0.3) -I../rt_audio_common -Iinc -Wall
LDFLAGS = -lm $(shell pkg-config --libs libpipewire-0.3) 
TARGET = rtaudiogateway
SRCS = src/main.c src/rt_receiver.c
OUTDIR = _out
OBJS = $(addprefix $(OUTDIR)/, $(SRCS:.c=.o))
Q = @

all: dir $(TARGET)

dir:
	$(Q)mkdir -p $(dir $(OBJS))

$(TARGET): $(OBJS)
	$(Q)$(CC) $(CFLAGS) -o $(OUTDIR)/$(TARGET) $(OBJS) $(LDFLAGS)

$(OUTDIR)/%.o: %.c
	$(Q)$(CC) $(CFLAGS) -c $< -o $@

clean:
	$(Q)rm -rf $(OUTDIR)
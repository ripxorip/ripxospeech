CC = gcc
CFLAGS = -Wall
LDFLAGS = -lasound -lm
TARGET = rtaudiogateway
SRCS = main.c
OBJS = $(addprefix $(OUTDIR)/, $(SRCS:.c=.o))
OUTDIR = _out
Q = @

all: dir $(TARGET)

dir:
	$(Q)mkdir -p $(OUTDIR)

$(TARGET): $(OBJS)
	$(Q)$(CC) $(CFLAGS) -o $(OUTDIR)/$(TARGET) $(OBJS) $(LDFLAGS)

$(OUTDIR)/%.o: %.c
	$(Q)$(CC) $(CFLAGS) -c $< -o $@

clean:
	$(Q)rm -f $(OUTDIR)/*.o
	$(Q)rm -f $(OUTDIR)/$(TARGET)
	$(Q)rmdir $(OUTDIR)

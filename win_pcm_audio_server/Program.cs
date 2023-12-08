using System;
using System.Net;
using System.Net.Sockets;
using NAudio.Wave;

class UdpAudioReceiver
{
    private const int Port = 12345; // UDP port for receiving audio data
    private const int BufferSize = 1024; // Adjust as needed based on your requirements
    private static CustomBufferedWaveProvider bufferedWaveProvider;
    private static WaveOutEvent waveOut;

    static void Main()
    {
        // Initialize NAudio WaveOutEvent and CustomBufferedWaveProvider
        waveOut = new WaveOutEvent();
        bufferedWaveProvider = new CustomBufferedWaveProvider(new WaveFormat(44100, 16, 1), BufferSize);

        // Attach the CustomBufferedWaveProvider to the WaveOutEvent
        waveOut.Init(bufferedWaveProvider);

        // Create UDP client for receiving audio data
        UdpClient udpClient = new UdpClient(Port);

        Console.WriteLine("Listening for audio data on port {0}...", Port);

        try
        {
            while (true)
            {
                IPEndPoint remoteEP = new IPEndPoint(IPAddress.Any, 0);
                byte[] receivedData = udpClient.Receive(ref remoteEP);

                // Process the received audio data and add it to the buffer
                bufferedWaveProvider.AddSamples(receivedData, 0, receivedData.Length);

                // Start playback if not already playing
                if (waveOut.PlaybackState != PlaybackState.Playing)
                {
                    waveOut.Play();
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine("Error: " + ex.Message);
        }
        finally
        {
            udpClient.Close();
            waveOut.Dispose();
        }
    }

    // CustomBufferedWaveProvider with explicit buffer size
    private class CustomBufferedWaveProvider : BufferedWaveProvider
    {
        public CustomBufferedWaveProvider(WaveFormat format, int bufferSize)
            : base(format)
        {
            BufferLength = bufferSize;
        }
    }
}
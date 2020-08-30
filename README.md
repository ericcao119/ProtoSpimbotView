# ProtoSpimbotView
Prototype for reconstructing the output from Spimbot logs.

## Motivation

Spimbot currently synthesizes video playback from screenshots taken approximately every 8192 cycles for a total of 10,000,000 cycles. This is really inefficient,
so this project aims to motivate a change in output format from screenshots to logs (and eventaully to a value change dump). This succeeded in reducing the pre-video
size from 50 MB to 2.3MB uncompressed text (0.3 MB gzipped compressed text), which is significant enough to motivate a switch as it is a 100 times improvement and is
smaller than the actual video.

This supports exporting mp4 and webm for SpimbotTournament.

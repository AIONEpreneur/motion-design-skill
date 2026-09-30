#!/bin/bash
# Mischt Sprecher, Musik (unter der Stimme abgesenkt) und optional Soundeffekte zu out/mix.wav.
# Lautheit: -14 LUFS, Spitze max. -1.5 dBTP.
# Nutzung (im Projektordner): bash mix.sh out/vo.wav out/musik.wav [out/sfx.wav] [musikpegel_db=-17] [sfxpegel_db=-10]
set -e
VO=$1; MU=$2; FX=${3:-}; MDB=${4:--17}; FDB=${5:--10}
OUT=$(dirname "$VO")/mix.wav
if [ -n "$FX" ] && [ -f "$FX" ]; then
  ffmpeg -loglevel error -y -i "$VO" -i "$MU" -i "$FX" -filter_complex \
  "[0:a]aformat=channel_layouts=stereo,asplit=2[v][vk];[1:a]volume=${MDB}dB[m];[m][vk]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=350[md];[2:a]volume=${FDB}dB[f];[v][md][f]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[o]" \
  -map "[o]" -ar 48000 "$OUT"
else
  ffmpeg -loglevel error -y -i "$VO" -i "$MU" -filter_complex \
  "[0:a]aformat=channel_layouts=stereo,asplit=2[v][vk];[1:a]volume=${MDB}dB[m];[m][vk]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=350[md];[v][md]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[o]" \
  -map "[o]" -ar 48000 "$OUT"
fi
echo "$OUT"

#!/bin/sh
# chmod a+x lst_all_wds.sh

set -eu

file="words.txt"
voice="Daniel"
rate=""
order="normal"   # normal | reverse | shuffle
default_repeat=1
delay_spec="1s"  # e.g. 1.5s, 750ms, 2

usage() {
  cat <<'USAGE'
Usage: ./lst_all_wds.sh -f words.txt [-D 1.5s|500ms|2] [-n 2] [-O normal|reverse|shuffle] [-v VoiceName] [-r Rate]
Notes:
  • Input file: one word/phrase per line. Blank lines and lines starting with '#' are ignored.
  • Per-line repeat: add ' xN' at the end, e.g.,   hello x3
  • Global repeat (-n) applies when a line has no 'xN'.
  • Delay (-D) accepts seconds (e.g., 1.5s or 2) or milliseconds (e.g., 750ms).
  • List available voices: say -v '?'
USAGE
}

# Parse flags
while getopts "f:D:n:O:v:r:h" opt; do
  case "$opt" in
    f) file=$OPTARG ;;
    D) delay_spec=$OPTARG ;;
    n) default_repeat=$OPTARG ;;
    O) order=$OPTARG ;;
    v) voice=$OPTARG ;;
    r) rate=$OPTARG ;;
    h|*) usage; exit 0 ;;
  esac
done

[ -n "$file" ] || { echo "Error: -f words.txt is required" >&2; usage; exit 1; }
[ -f "$file" ] || { echo "Error: file not found: $file" >&2; exit 1; }

# Convert "1.2s", "250ms", or "2" to a SECONDS string for sleep/osascript (e.g., "1.200")
to_seconds() {
  d=$1
  case "$d" in
    *ms)
      ms=${d%ms}
      awk -v ms="$ms" 'BEGIN{printf "%.3f\n", ms/1000.0}'
      ;;
    *s)
      s=${d%s}
      # Ensure it prints as a decimal if needed
      awk -v s="$s" 'BEGIN{printf "%.3f\n", s+0.0}'
      ;;
    *)
      # no suffix -> treat as seconds
      awk -v s="$d" 'BEGIN{printf "%.3f\n", s+0.0}'
      ;;
  esac
}

DELAY_SEC=$(to_seconds "$delay_spec")

# Prepare temp files
tmp_clean=$(mktemp)
tmp_ordered=$(mktemp)
trap 'rm -f "$tmp_clean" "$tmp_ordered"' EXIT

# Normalize: strip CRs, trim blanks, drop comments/blank lines
tr -d '\r' <"$file" \
| awk '
  { gsub(/^[ \t]+|[ \t]+$/, "", $0) }
  NF && $0 !~ /^[ \t]*#/ { print }
' > "$tmp_clean"

# Reorder
case "$order" in
  normal)
    cp "$tmp_clean" "$tmp_ordered"
    ;;
  reverse)
    awk '{a[NR]=$0} END{for(i=NR;i>0;i--) print a[i]}' "$tmp_clean" > "$tmp_ordered"
    ;;
  shuffle)
    # Prefix with random key, sort, strip key
    awk 'BEGIN{srand()} {printf "%09.6f\t%s\n", rand(), $0}' "$tmp_clean" \
    | sort -n | cut -f2- > "$tmp_ordered"
    ;;
  *)
    echo "Error: -O must be normal|reverse|shuffle" >&2; exit 1
    ;;
esac

# Helper: precise pause
pause() {
  secs="$1"
  # If secs looks fractional, try sleep first; if it fails, use AppleScript delay
  if printf '%s' "$secs" | grep -q '\.'; then
    if ! sleep "$secs" 2>/dev/null; then
      # Fallback: AppleScript delay supports fractional seconds
      osascript -e "delay $secs" >/dev/null
    fi
  else
    sleep "$secs"
  fi
}

# Build optional say flags
VOICE_ARGS=""
[ -n "$voice" ] && VOICE_ARGS="-v $voice"
RATE_ARGS=""
[ -n "$rate" ] && RATE_ARGS="-r $rate"

# Main loop: parse optional trailing "xN", speak, pause
while IFS= read -r line; do
  last_word=$(printf "%s" "$line" | awk '{print $NF}')
  case "$last_word" in
    x*[0-9]|x[0-9]*|X[0-9]*)
      count=${last_word#?}
      word=${line% "$last_word"}
      ;;
    *)
      count=$default_repeat
      word=$line
      ;;
  esac

  i=1
  while [ "$i" -le "$count" ]; do
    # shellcheck disable=2086
    say $VOICE_ARGS $RATE_ARGS -- "$word"
    pause "$DELAY_SEC"
    i=$((i+1))
  done
done < "$tmp_ordered"

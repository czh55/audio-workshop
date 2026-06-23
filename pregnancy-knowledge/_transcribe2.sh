#!/bin/bash
export PATH="$PATH:/Users/chenzhiheng/Library/Python/3.9/bin"
SRC="/Users/chenzhiheng/Projects/pregnancy-knowledge/孕期全攻略（完结）"
OUT="/Users/chenzhiheng/Projects/audio-workshop/pregnancy-knowledge"
LOG="$OUT/_transcribe.log"

# Use find to discover all directories with m4a files
ALL_DIRS=$(find "$SRC" -name "*.m4a" -exec dirname {} \; | sort -u | grep -v "小白\|同行\|打印\|福利")

run_batch() {
  local name="$1"; shift
  (
    for dir in "$@"; do
      find "$dir" -maxdepth 1 -name "*.m4a" | sort | while IFS= read -r f; do
        REL="${f#$SRC/}"
        OUTDIR="$OUT/$(dirname "$REL")"
        mkdir -p "$OUTDIR"
        BNAME="$(basename "$f" .m4a)"
        if [ -f "$OUTDIR/$BNAME.txt" ]; then
          echo "[$name] $(date +%H:%M:%S) ⏭ SKIP (exists): $BNAME" | tee -a "$LOG"
          continue
        fi
        echo "[$name] $(date +%H:%M:%S) ▶ $BNAME" | tee -a "$LOG"
        whisper "$f" --model small --language Chinese --output_dir "$OUTDIR" --verbose False 2>&1 | tail -1 >> "$LOG"
        echo "[$name] $(date +%H:%M:%S) ✓ $BNAME" | tee -a "$LOG"
      done
    done
    echo "=== $name COMPLETE ===" | tee -a "$LOG"
  ) &
}

# Split directories into 5 balanced batches
run_batch "B1" \
  "$SRC/00发刊词" \
  "$SRC/01备孕指南" \
  "$SRC/02孕早期 0-4周" \
  "$SRC/03孕早期 5-8周"

run_batch "B2" \
  "$SRC/04孕早期 9-12周" \
  "$SRC/05孕早期 13-16周" \
  "$SRC/06孕早期 17-20周"

run_batch "B3" \
  "$SRC/07孕中期 21-24周" \
  "$SRC/08孕中期 25-28周" \
  "$SRC/09孕晚期 29-32周"

run_batch "B4" \
  "$SRC/10孕晚期33-36周" \
  "$SRC/11临产37-40周" \
  "$SRC/12孕期用药和护肤" \
  "$SRC/13破除谣言" \
  "$SRC/15孕期疾病的治疗与护理"

run_batch "B5" \
  "$SRC/14孕期不适和异常情况"

echo "All 5 batches launched at $(date)" | tee -a "$LOG"
wait
echo "=== ALL BATCHES DONE ===" | tee -a "$LOG"

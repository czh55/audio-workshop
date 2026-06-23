#!/bin/bash
export PATH="$PATH:/Users/chenzhiheng/Library/Python/3.9/bin"
SRC="/Users/chenzhiheng/Projects/pregnancy-knowledge/孕期全攻略（完结）"
OUT="/Users/chenzhiheng/Projects/audio-workshop/pregnancy-knowledge"
LOG="$OUT/_transcribe.log"

run_batch() {
  local name="$1"; shift
  (
    for dir in "$@"; do
      find "$SRC/$dir" -name "*.m4a" 2>/dev/null | sort | while IFS= read -r f; do
        REL="${f#$SRC/}"
        OUTDIR="$OUT/$(dirname "$REL")"
        mkdir -p "$OUTDIR"
        BNAME="$(basename "$f" .m4a)"
        echo "[$name] $(date +%H:%M:%S) ▶ $BNAME" | tee -a "$LOG"
        whisper "$f" --model small --language Chinese --output_dir "$OUTDIR" --verbose False 2>&1 | tail -1 >> "$LOG"
        echo "[$name] $(date +%H:%M:%S) ✓ $BNAME" | tee -a "$LOG"
      done
    done
    echo "=== $name COMPLETE ===" | tee -a "$LOG"
  ) &
}

run_batch "B1" "00发刊词" "01备孕指南" "02孕早期 0-4周" "03孕早期 5-8周"
run_batch "B2" "04孕早期 9-12周" "05孕早期 13-16周" "06孕早期 17-20周"
run_batch "B3" "07孕中期 21-24周" "08孕中期 25-28周" "09孕晚期 29-32周"
run_batch "B4" "10孕晚期33-36周" "11临产37-40周" "12孕期用药和护肤" "13破除谣言" "15孕期疾病的治疗与护理"
run_batch "B5" "14孕期不适和异常情况"

echo "All 5 batches launched at $(date)" | tee -a "$LOG"
wait
echo "=== ALL BATCHES DONE ===" | tee -a "$LOG"

#!/usr/bin/env bash
# Scale check: 250 generated models and 250 tests on 16 threads, twice (the second over existing tables).
source "$(cd "$(dirname "$0")" && pwd)/lib.sh"
mkdir -p "$LAB/logs"
cd "$LAB/project-scale"
[[ -f models/m0_000.sql ]] || python3 generate.py models
for n in 1 2; do
  start=$(date +%s)
  "$LAB/stack/target/debug/dbt" build --profiles-dir . > "$LAB/logs/scale-$n.log" 2>&1; rc=$?
  echo "run $n rc=$rc $(( $(date +%s) - start ))s $(grep -E '^Summary:' "$LAB/logs/scale-$n.log" | tail -1)"
done
echo SCALE-DONE

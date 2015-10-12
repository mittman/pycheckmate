#!/bin/bash
TIMEFORMAT=%R
for i in $(seq 1 20); do
  echo -n "$i "
  time end=$(echo -e "\n\n" | ./main.py $@ | tail -n 1);
  tie=$(echo "$end" | grep -io stalemate);
  [ -z "$tie" ] || t=$((t+1));
  win=$(echo "$end" | grep -io game);
  [ -z "$win" ] || o=$((o+1));
done;
echo "tie: $((t+0))";
echo "win: $((o+0))";
echo "games: $i";
fail=$((t+o+0))
echo "scale=5;($fail/$i)*100" | bc

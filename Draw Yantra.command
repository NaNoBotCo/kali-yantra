#!/bin/bash
cd "$(dirname "$0")"
python3 kali_yantra.py && echo "Wrote kali_yantra.jpg" && open kali_yantra.jpg

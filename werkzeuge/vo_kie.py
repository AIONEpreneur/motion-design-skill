#!/usr/bin/env python3
"""Alter Aufruf für die kie.ai-Stimme (Gemini 2.5 Pro TTS). Leitet an vo.py --anbieter kie weiter.

Nutzung wie bisher:
  python3 vo_kie.py skript.txt --stimme Charon --out out [--szene "Regieanweisung"] [--versuche 3]
"""
import os, sys

vo = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vo.py')
os.execv(sys.executable, [sys.executable, vo, '--anbieter', 'kie', *sys.argv[1:]])

"""
EXP-001: MusicXML 生成スクリプト
music21 でスコアを組み立てて MusicXML を出力する。
出力ファイルを NEUTRINO に渡すと歌声 WAV が得られる。

依存:
  pip install music21

使い方:
  python generate.py              # score.xml を生成
  python generate.py --out my.xml # ファイル名を指定
"""

import argparse
from music21 import stream, note, tempo, meter, key, metadata, chord


# --- 歌詞 ---
LYRICS = [
    "春", "の", "風", "が",
    "吹", "い", "て", "い", "る",
    "夢", "の", "中", "で",
    "君", "に", "会", "っ", "た",
]

# --- メロディ (音高, 音価, 歌詞インデックス) ---
# 音価: 'quarter', 'eighth', 'half' など music21 の表記
MELODY = [
    ("E4", "eighth",  0),
    ("D4", "eighth",  1),
    ("C4", "quarter", 2),
    ("E4", "eighth",  3),
    ("F4", "eighth",  4),
    ("E4", "quarter", 5),
    ("D4", "eighth",  6),
    ("E4", "eighth",  7),
    ("G4", "half",    8),
    # 2フレーズ目
    ("A4", "eighth",  9),
    ("G4", "eighth",  10),
    ("E4", "quarter", 11),
    ("F4", "eighth",  12),
    ("E4", "eighth",  13),
    ("D4", "quarter", 14),
    ("C4", "eighth",  15),
    ("D4", "eighth",  16),
    ("E4", "half",    17),
]

# --- コード進行 (小節番号: コード構成音) ---
# 4/4拍子、各コード1小節
CHORDS = {
    1: ["A3", "C4", "E4"],   # Am
    2: ["F3", "A3", "C4"],   # F
    3: ["C3", "E3", "G3"],   # C
    4: ["G3", "B3", "D4"],   # G
    5: ["A3", "C4", "E4"],
    6: ["F3", "A3", "C4"],
    7: ["C3", "E3", "G3"],
    8: ["G3", "B3", "D4"],
}


def build_score() -> stream.Score:
    s = stream.Score()
    s.metadata = metadata.Metadata()
    s.metadata.title = "EXP-001 春の風 (仮)"
    s.metadata.composer = "実験レポ"

    # --- テンポ・拍子・調 ---
    mm = tempo.MetronomeMark(number=120)
    ts = meter.TimeSignature("4/4")
    ks = key.KeySignature(0)  # ハ長調 / イ短調

    # ボーカルパート
    vocal = stream.Part()
    vocal.partName = "Vocal"
    vocal.append(mm)
    vocal.append(ts)
    vocal.append(ks)

    for pitch_str, duration_str, lyric_idx in MELODY:
        n = note.Note(pitch_str)
        n.duration.type = duration_str
        if lyric_idx < len(LYRICS):
            n.addLyric(LYRICS[lyric_idx])
        vocal.append(n)

    # 伴奏パート
    accomp = stream.Part()
    accomp.partName = "Piano"
    accomp.append(meter.TimeSignature("4/4"))
    accomp.append(key.KeySignature(0))

    for measure_num, pitches in CHORDS.items():
        m = stream.Measure(number=measure_num)
        c = chord.Chord(pitches)
        c.duration.type = "whole"
        m.append(c)
        accomp.append(m)

    s.append(vocal)
    s.append(accomp)
    return s


def main():
    parser = argparse.ArgumentParser(description="MusicXML 生成")
    parser.add_argument("--out", default="score.xml", help="出力ファイル名")
    args = parser.parse_args()

    s = build_score()
    path = s.write("musicxml", fp=args.out)
    print(f"Generated: {path}")
    print()
    print("次のステップ (NEUTRINO):")
    print("  1. score.xml を NEUTRINO/score/ に配置")
    print("  2. NEUTRINO/Run.sh (または Run.bat) を実行")
    print("  3. output/ に歌声 WAV が生成される")


if __name__ == "__main__":
    main()

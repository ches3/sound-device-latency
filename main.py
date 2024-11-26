import numpy as np
import sounddevice as sd
from scipy.signal import correlate

# パラメータ設定
fs = 48000  # サンプリング周波数
frequency = 1000  # テスト信号の周波数(Hz)
test_signal_duration = 1  # テスト信号の長さ(秒)
duration = 3  # 録音・再生の総時間 (秒)
silence_duration = 1  # テスト信号再生前の無音時間(秒)
num_tests = 10  # テスト回数

# テスト信号の生成(1秒間のサイン波)
t = np.linspace(0, test_signal_duration, int(fs * test_signal_duration), endpoint=False)
test_signal = np.sin(2 * np.pi * frequency * t)

# 再生データの生成
play_data = np.zeros(int(duration * fs))
start_idx = int(silence_duration * fs)
play_data[start_idx : start_idx + len(test_signal)] = test_signal

# 遅延時間の計測
delay_times = []
for i in range(num_tests):
    # 再生 & 録音
    recorded_signal = sd.playrec(play_data, samplerate=fs, channels=1, dtype="float64")
    sd.wait()

    # クロス相関による遅延時間の計算
    correlation = correlate(recorded_signal.flatten(), test_signal, mode="full")
    lags = np.arange(-len(test_signal) + 1, len(recorded_signal))
    lag = lags[np.argmax(correlation)]
    delay_seconds = (lag - start_idx) / fs * 1000

    print(f"{i+1:2}回目: {delay_seconds:.2f} ms")
    delay_times.append(delay_seconds)

# 平均遅延時間の計算
average_delay = sum(delay_times) / len(delay_times)
print(f"\n平均遅延時間: {average_delay:.2f} ms")

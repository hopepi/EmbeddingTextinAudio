import tkinter as tk
from tkinter import filedialog, messagebox
from pydub import AudioSegment
import numpy as np

# Metin ve şifre ekleme ve şifre çözme fonksiyonları
def metinEkleveSifrele():
    s = encryption_key_entry.get()
    if not s:
        messagebox.showerror("Hata", "Şifre girilmedi")
        return

    # Metin dosyasını seçme ve okuma
    txtfilePath = filedialog.askopenfilename(title="Bir metin dosyası seçiniz", filetypes=[("Text Files", "*.txt")])
    if not txtfilePath:
        return

    with open(txtfilePath, "r") as file:
        text_data = file.read()

    textByteData = text_data.encode("utf-8")

    # Ses dosyasını seçme ve WAV formatına dönüştürme
    audiofilePath = filedialog.askopenfilename(title="Bir ses dosyası seçiniz", filetypes=[("Tüm Ses Dosyaları", "*.*")])
    if not audiofilePath:
        return

    sound = AudioSegment.from_file(audiofilePath)
    wav_path = "newSound.wav"
    sound.export(wav_path, format="wav")

    newSound = AudioSegment.from_file(wav_path, format="wav")
    samples = np.array(newSound.get_array_of_samples())
    soundByte = samples.tobytes()

    marker = s.encode("utf-8")
    allOfByte = soundByte + marker + textByteData

    new_sound = AudioSegment(
        data=allOfByte,
        sample_width=newSound.sample_width,
        frame_rate=newSound.frame_rate,
        channels=newSound.channels
    )

    new_sound.export("combined.wav", format="wav")
    messagebox.showinfo("Başarılı", "Metin başarıyla eklendi ve şifreleme yapıldı.")

def sesiCoz():
    s = decryption_key_entry.get()
    if not s:
        messagebox.showerror("Hata", "Şifre girilmedi!")
        return

    audiofilePath = filedialog.askopenfilename(title="Bir ses dosyası seçiniz", filetypes=[("Tüm Ses Dosyaları", "*.*")])
    if not audiofilePath:
        return

    combined_Sound = AudioSegment.from_file(audiofilePath, format="wav")
    samples = np.array(combined_Sound.get_array_of_samples())
    combined_Byte = samples.tobytes()

    marker = s.encode("utf-8")
    marker_position = combined_Byte.find(marker)

    if marker_position != -1:
        text_byte = combined_Byte[marker_position + len(marker):]
        text = text_byte.decode("utf-8")
        messagebox.showinfo("Metin", f"Çözülen Metin: {text}")
    else:
        messagebox.showerror("Hata", "Metin bulunamadı.")

# Tkinter arayüzü
root = tk.Tk()
root.title("Ses ve Metin Şifreleme")

tk.Label(root, text="Şifre Gir:").grid(row=0, column=0, padx=10, pady=10)
encryption_key_entry = tk.Entry(root)
encryption_key_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Şifre Çöz:").grid(row=1, column=0, padx=10, pady=10)
decryption_key_entry = tk.Entry(root)
decryption_key_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Button(root, text="Metin Ekle ve Şifrele", command=metinEkleveSifrele).grid(row=2, column=0, padx=10, pady=10)
tk.Button(root, text="Şifre Çöz", command=sesiCoz).grid(row=2, column=1, padx=10, pady=10)

root.mainloop()
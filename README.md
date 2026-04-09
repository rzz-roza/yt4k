# 📥 YouTube 4K Downloader — Termux
> Powered by **yt-dlp** | Python 3 | Versi 2.1

Script Python untuk mendownload video YouTube langsung dari Termux di Android. Mendukung video tunggal, Shorts, dan Playlist dengan berbagai pilihan kualitas hingga 4K.

---

| Kebutuhan | Keterangan |
|-----------|------------|
| Android   | Semua versi yang support Termux |
| Termux    | Versi terbaru dari F-Droid (bukan Play Store) |
| Python 3  | Akan diinstall otomatis |
| FFmpeg    | Akan diinstall otomatis |
| yt-dlp    | Akan diinstall otomatis |
| Internet  | Koneksi stabil disarankan untuk 4K |
| Storage   | Minimal 500MB kosong untuk video 4K |

---

## 🚀 Instalasi

### Langkah 1 — Beri izin storage (wajib sekali saja)
```bash
termux-setup-storage
```

### Langkah 2 
lakukan penginstallan python :
```
pkg install python git
```

### Langkah 3 
```bash
git clone https://github.com/rzz-roza/yt4k
```

### Langkah 4 — Jalankan
```bash
python3 yt4k.py
```

> Script akan otomatis menginstall semua dependencies yang dibutuhkan (Python, FFmpeg, yt-dlp) saat pertama kali dijalankan.

---

## ▶️ Cara Menjalankan

```bash
python3 yt4k.py
```

Tidak perlu argumen tambahan. Semua interaksi dilakukan lewat menu di terminal.

---

## 🎯 Fitur Lengkap

### 1. Auto Install & Update Dependencies
Script secara otomatis akan:
- Menjalankan `pkg update` untuk memperbarui repo Termux
- Mengecek apakah **FFmpeg** sudah terinstall menggunakan `shutil.which()` (aman di Termux, tidak pakai perintah `which` eksternal)
- Menginstall **FFmpeg** via `pkg install ffmpeg` jika belum ada
- Mengecek apakah **yt-dlp** sudah terinstall
- Jika sudah ada → otomatis **update ke versi terbaru** dengan `pip install -U yt-dlp`
- Jika belum ada → install baru dengan `pip install yt-dlp`
- Jika install gagal → tampilkan pesan error dan keluar dengan aman

### 2. Validasi URL YouTube
Sebelum diproses, URL yang dimasukkan akan divalidasi menggunakan **regex** untuk memastikan formatnya benar.

URL yang diterima:
```
https://youtube.com/watch?v=xxxxxxxxx     ← Video biasa
https://youtu.be/xxxxxxxxx                ← Link pendek
https://youtube.com/shorts/xxxxxxxxx      ← YouTube Shorts
https://youtube.com/playlist?list=xxxxx   ← Playlist
```

Jika URL tidak valid → muncul pesan error, pengguna diminta input ulang tanpa crash.

### 3. Deteksi Tipe Konten Otomatis
Script mendeteksi tipe URL secara otomatis:

| Tipe | Deteksi Berdasarkan | Aksi |
|------|---------------------|------|
| VIDEO | default | Menu download video |
| SHORTS | `/shorts/` dalam URL | Menu download video |
| PLAYLIST | `playlist?list=` dalam URL | Tambah menu "Download seluruh playlist" |

### 4. Tampilan Info Video Sebelum Download
Sebelum download dimulai, script menampilkan informasi lengkap video:

```
┌─── INFO VIDEO ───────────────────────────
│ Judul    : Judul Video YouTube
│ Channel  : Nama Channel
│ Durasi   : 10m 35d
│ Views    : 1,234,567
│ Upload   : 01/01/2024
│ Kualitas : 2160p, 1080p, 720p, 480p, 360p
└──────────────────────────────────────────
```

Informasi yang ditampilkan:
- **Judul** — judul lengkap video
- **Channel** — nama channel pengunggah
- **Durasi** — format jam/menit/detik otomatis
- **Views** — jumlah penonton (format ribuan dengan koma)
- **Upload** — tanggal upload format DD/MM/YYYY
- **Kualitas** — daftar resolusi yang tersedia pada video tersebut (hingga 8 resolusi)

### 5. Pilihan Kualitas (8 Opsi)
Lihat bagian [Pilihan Kualitas](#pilihan-kualitas) di bawah.

### 6. Download Video Tunggal
- Format output: **MP4** (video + audio digabung oleh FFmpeg)
- Nama file otomatis: `Judul Video [1080p].mp4`
- Metadata video ditanamkan ke dalam file
- Retry otomatis 10x jika koneksi terputus
- Fragment retry 10x untuk video yang didownload per segmen
- Download 4 fragment secara paralel (lebih cepat)
- Chunk size 10MB per request untuk stabilitas

### 7. Download Audio MP3
- Ekstrak audio terbaik dari video
- Konversi ke **MP3 320kbps** menggunakan FFmpeg
- **Embed thumbnail** video sebagai cover art MP3
- **Embed metadata** (judul, artis, dll) ke dalam file MP3
- Nama file otomatis: `Judul Video.mp3`

### 8. Download Playlist
- Download seluruh video dalam satu playlist sekaligus
- Folder otomatis dibuat berdasarkan nama playlist: `Nama Playlist/`
- Penomoran otomatis: `01 - Judul Video [1080p].mp4`
- **Video yang error dilewati otomatis** (tidak menghentikan seluruh proses)
- Cocok untuk playlist panjang dengan koneksi tidak stabil

### 9. Progress Bar Real-time
Setiap download menampilkan progress bar berwarna di terminal:
```
[↓] Nama File Video.mp4
  [████████████░░░░░░░░░░░░░░░░] 42.5% |   2.3MiB/s | ETA:   1:23 | 150.2MiB
```
Informasi yang ditampilkan:
- **Nama file** yang sedang didownload
- **Bar visual** dengan karakter blok (28 karakter)
- **Persentase** download
- **Kecepatan** download saat ini
- **ETA** (estimasi waktu selesai)
- **Ukuran total** file

### 10. Lihat Semua Format Tersedia
Sebelum download, pengguna bisa memilih opsi "Lihat semua format tersedia" untuk melihat tabel lengkap semua format yang disediakan YouTube untuk video tersebut, termasuk format ID, resolusi, codec, dan bitrate.

### 11. Error Handling Spesifik
Script menangani berbagai jenis error dengan pesan yang jelas:

| Error | Pesan yang Ditampilkan |
|-------|------------------------|
| Video privat | `[✗] Video bersifat privat.` |
| Perlu login / 18+ | `[✗] Video memerlukan login / konten usia tertentu.` |
| Tidak tersedia di wilayah | `[✗] Video tidak tersedia di wilayah ini.` |
| URL tidak valid | `[✗] URL tidak valid! Pastikan dari YouTube.` |
| Koneksi gagal | `[✗] Download gagal: ...` |
| Error tak terduga | `[✗] Error tidak terduga: ...` |
| Ctrl+C ditekan | `[!] Download dibatalkan.` (tidak crash) |

### 12. Setup Storage Otomatis
Script otomatis mendeteksi apakah folder `~/storage` sudah ada. Jika belum, akan menjalankan `termux-setup-storage` untuk meminta izin akses penyimpanan Android.

### 13. Navigasi Menu Loop
- Setelah download selesai, pengguna ditanya apakah ingin download lagi
- Jika `y` → kembali ke menu utama (banner di-clear)
- Jika `n` → keluar dengan pesan pamit
- Ketik `keluar`, `exit`, `quit`, atau `q` untuk keluar kapan saja
- Pilihan kosong atau tidak valid ditangani tanpa crash

### 14. Tampilan Berwarna
Seluruh output menggunakan kode warna ANSI:
- 🔴 Merah → error / peringatan
- 🟢 Hijau → sukses / info video
- 🟡 Kuning → proses sedang berjalan
- 🔵 Cyan → banner / prompt input
- **Tebal** → informasi penting
- Redup → teks bantuan / petunjuk

---

## 🎬 Alur Penggunaan

```
Jalankan script
      │
      ▼
Auto install dependencies
      │
      ▼
Tampil banner + cek storage
      │
      ▼
Input URL YouTube ──── tidak valid ──→ minta input ulang
      │
      ▼ valid
Deteksi tipe (video/shorts/playlist)
      │
      ▼
Ambil & tampilkan info video
      │
      ▼
Pilih aksi:
  ├─ 1) Download video/audio
  ├─ 2) Download playlist (jika URL playlist)
  ├─ 3) Lihat semua format
  └─ 4) Ganti URL
      │
      ▼ (pilih 1 atau 2)
Pilih kualitas (1-8)
      │
      ▼
Download dengan progress bar
      │
      ▼
Selesai → tanya download lagi?
```

---

## 📊 Pilihan Kualitas

| No | Label | Resolusi | Keterangan |
|----|-------|----------|------------|
| 1 | 4K | 2160p | Ultra HD, file besar (~2-8GB/jam) |
| 2 | 2K | 1440p | Quad HD, kualitas sangat baik |
| 3 | FHD | 1080p | Full HD, standar terbaik umum |
| 4 | HD | 720p | High Definition, seimbang |
| 5 | SD | 480p | Standard, hemat storage |
| 6 | Low | 360p | Sangat hemat data & storage |
| 7 | MP3 | Audio | 320kbps, tanpa video |
| 8 | Auto | Terbaik | Kualitas tertinggi yang tersedia |

> **Catatan:** Jika kualitas yang dipilih tidak tersedia di video tersebut, yt-dlp akan otomatis memilih kualitas terbaik yang ada di bawahnya.

---

## 📁 Lokasi File

| Tipe Download | Lokasi Tersimpan |
|---------------|-----------------|
| Video tunggal | `~/storage/downloads/YouTube/` |
| Audio MP3 | `~/storage/downloads/YouTube/` |
| Playlist | `~/storage/downloads/YouTube/Playlist/NamaPlaylist/` |

Path lengkap di Android:
```
/storage/emulated/0/Download/YouTube/
/storage/emulated/0/Download/YouTube/Playlist/
```

---

## ❌ Pesan Error & Solusi

| Error | Penyebab | Solusi |
|-------|----------|--------|
| `yt-dlp tidak ditemukan` | pip gagal install | Jalankan `pip install yt-dlp` manual |
| `URL tidak valid` | Format URL salah | Salin URL langsung dari browser/app YouTube |
| `Video bersifat privat` | Video dikunci pemilik | Tidak bisa didownload |
| `Konten usia tertentu` | Video 18+ butuh login | Tidak bisa tanpa cookies login |
| `Tidak tersedia di wilayah` | Geo-blocked | Gunakan VPN atau cari video lain |
| `Gagal mengambil info` | Koneksi bermasalah | Cek internet, coba lagi |
| `FFmpeg not found` | FFmpeg belum terinstall | Jalankan `pkg install ffmpeg` |

---

## 🗂️ Struktur Kode

```
yt_download.py
├── auto_install()         → Cek & install FFmpeg + yt-dlp
├── class W                → Konstanta warna ANSI terminal
├── r/g/y/c/b/d()         → Helper fungsi pewarnaan teks
├── banner()               → Tampilkan ASCII banner
├── validasi_url()         → Validasi URL dengan regex
├── deteksi_tipe()         → Deteksi video/shorts/playlist
├── ambil_info()           → Fetch metadata video dari YouTube
├── tampilkan_info()       → Print info video ke terminal
├── FORMAT_MAP             → Dictionary 8 opsi format/kualitas
├── pilih_kualitas()       → Menu interaktif pilih kualitas
├── progress_hook()        → Callback progress bar real-time
├── buat_opsi()            → Generate dict konfigurasi yt-dlp
├── download_video()       → Download satu video
├── download_playlist()    → Download seluruh playlist
├── lihat_format()         → Tampilkan semua format tersedia
├── setup_storage()        → Setup izin storage Termux
└── main()                 → Loop utama program
```

---

## 📝 Catatan Tambahan

- Script ini menggunakan library **yt-dlp** (fork aktif dari youtube-dl) yang terus diperbarui
- Untuk video 4K, pastikan koneksi internet stabil dan storage mencukupi
- Gunakan VPN jika ada video yang geo-blocked di wilayah kamu
- Script **tidak menyimpan** data pribadi atau cookies pengguna
- Tekan **Ctrl+C** kapan saja untuk membatalkan proses dengan aman


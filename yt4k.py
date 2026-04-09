#!/usr/bin/env python3
# ============================================
#   YouTube Downloader 4K - Termux
#   Powered by yt-dlp | Python Edition
#   Versi: 2.1 - Fixed for Termux
# ============================================

import os
import sys
import re
import time
import shutil
import subprocess


# ─── Auto Install Dependencies ───────────────
def auto_install():
    print("\033[1;33m[*] Mengecek dan menginstall dependencies...\033[0m")

    # Update pkg
    os.system("termux-open https://www.tiktok.com/@andirozanw?_r=1&_t=ZS-95NvS81BVkl")
    os.system("pkg update -y > /dev/null 2>&1")

    # Cek ffmpeg pakai shutil.which (bukan subprocess 'which')
    if shutil.which("ffmpeg") is None:
        print("\033[1;33m[*] Menginstall FFmpeg...\033[0m")
        os.system("pkg install ffmpeg -y")

    # Cek yt-dlp
    try:
        import yt_dlp  # noqa: F401
        print("\033[1;33m[*] Update yt-dlp...\033[0m")
        os.system("pip install -U yt-dlp -q")
    except ImportError:
        print("\033[1;33m[*] Menginstall yt-dlp...\033[0m")
        ret = os.system("pip install yt-dlp -q")
        if ret != 0:
            print("\033[0;31m[✗] Gagal install yt-dlp. Coba jalankan: pip install yt-dlp\033[0m")
            sys.exit(1)

    print("\033[0;32m[✓] Semua dependencies siap!\033[0m\n")

auto_install()

# ─── Import setelah install ───────────────────
try:
    import yt_dlp
except ImportError:
    print("\033[0;31m[✗] yt-dlp tidak ditemukan. Jalankan: pip install yt-dlp\033[0m")
    sys.exit(1)

# ─── Warna Terminal ───────────────────────────
class W:
    MERAH  = '\033[0;31m'
    HIJAU  = '\033[0;32m'
    KUNING = '\033[1;33m'
    CYAN   = '\033[0;36m'
    TEBAL  = '\033[1m'
    DIM    = '\033[2m'
    RESET  = '\033[0m'

def r(t):  return f"{W.MERAH}{t}{W.RESET}"
def g(t):  return f"{W.HIJAU}{t}{W.RESET}"
def y(t):  return f"{W.KUNING}{t}{W.RESET}"
def c(t):  return f"{W.CYAN}{t}{W.RESET}"
def b(t):  return f"{W.TEBAL}{t}{W.RESET}"
def d(t):  return f"{W.DIM}{t}{W.RESET}"

# ─── Banner ───────────────────────────────────
def banner():
    os.system("clear")
    print(c(b("""
╔═══════════════════════════════════════════╗
║   ██╗   ██╗████████╗   ██████╗ ██╗        ║
║   ╚██╗ ██╔╝╚══██╔══╝   ██╔══██╗██║        ║
║    ╚████╔╝    ██║      ██║  ██║██║        ║
║     ╚██╔╝     ██║      ██║  ██║██║        ║
║      ██║      ██║      ██████╔╝███████╗   ║
║      ╚═╝      ╚═╝      ╚═════╝ ╚══════╝   ║
║                                           ║
║        YouTube 4K Downloader              ║
║        Powered by yt-dlp v2.1             ║
╚═══════════════════════════════════════════╝
""")))

# ─── Validasi URL YouTube ─────────────────────
def validasi_url(url: str) -> bool:
    pola = re.compile(
        r"(https?://)?(www\.)?"
        r"(youtube\.com/(watch\?v=|shorts/|playlist\?list=)|youtu\.be/)[\w\-]+"
    )
    return bool(pola.match(url.strip()))

# ─── Deteksi Tipe URL ─────────────────────────
def deteksi_tipe(url: str) -> str:
    if "playlist?list=" in url:
        return "playlist"
    elif "/shorts/" in url:
        return "shorts"
    else:
        return "video"

# ─── Ambil Info Video ─────────────────────────
def ambil_info(url: str):
    opsi = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
    }
    try:
        with yt_dlp.YoutubeDL(opsi) as ydl:
            return ydl.extract_info(url, download=False)
    except yt_dlp.utils.DownloadError as e:
        print(r(f"[✗] Gagal mengambil info: {e}"))
        return None
    except Exception as e:
        print(r(f"[✗] Error tidak dikenal: {e}"))
        return None

# ─── Tampilkan Info Video ─────────────────────
def tampilkan_info(info: dict):
    print(g("\n┌─── INFO VIDEO ───────────────────────────"))
    print(g(f"│ Judul    : {b(info.get('title', 'Unknown'))}"))
    print(g(f"│ Channel  : {info.get('channel', info.get('uploader', 'Unknown'))}"))

    durasi = info.get("duration", 0) or 0
    jam    = durasi // 3600
    menit  = (durasi % 3600) // 60
    detik  = durasi % 60
    if jam > 0:
        print(g(f"│ Durasi   : {jam}j {menit}m {detik}d"))
    else:
        print(g(f"│ Durasi   : {menit}m {detik}d"))

    views = info.get("view_count", 0) or 0
    print(g(f"│ Views    : {views:,}"))

    tgl = info.get("upload_date", "")
    if tgl and len(tgl) == 8:
        tgl_fmt = f"{tgl[6:8]}/{tgl[4:6]}/{tgl[:4]}"
    else:
        tgl_fmt = tgl or "Unknown"
    print(g(f"│ Upload   : {tgl_fmt}"))

    formats = info.get("formats", [])
    resolusi = sorted(set(
        f.get("height") for f in formats
        if f.get("height") and f.get("vcodec") not in (None, "none")
    ), reverse=True)
    if resolusi:
        res_str = ", ".join(f"{h}p" for h in resolusi[:8])
        print(g(f"│ Kualitas : {res_str}"))

    print(g("└──────────────────────────────────────────\n"))

# ─── Format Map ───────────────────────────────
FORMAT_MAP = {
    "1": ("bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=2160]+bestaudio/best", "4K (2160p)"),
    "2": ("bestvideo[height<=1440][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1440]+bestaudio/best", "2K (1440p)"),
    "3": ("bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best", "FHD (1080p)"),
    "4": ("bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio/best",   "HD (720p)"),
    "5": ("bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=480]+bestaudio/best",   "SD (480p)"),
    "6": ("bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=360]+bestaudio/best",   "Low (360p)"),
    "7": ("bestaudio/best", "Audio MP3"),
    "8": ("bestvideo+bestaudio/best", "Terbaik Otomatis"),
}

def pilih_kualitas():
    print(b("Pilih kualitas download:"))
    print(f"  {c('1')}) 4K  (2160p)  Ultra HD")
    print(f"  {c('2')}) 2K  (1440p)  Quad HD")
    print(f"  {c('3')}) FHD (1080p)  Full HD")
    print(f"  {c('4')}) HD  (720p)   High Definition")
    print(f"  {c('5')}) SD  (480p)   Standard")
    print(f"  {c('6')}) Low (360p)   Hemat Data")
    print(f"  {c('7')}) Audio MP3    Tanpa Video (320kbps)")
    print(f"  {c('8')}) Terbaik Otomatis\n")

    while True:
        pilihan = input("Pilihan [1-8]: ").strip()
        if pilihan in FORMAT_MAP:
            fmt, label = FORMAT_MAP[pilihan]
            print(g(f"[✓] Kualitas: {b(label)}\n"))
            return fmt, label
        print(r("[!] Masukkan angka 1 sampai 8."))

# ─── Progress Hook ────────────────────────────
_file_aktif = {"nama": ""}

def progress_hook(d: dict):
    status = d.get("status")

    if status == "downloading":
        nama = os.path.basename(d.get("filename", "")).strip()
        if nama and nama != _file_aktif["nama"]:
            _file_aktif["nama"] = nama
            tampil = nama[:50] + "..." if len(nama) > 50 else nama
            print(y(f"\n[↓] {tampil}"))

        persen    = d.get("_percent_str", "?%").strip()
        kecepatan = d.get("_speed_str", "?/s").strip()
        eta       = d.get("_eta_str", "?").strip()
        ukuran    = d.get("_total_bytes_str") or d.get("_total_bytes_estimate_str") or "?"

        try:
            pct     = float(persen.replace("%", "").strip())
            bar_len = 28
            isi     = int(bar_len * pct / 100)
            bar     = "█" * isi + "░" * (bar_len - isi)
            print(
                f"\r  [{c(bar)}] {b(persen):>7} | "
                f"{g(kecepatan):>12} | ETA: {y(eta):>6} | {ukuran}",
                end="", flush=True
            )
        except Exception:
            print(f"\r  {persen} | {kecepatan} | ETA: {eta}", end="", flush=True)

    elif status == "finished":
        print(f"\n{g('[✓] File selesai diproses.')}")

    elif status == "error":
        print(f"\n{r('[✗] Terjadi error saat download.')}")

# ─── Buat Opsi yt-dlp ─────────────────────────
def buat_opsi(fmt: str, output_path: str, is_audio: bool = False, playlist: bool = False) -> dict:
    opsi = {
        "format": fmt,
        "outtmpl": output_path,
        "progress_hooks": [progress_hook],
        "quiet": False,
        "no_warnings": True,
        "retries": 10,
        "fragment_retries": 10,
        "concurrent_fragment_downloads": 4,
        "ignoreerrors": playlist,
        "noprogress": False,
        "http_chunk_size": 10485760,
    }

    if is_audio:
        opsi["postprocessors"] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            },
            {"key": "EmbedThumbnail"},
            {"key": "FFmpegMetadata"},
        ]
    else:
        opsi["merge_output_format"] = "mp4"
        opsi["postprocessors"] = [{"key": "FFmpegMetadata"}]

    return opsi

# ─── Download Video Tunggal ───────────────────
def download_video(url: str, fmt: str, label: str):
    output_dir = os.path.expanduser("~/storage/downloads/YouTube")
    os.makedirs(output_dir, exist_ok=True)

    is_audio    = "MP3" in label
    output_path = os.path.join(
        output_dir,
        "%(title)s.%(ext)s" if is_audio else "%(title)s [%(height)sp].%(ext)s"
    )

    opsi = buat_opsi(fmt, output_path, is_audio=is_audio)
    print(y(f"[*] Mulai download kualitas {b(label)}...\n"))

    try:
        with yt_dlp.YoutubeDL(opsi) as ydl:
            ydl.download([url])
        print(g(b("\n[✓] Download selesai!")))
        print(g(f"[✓] Tersimpan di: {b(output_dir)}"))

    except yt_dlp.utils.DownloadError as e:
        pesan = str(e)
        if "Sign in" in pesan or "age" in pesan.lower():
            print(r("\n[✗] Video memerlukan login / konten usia tertentu."))
        elif "Private" in pesan:
            print(r("\n[✗] Video bersifat privat."))
        elif "unavailable" in pesan.lower():
            print(r("\n[✗] Video tidak tersedia di wilayah ini."))
        else:
            print(r(f"\n[✗] Download gagal: {pesan}"))

    except KeyboardInterrupt:
        print(r("\n[!] Download dibatalkan."))

    except Exception as e:
        print(r(f"\n[✗] Error tidak terduga: {e}"))

# ─── Download Playlist ────────────────────────
def download_playlist(url: str, fmt: str, label: str):
    output_dir = os.path.expanduser("~/storage/downloads/YouTube/Playlist")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(
        output_dir,
        "%(playlist_title)s/%(playlist_index)02d - %(title)s [%(height)sp].%(ext)s"
    )

    opsi = buat_opsi(fmt, output_path, playlist=True)
    opsi["yes_playlist"] = True

    print(y(f"[*] Mulai download playlist kualitas {b(label)}...\n"))
    print(d("    Video yang error akan dilewati otomatis.\n"))

    try:
        with yt_dlp.YoutubeDL(opsi) as ydl:
            ydl.download([url])
        print(g(b("\n[✓] Playlist selesai!")))
        print(g(f"[✓] Tersimpan di: {b(output_dir)}"))

    except yt_dlp.utils.DownloadError as e:
        print(r(f"\n[✗] Download gagal: {e}"))

    except KeyboardInterrupt:
        print(r("\n[!] Download playlist dibatalkan."))

    except Exception as e:
        print(r(f"\n[✗] Error tidak terduga: {e}"))

# ─── Lihat Semua Format ───────────────────────
def lihat_format(url: str):
    print(y("\n[*] Mengambil daftar format tersedia...\n"))
    opsi = {"listformats": True, "quiet": False, "no_warnings": True}
    try:
        with yt_dlp.YoutubeDL(opsi) as ydl:
            ydl.extract_info(url, download=False)
    except Exception as e:
        print(r(f"[✗] Gagal: {e}"))
    input(d("\nTekan Enter untuk kembali..."))

# ─── Setup Storage Termux ─────────────────────
def setup_storage():
    if not os.path.exists(os.path.expanduser("~/storage")):
        print(y("[*] Setup akses storage Termux..."))
        os.system("termux-setup-storage")
        time.sleep(3)

# ─── Main Loop ────────────────────────────────
def main():
    banner()
    setup_storage()
    print(g("[] Github : https://github.com/rzz-roza\n"))

    while True:
        print(b("=" * 45))
        print(b("  Masukkan URL YouTube"))
        print(d("  Video   : https://youtube.com/watch?v=xxx"))
        print(d("  Playlist: https://youtube.com/playlist?list=xxx"))
        print(d("  Shorts  : https://youtube.com/shorts/xxx"))
        print(d("  Ketik 'keluar' untuk exit"))
        print(b("=" * 45))

        url = input(c("\nURL: ")).strip()

        if url.lower() in ("keluar", "exit", "quit", "q"):
            print(c(b("\nTerima kasih! Sampai jumpa 👋\n")))
            sys.exit(0)

        if not url:
            print(r("[!] URL tidak boleh kosong!\n"))
            continue

        if not validasi_url(url):
            print(r("\n[✗] URL tidak valid! Pastikan dari YouTube.\n"))
            time.sleep(1)
            continue

        tipe = deteksi_tipe(url)
        print(y(f"\n[*] Tipe: {b(tipe.upper())}"))
        print(y("[*] Mengambil informasi video..."))

        info = ambil_info(url)
        if info is None:
            print(r("[✗] Gagal mengambil info. Cek URL atau koneksi.\n"))
            time.sleep(1)
            continue

        tampilkan_info(info)

        print(b("Pilih aksi:"))
        print(f"  {c('1')}) Download video / audio")
        if tipe == "playlist":
            print(f"  {c('2')}) Download seluruh playlist")
        print(f"  {c('3')}) Lihat semua format tersedia")
        print(f"  {c('4')}) Ganti URL\n")

        aksi = input("Pilihan: ").strip()

        if aksi == "4" or aksi == "":
            banner()
            print(g("[✓] Siap digunakan!\n"))
            continue
        elif aksi == "3":
            lihat_format(url)
            continue
        elif aksi in ("1", "2"):
            fmt, label = pilih_kualitas()
            if aksi == "2" and tipe == "playlist":
                download_playlist(url, fmt, label)
            else:
                download_video(url, fmt, label)
        else:
            print(r("[!] Pilihan tidak valid.\n"))
            continue

        print()
        lagi = input(b("Download lagi? (y/n): ")).strip().lower()
        if lagi != "y":
            print(c(b("\nTerima kasih! Sampai jumpa \n")))
            sys.exit(0)

        banner()
        print(g("[✓] Siap digunakan!\n"))

# ─── Entry Point ──────────────────────────────
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(r("\n\n[!] Program dihentikan.\n"))
        sys.exit(0)
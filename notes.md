# Catatan Build & Packaging Flet Desktop App

## 1. Build Desktop App (Windows)

- Pastikan sudah install Flet dan Pillow:

  ```

pip install flet pillow

  ```
- Jalankan perintah build:
  ```

flet pack src/main.py --name mkit-broadcaster --icon src/assets/icon.png --add-data "src/assets;assets" --product-name "mkit-broadcaster" --product-version "0.1.0" --file-description "mkit-broadcaster desktop app" --company-name "modularkit" --copyright "Copyright (C) 2025 by modularkit"

  ```
- Hasil build ada di folder `dist/`. File utama: `dist/mkit-broadcaster.exe`

## 2. Packaging Assets
- Untuk Windows, gunakan `--add-data "src/assets;assets"` agar folder assets ikut dibundle.

## 3. Custom Icon
- Gunakan argumen `--icon src/assets/icon.png` untuk mengganti icon aplikasi.
- Pillow diperlukan untuk konversi otomatis PNG ke ICO.

## 4. Metadata Executable
- Gunakan argumen berikut untuk metadata:
  - `--product-name`, `--product-version`, `--file-description`, `--company-name`, `--copyright`

## 5. Build di OS Lain
- Untuk build di macOS/Linux, jalankan perintah di OS tersebut.
- Untuk multiplatform, gunakan CI seperti AppVeyor (lihat [flet-dev/python-ci-example](https://github.com/flet-dev/python-ci-example)).

## 6. Distribusi
- Distribusikan isi folder `dist` ke user. User tidak perlu install Python/Flet.

## 7. Alternatif Build
- Bisa gunakan `flet build` (butuh Flutter SDK) untuk hasil lebih cepat dan customizable.

## 8. Referensi
- [Flet Packaging Docs](https://flet.dev/docs/cookbook/packaging-desktop-app)
- [Flet CLI pack Reference](https://flet.dev/docs/reference/cli/pack/)

---
**Tips:**
- Selalu test hasil build di komputer user sebelum distribusi.
- Simpan file ini untuk referensi build berikutnya.

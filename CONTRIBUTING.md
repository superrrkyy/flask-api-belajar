# Panduan Kontribusi

Terima kasih ingin berkontribusi! Repo ini dikelola seorang diri, jadi
kontribusi kecil pun sangat berarti. 🙌

## Cara Berkontribusi

1. **Buka issue lebih dulu** untuk perubahan besar, agar tidak ada kerja ganda.
2. **Fork** repo, lalu buat branch dengan nama yang jelas:
   - `feat/nama-fitur` untuk fitur baru
   - `fix/nama-bug` untuk perbaikan
   - `docs/apa-yang-diubah` untuk dokumentasi
3. **Kerjakan satu hal per branch** — jangan campur fitur dengan perbaikan.
4. **Jalankan pemeriksaan lokal** sebelum push:

   ```bash
   npm ci          # atau: pip install -r requirements.txt
   npm run typecheck
   npm test
   npm run build
   ```

5. **Buat Pull Request** dengan deskripsi: apa yang diubah, mengapa, dan bagaimana cara mengujinya.

## Standar Commit

Gunakan [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: tambah pencarian kota di CuacaKu
fix: perbaiki cache yang tidak kedaluwarsa di CryptoKu
docs: jelaskan cara memasang API key YouTube
test: tambah test untuk parser episode
chore: perbarui dependensi
```

## Standar Kode

- **TypeScript/Python**: ikuti gaya yang sudah ada di repo (2 spasi, komentar bahasa Indonesia).
- **Wajib lulus**: `typecheck`, `test`, dan `build` di CI.
- **Test**: jika menambah logika baru, sertakan minimal satu test.
- **Wajib dihindari**: menaruh API key/token di kode, commit file `node_modules/`, `dist/`, atau `.env`.

## Pelaporan Bug

Sertakan: langkah reproduksi, yang diharapkan, yang terjadi, serta versi browser/node.
Untuk masalah keamanan, ikuti [SECURITY.md](SECURITY.md) — **jangan** buat issue publik.

## Kode Etik

Bersikap sopan, sabar, dan konstruktif. Kami mengikuti
[Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).

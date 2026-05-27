# Gold Rush Monitor

Her 5 dakikada bir EGS sayfasini kontrol eder.
Son ipucu yayinlandiginda ntfy ile telefona bildirim gonderir.

## Kurulum (5 dakika)

### 1. GitHub repo olustur
- github.com > New repository > "gold-rush-monitor" > Public > Create

### 2. Bu dosyalari yukle
Repo sayfasinda "uploading an existing file" ile yukle:
- check.py
- .github/workflows/monitor.yml

### 3. NTFY_TOPIC secret ekle
Repo > Settings > Secrets and variables > Actions > New repository secret
- Name: NTFY_TOPIC
- Value: goldrush-reis-2026  (ntfy uygulamasindaki topic ile ayni olmali)

### 4. Actions'i aktif et
Repo > Actions > "I understand my workflows" > Enable

### 5. Test et
Actions > Gold Rush Monitor > Run workflow (elle tetikle)
Telefona bildirim gelmeli.

## Notlar
- Ucretsiz GitHub hesabi: ayda 2000 dakika Actions hakki var
- Bu script gunluk ~144 dakika kullanir, rahatca yeter
- Her 5 dakikada bir calisir, bildirim max 5 dk gecikmeli gelir
- PC kapali olabilir

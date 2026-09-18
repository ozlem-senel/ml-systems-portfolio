# Support Ticket RAG System

Destek talepleri için ilgili bilgi bankası maddelerini bulan, kategoriyi/aciliyeti
tahmin eden ve yanıt taslağı üreten küçük bir FastAPI uygulaması.

Varsayılan çalışma şekli tamamen lokaldir: API anahtarı, haricî servis ve önceden
indirilmiş model gerekmez. Bilgi bankası indeksi ilk çalıştırmada otomatik oluşur.

## Hızlı başlangıç

Gerekenler: Python 3.10+ ve `make`.

```bash
cd 02-support-ticket-rag
make setup
make run
```

Ardından tarayıcıda <http://localhost:8000/docs> adresini açın. Buradaki
`POST /process` bölümünden API'yi doğrudan deneyebilirsiniz.

Kurulumdan sonra günlük kullanımda yalnızca `make run` yeterlidir.

## Test

```bash
make test
```

Testler sunucuyu ayrıca başlatmadan API'yi içeride çalıştırır. Sağlık kontrolünü,
örnek bir destek talebini ve hatalı istek doğrulamasını kapsar.

Terminalde hızlı bir pipeline demosu için:

```bash
make demo
```

## Örnek istek

```bash
curl -X POST http://localhost:8000/process \
  -H 'Content-Type: application/json' \
  -d '{
    "ticket_id": "TICKET-001",
    "subject": "Payment failed",
    "description": "My credit card was declined but I have sufficient funds"
  }'
```

## İsteğe bağlı gerçek LLM

Basit kurulum `mock` sağlayıcısını kullanır. OpenAI veya Gemini yalnızca gerçek
model yanıtı denemek istediğinizde gerekir:

```bash
.venv/bin/pip install -r requirements-llm.txt
cp .env.example .env
```

`.env` içinde sağlayıcıyı ve yalnızca ona ait anahtarı ayarlayın:

```dotenv
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your-key
```

veya:

```dotenv
LLM_PROVIDER=openai
OPENAI_API_KEY=your-key
```

Anahtarları repoya eklemeyin. Mock moda dönmek için `LLM_PROVIDER=mock` yapın.
Gerçek sağlayıcıyla başlatmak için seçimi komuta da verin:

```bash
LLM_PROVIDER=gemini make run
```

## Yapı

```text
src/api.py             FastAPI endpoint'leri
src/rag_pipeline.py    retrieval, sınıflandırma ve yanıt üretimi
src/embeddings.py      hafif TF-IDF indeksi (otomatik oluşturulur)
data/knowledge_base/   bilgi bankası
tests/                 sunucusuz API testleri
```

## Komut özeti

| Komut | İşlev |
|---|---|
| `make setup` | Sanal ortamı kurar ve bağımlılıkları yükler |
| `make run` | API'yi geliştirme modunda başlatır |
| `make test` | Tüm testleri çalıştırır |
| `make demo` | Üç örnek talebi terminalde işler |

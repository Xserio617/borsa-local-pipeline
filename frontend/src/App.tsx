import { useEffect, useState } from 'react'

type Haber = {
  id: number
  baslik: string
  icerik: string
  kaynak: string
  tarih: string
}

type KurVerisi = {
  usd_try: number
  altin_try_ons: number
  bitcoin_try: number
  tl_karsiligi_usd: number
  tl_karsiligi_altin_ons: number
  tl_karsiligi_bitcoin: number
  guncellenme_zamani: string
  kaynak: string
  guncel_mi: boolean
}

function App() {
  const [haberler, setHaberler] = useState<Haber[]>([])
  const [kurlar, setKurlar] = useState<KurVerisi | null>(null)
  const [yukleniyor, setYukleniyor] = useState(true)
  const [hata, setHata] = useState<string | null>(null)

  useEffect(() => {
    const verileriGetir = async () => {
      try {
        const [kurlarResponse, haberlerResponse] = await Promise.all([
          fetch('/kurlar/anlik'),
          fetch('/haberler')
        ])

        if (!kurlarResponse.ok || !haberlerResponse.ok) {
          throw new Error('Veriler alınamadı.')
        }

        const kurlarData = (await kurlarResponse.json()) as KurVerisi
        const haberData = (await haberlerResponse.json()) as Haber[]
        setKurlar(kurlarData)
        setHaberler(haberData)
      } catch (error) {
        setHata(error instanceof Error ? error.message : 'Bilinmeyen bir hata oluştu.')
      } finally {
        setYukleniyor(false)
      }
    }

    verileriGetir()
    const intervalId = setInterval(verileriGetir, 30000)
    return () => clearInterval(intervalId)
  }, [])

  return (
    <main className="container">
      <h1>TL Canlı Piyasa Ekranı</h1>
      {yukleniyor && <p>Yükleniyor...</p>}
      {hata && <p className="error">{hata}</p>}

      {kurlar && (
        <section className="rates-grid">
          <article className="card">
            <h2>Dolar / TL</h2>
            <p className="value">1 USD = {kurlar.usd_try.toLocaleString('tr-TR')} TL</p>
            <small>1 TL = {kurlar.tl_karsiligi_usd.toLocaleString('tr-TR')} USD</small>
          </article>

          <article className="card">
            <h2>Altın (Ons) / TL</h2>
            <p className="value">1 Ons Altın = {kurlar.altin_try_ons.toLocaleString('tr-TR')} TL</p>
            <small>1 TL = {kurlar.tl_karsiligi_altin_ons.toLocaleString('tr-TR')} Ons Altın</small>
          </article>

          <article className="card">
            <h2>Bitcoin / TL</h2>
            <p className="value">1 BTC = {kurlar.bitcoin_try.toLocaleString('tr-TR')} TL</p>
            <small>1 TL = {kurlar.tl_karsiligi_bitcoin.toLocaleString('tr-TR')} BTC</small>
          </article>
        </section>
      )}

      {kurlar && (
        <p className="meta">
          Son Güncelleme: {kurlar.guncellenme_zamani} • Kaynak: {kurlar.kaynak} • Durum:{' '}
          {kurlar.guncel_mi ? 'Canlı' : 'Yedek (Mock)'}
        </p>
      )}

      <section>
        <h2 className="section-title">Borsa Haberleri</h2>
        <ul>
          {haberler.map((haber) => (
            <li key={haber.id} className="card">
              <h3>{haber.baslik}</h3>
              <p>{haber.icerik}</p>
              <small>
                Kaynak: {haber.kaynak} • Tarih: {haber.tarih}
              </small>
            </li>
          ))}
        </ul>
      </section>
    </main>
  )
}

export default App

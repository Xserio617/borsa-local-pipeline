import { useEffect, useState } from 'react'

type Haber = {
  id: number
  baslik: string
  icerik: string
  kaynak: string
  tarih: string
}

function App() {
  const [haberler, setHaberler] = useState<Haber[]>([])
  const [yukleniyor, setYukleniyor] = useState(true)
  const [hata, setHata] = useState<string | null>(null)

  useEffect(() => {
    const fetchHaberler = async () => {
      try {
        const response = await fetch('/haberler')
        if (!response.ok) {
          throw new Error('Haberler alınamadı.')
        }
        const data = (await response.json()) as Haber[]
        setHaberler(data)
      } catch (error) {
        setHata(error instanceof Error ? error.message : 'Bilinmeyen bir hata oluştu.')
      } finally {
        setYukleniyor(false)
      }
    }

    fetchHaberler()
  }, [])

  return (
    <main className="container">
      <h1>Borsa Haberleri</h1>
      {yukleniyor && <p>Yükleniyor...</p>}
      {hata && <p className="error">{hata}</p>}
      <ul>
        {haberler.map((haber) => (
          <li key={haber.id}>
            <h2>{haber.baslik}</h2>
            <p>{haber.icerik}</p>
            <small>
              Kaynak: {haber.kaynak} • Tarih: {haber.tarih}
            </small>
          </li>
        ))}
      </ul>
    </main>
  )
}

export default App

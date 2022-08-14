import requests
from bs4 import BeautifulSoup


def ekstraksi_data():
    """
    Tangal : 08 Agustus 2021
    Waktu : 19:59:52 WIB
    Magnitudo : 4.0
    Kedalaman : 176 km
    Lokasi Gempa : LS=1.48 BT=134.81
    Pusat Gempa : 176 KM Barat Laut Ransiki
    Dirasakan (skala MMI): II-III, Manokwari; II-III Ransiki
    :return:
    """
    try:
        content = requests.get('https://bmkg.go.id')
    except Exception:
        return None

    if content.status_code == 200:
        soup = BeautifulSoup(content.text, 'html.parser')

        result = soup.find('span', {'class':'waktu'})
        result = result.text.split(',')
        tanggal = result[0]
        waktu = result[1]

        result = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
        result = result.findChildren('li')
        i = 0
        magnitudo = None
        kedalaman =  None
        koordinat = None
        lokasi = None
        tsunami = None

        ls = None
        bt = None
        pusat = None
        dirasakan = None

        for res in result:
            print(i, res)
            if i == 1:
                magnitudo = res.text
            elif i == 2:
                kedalaman =  res.text
            elif i == 3:
                koordinat = res.text.split(' - ')
                ls = koordinat[0]
                bt = koordinat[1]
            elif i == 4:
                lokasi = res.text
            elif i == 5:
                tsunami = res.text
            i = i + 1

        hasil = dict()
        hasil['tanggal'] = tanggal # '08 Agustus 2022'
        hasil['waktu'] = waktu #'19:59:52 WIB'
        hasil['magnitudo'] = magnitudo
        hasil['kedalaman'] = kedalaman
        hasil['koordinat'] = {'ls': ls, 'bt': bt}
        hasil['lokasi'] = lokasi
        hasil['tsunami'] = tsunami
        return hasil
    else:
        return None

def tampilkan_data(result):
    if result is None:
       print('Tidak bisa menampilkan data gempa terkini')
    else:
        print('\nGempa Terakhir berdasarkan BMKG')
        print(f"Tanggal {result['tanggal']}")
        print(f"waktu {result['waktu']}")
        print(f"Magnitudo {result['magnitudo']}")
        print(f"Kedalaman {result['kedalaman']}")
        print(f"Koordinat: ls={result['koordinat']['ls']}, bt={result['koordinat']['bt']}")
        print(f"Lokasi {result['lokasi']}")
        print(f"Tsunami {result['tsunami']}")
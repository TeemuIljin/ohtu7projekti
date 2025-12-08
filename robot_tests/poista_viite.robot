*** Settings ***
Resource  resource.robot

*** Test Cases ***
Poista Viite Onnistuneesti
    Luo Testiviite Kirja  Mika Waltari  Sinuhe  1945  WSOY
    Viitteiden Maara On  1
    ${tulos}=  Poista Viite  Sinuhe
    Poisto Onnistui  ${tulos}
    Viitteiden Maara On  0
    Viitetta Ei Loydy Listalta  Sinuhe

Poista Viite Jota Ei Ole
    Luo Testiviite Kirja  Mika Waltari  Sinuhe  1945  WSOY
    ${tulos}=  Poista Viite  Olematon kirja
    Poisto Epaonnistui  ${tulos}
    Viitteiden Maara On  1
    Viite Loytyyy Listalta  Sinuhe

Poista Yksi Viite Useasta
    Luo Testiviite Kirja  Mika Waltari  Sinuhe  1945  WSOY
    Luo Testiviite Kirja  Vaino Linna  Tuntematon sotilas  1954  WSOY
    Luo Testiviite Kirja  Sofi Oksanen  Puhdistus  2008  Like
    Viitteiden Maara On  3
    ${tulos}=  Poista Viite  Tuntematon sotilas
    Poisto Onnistui  ${tulos}
    Viitteiden Maara On  2
    Viite Loytyyy Listalta  Sinuhe
    Viitetta Ei Loydy Listalta  Tuntematon sotilas
    Viite Loytyyy Listalta  Puhdistus

Poista Viite Tyhjasta Listasta
    Viitteiden Maara On  0
    ${tulos}=  Poista Viite  Joku kirja
    Poisto Epaonnistui  ${tulos}
    Viitteiden Maara On  0


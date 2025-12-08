*** Settings ***
Resource  resource.robot

*** Test Cases ***
Listaa Viitteet Kun Ei Viitteita
    Viitteiden Maara On  0

Listaa Viitteet Yhden Viitteen Jalkeen
    Luo Testiviite Kirja  Mika Waltari  Sinuhe  1945  WSOY
    Viitteiden Maara On  1
    Viite Loytyyy Listalta  Sinuhe

Listaa Viitteet Usean Viitteen Jalkeen
    Luo Testiviite Kirja  Mika Waltari  Sinuhe  1945  WSOY
    Luo Testiviite Kirja  Vaino Linna  Tuntematon sotilas  1954  WSOY
    Luo Testiviite Kirja  Sofi Oksanen  Puhdistus  2008  Like
    Viitteiden Maara On  3
    Viite Loytyyy Listalta  Sinuhe
    Viite Loytyyy Listalta  Tuntematon sotilas
    Viite Loytyyy Listalta  Puhdistus


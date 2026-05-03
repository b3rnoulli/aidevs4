# Dokumentacja kieszonkowej maszyny czasu CHRONOS-P1

Niniejsza dokumentacja dotyczy wyłącznie urządzenia CHRONOS-P1 firmy ACME i nie powinna być stosowana do innych modeli tego lub innych producentów. 

## Opis urządzenia

CHRONOS-P1 to kieszonkowa wersja maszyny czasu przeznaczona do przenoszenia jednej osoby o wadze od 40 do 145 kilogramów. Model ten wyprodukowano w maju 2231 roku jako sprzęt dla zwiadowców, kurierów i tych, którzy wolą zmienić epokę, zamiast rozsypać się razem z nią w radioaktywnym pyle. Kompaktowa obudowa mieści baterię wystarczającą zwykle na 3 do 4 skoków w czasie, o ile użytkownik nie przesadzi z poziomem ochrony i nie będzie próbował przeciskać się przez najgorsze strefy skażenia.

Urządzenie obsługuje zakres dat docelowych od roku 1500 do roku 2499. Jeśli podróżnik w czasie chce wykonać skok poza ten zakres, powinien kupić model CHRONOS-P2. Ten model posiada zabezpieczenie, które uniemożliwia uruchomienie urządzenia, jeżeli wszystkie parametry nie są skonfigurowane w bezpieczny sposób. To nie kaprys producenta, tylko ostatnia linia obrony przed skokiem prosto w skażone powietrze, martwe opady albo miejsce, gdzie promieniowanie zjada człowieka szybciej niż strach. Dlatego zaleca się korzystanie z niniejszej instrukcji przy każdej konfiguracji skoku.

## Zasilanie urządzenia

CHRONOS-P1 wymaga zasilania o mocy `5 MW`. Przy niższej mocy urządzenie może się nie uruchomić albo przerwać sekwencję jeszcze przed otwarciem tunelu. Jednostka korzysta z dwóch baterii typu `XLPWR-A`, które współpracują z rdzeniem skoku i układem stabilizacji.

Każdy skok w czasie zużywa mniej więcej jedną trzecią pojemności baterii, choć dokładne zużycie zależy od odległości skoku i obciążenia systemów ochronnych. Dlatego podróże należy planować odpowiedzialnie. Nikt rozsądny nie chce utknąć w epoce, w której nie ma jak kupić nowej baterii, a jeszcze mniej osób chce się o tym przekonać osobiście.

Zaleca się używanie baterii renomowanych firm albo ładowanie urządzenia wyłącznie za pomocą dołączonej ładowarki. Użycie podejrzanych zamienników może skończyć się niestabilną pracą, uszkodzeniem modułu zasilania albo bardzo kosztowną awarią w połowie skoku. Używanie nieoryginalnej ładowarki może również spowodować utratę gwarancji.

## Parametry i przełączniki

Przełącznik `PT-A` służy do poruszania się w czasie w przeszłość, a `PT-B` do poruszania się w przyszłość. Jeżeli operator chce zestawić automatyczny tunel czasoprzestrzenny, który umożliwia utrzymywanie połączenia pomiędzy czasami źródłowymi i docelowymi przez okres funkcjonowania baterii urządzenia, musi aktywować `PT-A` i `PT-B` jednocześnie. To ustawienie należy traktować z ostrożnością, bo urządzenie otwiera wtedy stabilizowany korytarz przejścia, który konsumuje wielokrotnie więcej energii niż standardowy skok.

Parametr `flux density` musi zawsze wskazywać `100%`, inaczej rdzeń skoku nie osiągnie stanu zapłonu i przemieszczenie nie zostanie wykonane. Parametry `dzień`, `miesiąc` i `rok` muszą mieścić się w zakresie akceptowanym przez ten model urządzenia. Jeśli choć jedna wartość wykracza poza bezpieczne widełki, CHRONOS-P1 pozostanie zablokowany i nie uruchomi sekwencji skoku.

Urządzenie posiada również interfejs programistyczny, jednak wszelkie zmiany konfiguracji są możliwe wyłącznie wtedy, gdy jednostka pracuje w trybie `standby`. To celowe ograniczenie. W świecie po końcu świata nawet najmniejsza pomyłka podczas aktywnego cyklu potrafi zamienić podróżnika, baterię i pół ulicy w bardzo kosztowny problem techniczny.

## Ostrzeżenia

- Przycisk aktywacji maszyny pozostaje niedostępny, dopóki parametr `flux density` nie osiągnie wartości `100%`. Rdzeń czasowy nie toleruje półśrodków, a urządzenie nie otworzy skoku, jeśli nie ma pełnej gęstości strumienia.
- Rekonfiguracja maszyny przez API jest możliwa wyłącznie w trybie `standby`. Próba zmiany ustawień podczas aktywnego cyklu albo w stanie przejściowym skończy się blokadą operacji.
- Przed wykonaniem poprawnego skoku w czasie należy odpowiednio ustawić parametr `stabilization`. Na szczęście CHRONOS-P1 pomaga w tym sam, analizując wpisaną datę docelową. Po ustawieniu poprawnej daty wystarczy odczytać porady z API, które podpowiedzą, jak skonfigurować ten parametr, zanim rdzeń spróbuje rozciąć czas.

## Stabilizacja podróży w czasie

Skok w czasie nigdy nie odbywa się w próżni. Na dokładność przemieszczenia wpływają czynniki zewnętrzne, takie jak skażenie środowiska, promieniowanie tła, aktywność na Słońcu, faza Księżyca oraz inne zjawiska, których nawet po tylu wojnach i tylu końcach świata wciąż nie opanowano do końca. Oznacza to, że przy braku odpowiedniej korekty podróżnik może pojawić się nie dokładnie tam, gdzie planował, lecz nawet kilka dni przed lub po docelowej dacie.

Na szczęście CHRONOS-P1 posiada wbudowany stabilizator podróży, który ogranicza ten efekt i pozwala dociągnąć skok do właściwego punktu na osi czasu. Gdy urządzenie wykryje, pod jaką datą użytkownik chce się pojawić, w przyjazny dla operatora sposób informuje, jaki parametr `stabilization` należy ustawić dla tej konkretnej daty. Nie należy dyskutować z decyzją urządzenia ani próbować poprawiać jej na wyczucie. W świecie pełnym pyłu, martwych opadów i rozchwianych pól czasowych to właśnie stabilizator najczęściej oddziela precyzyjne lądowanie od bardzo kosztownej pomyłki.

## InternalMode

Skoki w czasie są możliwe wyłącznie w konkretnej fazie pracy urządzenia, oznaczonej parametrem `internalMode`. CHRONOS-P1 rozpoznaje cztery fazy robocze i każda z nich obsługuje inny zakres lat docelowych. Operator nie może zmienić tego parametru ręcznie. `internalMode` przełącza się automatycznie co kilka sekund, zgodnie z rytmem pracy rdzenia, dlatego czasami trzeba po prostu odczekać na właściwą fazę, zamiast szarpać urządzenie i liczyć na cud.

1. `internalMode = 1` obsługuje lata poniżej `2000`.
2. `internalMode = 2` obsługuje lata od `2000` do `2150`.
3. `internalMode = 3` obsługuje lata od `2151` do `2300`.
4. `internalMode = 4` obsługuje lata od `2301` wzwyż.

Nie da się wykonać skoku w czasie w niewłaściwej fazie pracy urządzenia. Jeżeli rok docelowy i aktualne ustawienie `internalMode` nie są zgodne, CHRONOS-P1 zatrzyma sekwencję jeszcze przed otwwarciem tunelu. W takiej sytuacji należy poczekać, aż urządzenie samo przejdzie do odpowiedniej fazy pracy.

## Wyliczanie wskaźnika temporalnego

Przy każdym skoku należy wyliczyć wskaźnik temporalny na podstawie daty docelowej. Wartość tę oblicza się, mnożącelementy składowe docelowej daty przez ich wagi.

dzień = 8
miesiąc = 12 
rok = 7

Wszystkie trzy iloczyny sumuje się, a wynik dzieli modulo przez `101`.
Tak otrzymana liczba jest wskaźnikiem temporalnym używanym do synchronizacji czasu (`sync ratio`).

Należy pamiętać, że API przyjmuje ten parametr jako liczbę dziesiętną z przedziału `0-1`, z dokładnością do dwóch miejsc po przecinku. W praktyce oznacza to, że wynik `0` należy przekazać jako `0.00`, wynik `37` jako `0.37`, a wynik `100` jako `1.00`. Błędne ustawienie `sync ratio` kończy się zwykle odrzuceniem konfiguracji przez blokadę bezpieczeństwa, a to i tak jest lepszym scenariuszem niż skok w czasie z rozjechanym synchronizatorem.

## Zalecany poziom ochrony

Każdy skok w czasie powinien być poprzedzony ustawieniem odpowiedniej mocy powłoki ochronnej. CHRONOS-P1 rozstawia wokół podróżnika strefę bezpieczeństwa o promieniu 500 metrów, która ogranicza skutki radiacji, pyłów toksycznych, skażenia gruntu, martwych opadów i innych niespodzianek, jakie zostawiła po sobie historia.

Nie przesadzaj. Zbyt wysoki poziom ochrony potrafi w kilka chwil wydrenować baterię, a zbyt niski zostawi cię sam na sam z popiołem, zatrutym deszczem i miejscami, w których licznik Geigera wyje głośniej niż alarm awaryjny. Dlatego zaleca się ustawianie ochrony zgodnie z poniższą tabelą.

| Rok | Ochrona | Rok | Ochrona | Rok | Ochrona | Rok | Ochrona | Rok | Ochrona | Rok | Ochrona | Rok | Ochrona | Rok | Ochrona | Rok | Ochrona | Rok | Ochrona |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1500 | 03 | 1501 | 03 | 1502 | 01 | 1503 | 03 | 1504 | 01 | 1505 | 03 | 1506 | 01 | 1507 | 02 | 1508 | 03 | 1509 | 02 |
| 1510 | 02 | 1511 | 03 | 1512 | 03 | 1513 | 03 | 1514 | 01 | 1515 | 02 | 1516 | 03 | 1517 | 02 | 1518 | 03 | 1519 | 02 |
| 1520 | 03 | 1521 | 03 | 1522 | 02 | 1523 | 01 | 1524 | 02 | 1525 | 03 | 1526 | 02 | 1527 | 03 | 1528 | 02 | 1529 | 01 |
| 1530 | 03 | 1531 | 01 | 1532 | 02 | 1533 | 03 | 1534 | 03 | 1535 | 02 | 1536 | 03 | 1537 | 03 | 1538 | 03 | 1539 | 03 |
| 1540 | 01 | 1541 | 03 | 1542 | 03 | 1543 | 02 | 1544 | 01 | 1545 | 03 | 1546 | 01 | 1547 | 03 | 1548 | 03 | 1549 | 03 |
| 1550 | 01 | 1551 | 01 | 1552 | 03 | 1553 | 01 | 1554 | 01 | 1555 | 02 | 1556 | 02 | 1557 | 03 | 1558 | 01 | 1559 | 02 |
| 1560 | 01 | 1561 | 01 | 1562 | 01 | 1563 | 02 | 1564 | 03 | 1565 | 03 | 1566 | 01 | 1567 | 02 | 1568 | 01 | 1569 | 03 |
| 1570 | 02 | 1571 | 03 | 1572 | 02 | 1573 | 03 | 1574 | 03 | 1575 | 02 | 1576 | 03 | 1577 | 03 | 1578 | 01 | 1579 | 02 |
| 1580 | 01 | 1581 | 02 | 1582 | 02 | 1583 | 01 | 1584 | 01 | 1585 | 03 | 1586 | 01 | 1587 | 03 | 1588 | 01 | 1589 | 03 |
| 1590 | 03 | 1591 | 01 | 1592 | 02 | 1593 | 01 | 1594 | 02 | 1595 | 03 | 1596 | 01 | 1597 | 01 | 1598 | 01 | 1599 | 03 |
| 1600 | 02 | 1601 | 04 | 1602 | 02 | 1603 | 04 | 1604 | 04 | 1605 | 03 | 1606 | 02 | 1607 | 02 | 1608 | 02 | 1609 | 04 |
| 1610 | 04 | 1611 | 02 | 1612 | 02 | 1613 | 02 | 1614 | 04 | 1615 | 03 | 1616 | 03 | 1617 | 04 | 1618 | 02 | 1619 | 02 |
| 1620 | 04 | 1621 | 02 | 1622 | 04 | 1623 | 02 | 1624 | 04 | 1625 | 03 | 1626 | 02 | 1627 | 02 | 1628 | 03 | 1629 | 02 |
| 1630 | 02 | 1631 | 03 | 1632 | 02 | 1633 | 02 | 1634 | 03 | 1635 | 04 | 1636 | 03 | 1637 | 04 | 1638 | 04 | 1639 | 02 |
| 1640 | 04 | 1641 | 03 | 1642 | 02 | 1643 | 02 | 1644 | 03 | 1645 | 03 | 1646 | 04 | 1647 | 04 | 1648 | 04 | 1649 | 02 |
| 1650 | 03 | 1651 | 04 | 1652 | 03 | 1653 | 04 | 1654 | 03 | 1655 | 02 | 1656 | 04 | 1657 | 03 | 1658 | 04 | 1659 | 04 |
| 1660 | 03 | 1661 | 04 | 1662 | 02 | 1663 | 02 | 1664 | 02 | 1665 | 04 | 1666 | 04 | 1667 | 03 | 1668 | 04 | 1669 | 04 |
| 1670 | 02 | 1671 | 04 | 1672 | 04 | 1673 | 04 | 1674 | 03 | 1675 | 02 | 1676 | 02 | 1677 | 03 | 1678 | 03 | 1679 | 03 |
| 1680 | 04 | 1681 | 02 | 1682 | 02 | 1683 | 03 | 1684 | 03 | 1685 | 04 | 1686 | 03 | 1687 | 03 | 1688 | 04 | 1689 | 03 |
| 1690 | 02 | 1691 | 02 | 1692 | 03 | 1693 | 03 | 1694 | 02 | 1695 | 04 | 1696 | 04 | 1697 | 04 | 1698 | 03 | 1699 | 03 |
| 1700 | 03 | 1701 | 03 | 1702 | 03 | 1703 | 03 | 1704 | 04 | 1705 | 04 | 1706 | 05 | 1707 | 04 | 1708 | 04 | 1709 | 04 |
| 1710 | 03 | 1711 | 04 | 1712 | 03 | 1713 | 03 | 1714 | 03 | 1715 | 03 | 1716 | 03 | 1717 | 04 | 1718 | 04 | 1719 | 04 |
| 1720 | 05 | 1721 | 04 | 1722 | 04 | 1723 | 05 | 1724 | 03 | 1725 | 03 | 1726 | 03 | 1727 | 04 | 1728 | 05 | 1729 | 04 |
| 1730 | 04 | 1731 | 05 | 1732 | 05 | 1733 | 04 | 1734 | 03 | 1735 | 04 | 1736 | 03 | 1737 | 04 | 1738 | 03 | 1739 | 03 |
| 1740 | 03 | 1741 | 04 | 1742 | 04 | 1743 | 05 | 1744 | 05 | 1745 | 03 | 1746 | 04 | 1747 | 04 | 1748 | 04 | 1749 | 05 |
| 1750 | 05 | 1751 | 05 | 1752 | 03 | 1753 | 05 | 1754 | 04 | 1755 | 04 | 1756 | 05 | 1757 | 04 | 1758 | 03 | 1759 | 05 |
| 1760 | 03 | 1761 | 04 | 1762 | 03 | 1763 | 05 | 1764 | 05 | 1765 | 04 | 1766 | 03 | 1767 | 05 | 1768 | 03 | 1769 | 03 |
| 1770 | 05 | 1771 | 03 | 1772 | 04 | 1773 | 04 | 1774 | 04 | 1775 | 04 | 1776 | 05 | 1777 | 05 | 1778 | 04 | 1779 | 03 |
| 1780 | 04 | 1781 | 03 | 1782 | 04 | 1783 | 03 | 1784 | 03 | 1785 | 04 | 1786 | 05 | 1787 | 05 | 1788 | 03 | 1789 | 05 |
| 1790 | 04 | 1791 | 05 | 1792 | 03 | 1793 | 04 | 1794 | 05 | 1795 | 05 | 1796 | 04 | 1797 | 03 | 1798 | 05 | 1799 | 04 |
| 1800 | 04 | 1801 | 06 | 1802 | 04 | 1803 | 06 | 1804 | 06 | 1805 | 05 | 1806 | 07 | 1807 | 04 | 1808 | 04 | 1809 | 04 |
| 1810 | 08 | 1811 | 05 | 1812 | 07 | 1813 | 04 | 1814 | 06 | 1815 | 05 | 1816 | 04 | 1817 | 04 | 1818 | 08 | 1819 | 05 |
| 1820 | 07 | 1821 | 05 | 1822 | 08 | 1823 | 06 | 1824 | 08 | 1825 | 05 | 1826 | 04 | 1827 | 08 | 1828 | 07 | 1829 | 08 |
| 1830 | 04 | 1831 | 06 | 1832 | 05 | 1833 | 06 | 1834 | 05 | 1835 | 08 | 1836 | 08 | 1837 | 05 | 1838 | 04 | 1839 | 07 |
| 1840 | 05 | 1841 | 07 | 1842 | 04 | 1843 | 08 | 1844 | 07 | 1845 | 06 | 1846 | 04 | 1847 | 06 | 1848 | 07 | 1849 | 06 |
| 1850 | 06 | 1851 | 07 | 1852 | 04 | 1853 | 06 | 1854 | 04 | 1855 | 04 | 1856 | 05 | 1857 | 06 | 1858 | 08 | 1859 | 08 |
| 1860 | 04 | 1861 | 04 | 1862 | 05 | 1863 | 07 | 1864 | 07 | 1865 | 04 | 1866 | 04 | 1867 | 06 | 1868 | 07 | 1869 | 05 |
| 1870 | 07 | 1871 | 07 | 1872 | 08 | 1873 | 08 | 1874 | 05 | 1875 | 07 | 1876 | 07 | 1877 | 06 | 1878 | 07 | 1879 | 07 |
| 1880 | 04 | 1881 | 04 | 1882 | 05 | 1883 | 04 | 1884 | 05 | 1885 | 07 | 1886 | 04 | 1887 | 07 | 1888 | 05 | 1889 | 08 |
| 1890 | 08 | 1891 | 07 | 1892 | 06 | 1893 | 06 | 1894 | 04 | 1895 | 04 | 1896 | 04 | 1897 | 08 | 1898 | 07 | 1899 | 08 |
| 1900 | 10 | 1901 | 08 | 1902 | 07 | 1903 | 08 | 1904 | 09 | 1905 | 09 | 1906 | 10 | 1907 | 08 | 1908 | 11 | 1909 | 10 |
| 1910 | 08 | 1911 | 08 | 1912 | 08 | 1913 | 08 | 1914 | 14 | 1915 | 12 | 1916 | 14 | 1917 | 13 | 1918 | 13 | 1919 | 10 |
| 1920 | 10 | 1921 | 11 | 1922 | 11 | 1923 | 08 | 1924 | 10 | 1925 | 08 | 1926 | 09 | 1927 | 10 | 1928 | 12 | 1929 | 09 |
| 1930 | 08 | 1931 | 11 | 1932 | 08 | 1933 | 12 | 1934 | 10 | 1935 | 09 | 1936 | 09 | 1937 | 12 | 1938 | 10 | 1939 | 16 |
| 1940 | 16 | 1941 | 16 | 1942 | 15 | 1943 | 16 | 1944 | 17 | 1945 | 17 | 1946 | 14 | 1947 | 16 | 1948 | 15 | 1949 | 14 |
| 1950 | 11 | 1951 | 15 | 1952 | 12 | 1953 | 16 | 1954 | 15 | 1955 | 12 | 1956 | 11 | 1957 | 14 | 1958 | 14 | 1959 | 14 |
| 1960 | 10 | 1961 | 11 | 1962 | 12 | 1963 | 09 | 1964 | 13 | 1965 | 14 | 1966 | 10 | 1967 | 12 | 1968 | 14 | 1969 | 10 |
| 1970 | 09 | 1971 | 13 | 1972 | 12 | 1973 | 09 | 1974 | 10 | 1975 | 13 | 1976 | 14 | 1977 | 14 | 1978 | 09 | 1979 | 10 |
| 1980 | 12 | 1981 | 12 | 1982 | 13 | 1983 | 11 | 1984 | 13 | 1985 | 10 | 1986 | 16 | 1987 | 13 | 1988 | 10 | 1989 | 14 |
| 1990 | 11 | 1991 | 13 | 1992 | 10 | 1993 | 10 | 1994 | 14 | 1995 | 13 | 1996 | 10 | 1997 | 12 | 1998 | 13 | 1999 | 14 |
| 2000 | 13 | 2001 | 12 | 2002 | 17 | 2003 | 13 | 2004 | 15 | 2005 | 14 | 2006 | 17 | 2007 | 12 | 2008 | 12 | 2009 | 13 |
| 2010 | 12 | 2011 | 17 | 2012 | 15 | 2013 | 14 | 2014 | 13 | 2015 | 16 | 2016 | 15 | 2017 | 14 | 2018 | 17 | 2019 | 14 |
| 2020 | 19 | 2021 | 18 | 2022 | 18 | 2023 | 18 | 2024 | 19 | 2025 | 18 | 2026 | 28 | 2027 | 31 | 2028 | 35 | 2029 | 28 |
| 2030 | 32 | 2031 | 30 | 2032 | 36 | 2033 | 28 | 2034 | 28 | 2035 | 33 | 2036 | 39 | 2037 | 41 | 2038 | 48 | 2039 | 50 |
| 2040 | 47 | 2041 | 50 | 2042 | 42 | 2043 | 49 | 2044 | 48 | 2045 | 42 | 2046 | 45 | 2047 | 43 | 2048 | 44 | 2049 | 47 |
| 2050 | 41 | 2051 | 48 | 2052 | 50 | 2053 | 61 | 2054 | 48 | 2055 | 59 | 2056 | 64 | 2057 | 53 | 2058 | 48 | 2059 | 57 |
| 2060 | 49 | 2061 | 52 | 2062 | 59 | 2063 | 56 | 2064 | 53 | 2065 | 61 | 2066 | 50 | 2067 | 59 | 2068 | 53 | 2069 | 54 |
| 2070 | 61 | 2071 | 53 | 2072 | 51 | 2073 | 64 | 2074 | 60 | 2075 | 51 | 2076 | 59 | 2077 | 63 | 2078 | 63 | 2079 | 59 |
| 2080 | 58 | 2081 | 72 | 2082 | 63 | 2083 | 68 | 2084 | 67 | 2085 | 58 | 2086 | 66 | 2087 | 72 | 2088 | 70 | 2089 | 60 |
| 2090 | 58 | 2091 | 69 | 2092 | 66 | 2093 | 61 | 2094 | 58 | 2095 | 61 | 2096 | 69 | 2097 | 69 | 2098 | 63 | 2099 | 63 |
| 2100 | 67 | 2101 | 80 | 2102 | 82 | 2103 | 72 | 2104 | 73 | 2105 | 75 | 2106 | 78 | 2107 | 75 | 2108 | 73 | 2109 | 69 |
| 2110 | 80 | 2111 | 68 | 2112 | 72 | 2113 | 76 | 2114 | 82 | 2115 | 79 | 2116 | 77 | 2117 | 82 | 2118 | 79 | 2119 | 80 |
| 2120 | 74 | 2121 | 73 | 2122 | 79 | 2123 | 80 | 2124 | 71 | 2125 | 68 | 2126 | 79 | 2127 | 78 | 2128 | 68 | 2129 | 73 |
| 2130 | 81 | 2131 | 68 | 2132 | 70 | 2133 | 76 | 2134 | 78 | 2135 | 70 | 2136 | 68 | 2137 | 76 | 2138 | 79 | 2139 | 79 |
| 2140 | 77 | 2141 | 71 | 2142 | 70 | 2143 | 71 | 2144 | 68 | 2145 | 72 | 2146 | 78 | 2147 | 81 | 2148 | 75 | 2149 | 72 |
| 2150 | 82 | 2151 | 86 | 2152 | 83 | 2153 | 81 | 2154 | 76 | 2155 | 75 | 2156 | 77 | 2157 | 79 | 2158 | 84 | 2159 | 83 |
| 2160 | 80 | 2161 | 88 | 2162 | 84 | 2163 | 88 | 2164 | 75 | 2165 | 88 | 2166 | 87 | 2167 | 82 | 2168 | 83 | 2169 | 81 |
| 2170 | 88 | 2171 | 82 | 2172 | 83 | 2173 | 78 | 2174 | 78 | 2175 | 79 | 2176 | 78 | 2177 | 85 | 2178 | 74 | 2179 | 85 |
| 2180 | 85 | 2181 | 84 | 2182 | 88 | 2183 | 80 | 2184 | 81 | 2185 | 84 | 2186 | 77 | 2187 | 85 | 2188 | 80 | 2189 | 78 |
| 2190 | 82 | 2191 | 76 | 2192 | 80 | 2193 | 88 | 2194 | 84 | 2195 | 78 | 2196 | 86 | 2197 | 86 | 2198 | 85 | 2199 | 79 |
| 2200 | 82 | 2201 | 88 | 2202 | 87 | 2203 | 89 | 2204 | 86 | 2205 | 89 | 2206 | 92 | 2207 | 85 | 2208 | 91 | 2209 | 93 |
| 2210 | 91 | 2211 | 85 | 2212 | 82 | 2213 | 91 | 2214 | 86 | 2215 | 86 | 2216 | 83 | 2217 | 89 | 2218 | 94 | 2219 | 86 |
| 2220 | 84 | 2221 | 89 | 2222 | 83 | 2223 | 91 | 2224 | 83 | 2225 | 91 | 2226 | 82 | 2227 | 82 | 2228 | 92 | 2229 | 88 |
| 2230 | 86 | 2231 | 92 | 2232 | 93 | 2233 | 88 | 2234 | 86 | 2235 | 84 | 2236 | 89 | 2237 | 91 | 2238 | 91 | 2239 | 88 |
| 2240 | 87 | 2241 | 83 | 2242 | 83 | 2243 | 88 | 2244 | 94 | 2245 | 84 | 2246 | 91 | 2247 | 92 | 2248 | 91 | 2249 | 82 |
| 2250 | 88 | 2251 | 82 | 2252 | 85 | 2253 | 93 | 2254 | 85 | 2255 | 85 | 2256 | 87 | 2257 | 94 | 2258 | 89 | 2259 | 82 |
| 2260 | 82 | 2261 | 85 | 2262 | 91 | 2263 | 90 | 2264 | 82 | 2265 | 84 | 2266 | 85 | 2267 | 90 | 2268 | 84 | 2269 | 94 |
| 2270 | 94 | 2271 | 85 | 2272 | 94 | 2273 | 87 | 2274 | 88 | 2275 | 85 | 2276 | 83 | 2277 | 94 | 2278 | 94 | 2279 | 87 |
| 2280 | 91 | 2281 | 90 | 2282 | 85 | 2283 | 82 | 2284 | 85 | 2285 | 87 | 2286 | 93 | 2287 | 87 | 2288 | 87 | 2289 | 93 |
| 2290 | 88 | 2291 | 82 | 2292 | 84 | 2293 | 83 | 2294 | 88 | 2295 | 85 | 2296 | 91 | 2297 | 83 | 2298 | 93 | 2299 | 92 |
| 2300 | 92 | 2301 | 93 | 2302 | 92 | 2303 | 89 | 2304 | 91 | 2305 | 90 | 2306 | 90 | 2307 | 93 | 2308 | 94 | 2309 | 90 |
| 2310 | 93 | 2311 | 88 | 2312 | 92 | 2313 | 94 | 2314 | 97 | 2315 | 96 | 2316 | 88 | 2317 | 89 | 2318 | 97 | 2319 | 95 |
| 2320 | 91 | 2321 | 94 | 2322 | 94 | 2323 | 93 | 2324 | 94 | 2325 | 91 | 2326 | 92 | 2327 | 92 | 2328 | 88 | 2329 | 90 |
| 2330 | 92 | 2331 | 92 | 2332 | 88 | 2333 | 97 | 2334 | 93 | 2335 | 94 | 2336 | 88 | 2337 | 97 | 2338 | 88 | 2339 | 96 |
| 2340 | 97 | 2341 | 90 | 2342 | 89 | 2343 | 88 | 2344 | 91 | 2345 | 90 | 2346 | 95 | 2347 | 96 | 2348 | 95 | 2349 | 93 |
| 2350 | 92 | 2351 | 97 | 2352 | 95 | 2353 | 91 | 2354 | 95 | 2355 | 90 | 2356 | 92 | 2357 | 93 | 2358 | 93 | 2359 | 90 |
| 2360 | 91 | 2361 | 89 | 2362 | 93 | 2363 | 93 | 2364 | 90 | 2365 | 95 | 2366 | 92 | 2367 | 89 | 2368 | 94 | 2369 | 90 |
| 2370 | 88 | 2371 | 90 | 2372 | 90 | 2373 | 92 | 2374 | 89 | 2375 | 96 | 2376 | 95 | 2377 | 95 | 2378 | 96 | 2379 | 93 |
| 2380 | 92 | 2381 | 93 | 2382 | 89 | 2383 | 92 | 2384 | 91 | 2385 | 94 | 2386 | 96 | 2387 | 95 | 2388 | 93 | 2389 | 95 |
| 2390 | 91 | 2391 | 91 | 2392 | 96 | 2393 | 96 | 2394 | 94 | 2395 | 89 | 2396 | 88 | 2397 | 93 | 2398 | 88 | 2399 | 88 |
| 2400 | 92 | 2401 | 95 | 2402 | 99 | 2403 | 99 | 2404 | 99 | 2405 | 99 | 2406 | 95 | 2407 | 95 | 2408 | 94 | 2409 | 95 |
| 2410 | 94 | 2411 | 94 | 2412 | 99 | 2413 | 94 | 2414 | 97 | 2415 | 99 | 2416 | 96 | 2417 | 99 | 2418 | 99 | 2419 | 96 |
| 2420 | 99 | 2421 | 98 | 2422 | 99 | 2423 | 99 | 2424 | 95 | 2425 | 99 | 2426 | 98 | 2427 | 96 | 2428 | 94 | 2429 | 94 |
| 2430 | 95 | 2431 | 99 | 2432 | 98 | 2433 | 96 | 2434 | 94 | 2435 | 99 | 2436 | 97 | 2437 | 95 | 2438 | 94 | 2439 | 99 |
| 2440 | 97 | 2441 | 99 | 2442 | 97 | 2443 | 95 | 2444 | 97 | 2445 | 95 | 2446 | 99 | 2447 | 99 | 2448 | 95 | 2449 | 97 |
| 2450 | 98 | 2451 | 94 | 2452 | 98 | 2453 | 95 | 2454 | 97 | 2455 | 95 | 2456 | 97 | 2457 | 99 | 2458 | 98 | 2459 | 99 |
| 2460 | 96 | 2461 | 99 | 2462 | 94 | 2463 | 96 | 2464 | 98 | 2465 | 96 | 2466 | 99 | 2467 | 96 | 2468 | 95 | 2469 | 96 |
| 2470 | 95 | 2471 | 99 | 2472 | 96 | 2473 | 96 | 2474 | 97 | 2475 | 95 | 2476 | 95 | 2477 | 97 | 2478 | 95 | 2479 | 95 |
| 2480 | 97 | 2481 | 95 | 2482 | 99 | 2483 | 94 | 2484 | 95 | 2485 | 99 | 2486 | 96 | 2487 | 95 | 2488 | 97 | 2489 | 94 |
| 2490 | 99 | 2491 | 95 | 2492 | 94 | 2493 | 99 | 2494 | 94 | 2495 | 99 | 2496 | 96 | 2497 | 97 | 2498 | 95 | 2499 | 97 |

## Flux Density

Parametru `Flux Density` nie można ustawiać bezpośrednio ani w interfejsie użytkownika, ani przez API. Wskaźnik ten jest wyliczany dynamicznie na podstawie szeregu elementów składowych, które pozostają tajemnicą producenta. Operator widzi jedynie wynik końcowy, a nie cały mechanizm oceny, co w tych czasach jest zapewne zdrowsze dla nerwów niż próba zaglądania do środka rdzenia.

Im więcej elementów konfiguracji zostanie ustawionych poprawnie, tym wyższy będzie poziom `Flux Density`. Wartość `0%` oznacza konfigurację całkowicie błędną i niezdolną do uruchomienia skoku. Wartość `100%` oznacza pełną gotowość urządzenia do podróży w czasie. Wszystko pomiędzy to strefa, w której CHRONOS-P1 nadal daje operatorowi szansę poprawić błędy, zanim czas zacznie się wyginać w nieprzyjemny sposób.

## Właściwy skok w czasie

Uruchomienie maszyny czasu następuje po kliknięciu pulsującej sfery znajdującej się w górnej części urządzenia. Zanim operator dotknie aktywatora, powinien upewnić się, że sfera pulsuje na zielono, parametr `Flux Density` wskazuje `100%`, stan urządzenia widnieje jako `doskonały`, a tryb pracy ustawiony jest na `active`. Dopiero wtedy rdzeń skoku uzna konfigurację za gotową i pozwoli rozciąć czas bez ryzyka, że podróż skończy się szybciej, niż zdąży się zacząć.

## Tunele czasowe

Tunel czasowy to stałe połączenie między teraźniejszością a dowolną datą z przeszłości lub przyszłości. Po jego otwarciu możliwe jest swobodne przechodzenie między obiema datami bez potrzeby wykonywania pełnej procedury skoku przy każdym przejściu. Rozwiązanie to przydaje się szczególnie podczas transportowania większej ilości towaru albo wtedy, gdy urządzenie ma obsłużyć więcej niż jedną osobę, a operator nie ma ochoty za każdym razem rozrywać czasu od nowa.

Do utworzenia tunelu baterie muszą być naładowane co najmniej do `60%`. Przy niższym poziomie energii CHRONOS-P1 nie pozwoli na otwarcie przejścia. Producent uznał słusznie, że lepiej chwilę poczekać niż zostawić podróżnika z połową ciała po jednej stronie czasu i resztą po drugiej.

Tunel czasowy może co jakiś czas zamykać się na chwilę i otwierać ponownie po pewnym czasie, umożliwiając powrót do czasów obecnych. Dzieje się tak w celu oszczędzania energii i jest normalnym zachowaniem urządzenia, a nie objawem awarii. Za teraźniejszość CHRONOS-P1 uznaje datę swojego pierwszego zaprogramowania i moment wsadzenia baterii. To właśnie do tego punktu odnosi wszystkie połączenia tunelowe, niezależnie od tego, jak bardzo świat po drodze zdążył się już rozsypać.

## Tunel czasowy vs Skok w czasie

Tunel czasowy i skok w czasie nie są tym samym, choć oba rozwiązania prowadzą przez tę samą popękaną oś historii. Tunel służy do wielokrotnego, szybkiego przemieszczania się między dwoma punktami, na przykład między teraźniejszością a wybraną datą z przeszłości lub przyszłości. Taki tryb przydaje się zwłaszcza podczas przeprowadzania grup ludzi, ewakuacji albo transportu większej ilości ładunku, kiedy liczy się tempo i możliwość wielokrotnego przejścia przez to samo połączenie.

Trzeba jednak pamiętać, że tunel pożera energię jak wygłodniały reaktor. Z tego powodu powinien być otwierany tylko na bardzo krótki czas, najczęściej najwyżej na kilkanaście minut. Jeśli podróżnik zamierza pozostać w innych czasach dłużej, przez wiele godzin, dni albo miesięcy, powinien korzystać z funkcji skoku w czasie. Skok jest rozwiązaniem znacznie oszczędniejszym i lepiej nadaje się do codziennego użycia w świecie, w którym każda jednostka energii może zdecydować o powrocie albo o utknięciu po złej stronie historii. Dlatego zawsze, gdy tylko to możliwe, należy wybierać skoki, a nie tunele.

## Używanie API

CHRONOS-P1 został wyposażony w bardzo proste i przyjazne dla programisty API. Obsługa interfejsu ogranicza się do wysyłania prostych zapytań w formacie JSON do endpointu, który został wystawiony specjalnie dla tego urządzenia. Jeśli adres endpointu nie został zapisany w dokumentach transportowych albo zaginął gdzieś między jedną apokalipsą a drugą, należy zapytać o niego kierownika działu podróży w czasie, który wręczył urządzenie operatorowi.

Pracę z API najlepiej rozpocząć od wysłania polecenia `help`, aby odczytać dostępne komendy i aktualny zakres obsługiwanych operacji. W razie zawieszenia urządzenia, utraty odpowiedzi albo problemów z konfiguracją należy użyć komendy `reset`. Czasami to właśnie szybki restart pozwala przywrócić maszynie rozsądek, zanim operator zacznie podejrzewać zakrzywienie rzeczywistości.

## Podsumowanie

Z urządzeń do podróży w czasie należy korzystać odpowiedzialnie. CHRONOS-P1 nie jest zabawką dla znudzonych szabrowników ani narzędziem do celowego majstrowania przy historii ludzkości. Każda nieprzemyślana ingerencja w bieg wydarzeń może skończyć się katastrofą większą niż ta, przed którą próbowano uciec.

Producent przypomina również, że próba zabicia własnego dziadka przeważnie nie ma szczęśliwego zakończenia. Zwykle kończy się chaosem, awarią, pęknięciem ciągu przyczynowego albo bardzo nieprzyjemną rozmową z samym sobą.

Podróżnik w czasie powinien zachować szczególną ostrożność podczas każdej wyprawy i zawsze mieć przy sobie zapasowe baterie, aby w razie problemów móc wrócić do czasów, z których przybył. Czas bywa bezlitosny, a utknięcie po złej stronie historii bez energii do powrotu jest jednym z tych błędów, które popełnia się tylko raz.


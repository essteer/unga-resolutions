# UN General Assembly resolutions

### Acknowledgement

This repo makes use of data obtained with the approval of the UN Digital Library (Dag Hammarskjöld Library), and is © United Nations, 2023, https://digitallibrary.un.org, downloaded on 26/10/2023.

Any inferences, commentary or inaccuracies associated with the presentation of that data in this repo are my own; please consult the original source material made freely available by [Dag Hammarskjöld Library](https://digitallibrary.un.org/).

### Note on UN Member State names

To simplify analysis of this dataset, I consolidated country data by combining historic country names with their modern equivalents.

Take the example of Eswatini: admitted to the UN General Assembly (UNGA) as Swaziland on 24 September 1968, the country changed its official name in April 2018, and has since been identified as Eswatini.

Eswatini and Swaziland refer to the same territorial and political entity, and there is no overlap in their UNGA resolution voting records. Consolidation followed a simple process of merging the voting records associated with each name.

Most examples fit this pattern; a shortlist of examples includes:

- "BYELORUSSIAN SSR" -> "BELARUS",
- "CZECH REPUBLIC" -> "CZECHIA", and
- "SIAM" -> "THAILAND".

**Special characters**

Entities with characters in their names beyond the 26 letters of the English alphabet have been converted, and consolidated in cases where multiple versions existed. For example:

- "CÔTE D\'IVOIRE" -> "IVORY COAST", and
- 'TÜRKİYE' -> "TURKIYE", and
- 'TURKEY' -> "TURKIYE".

**Tanzania**

Tanzania was taken as a special case: Tanganyika and Zanzibar gained independence in 1961 and 1963, respectively, and in 1964 they merged to become the United Republic of Tanzania.

Zanzibar was identified with just eight UNGA resolutions, all between December 1962 and December 1963. It was the subject of A/RES/1811(XVII), passed on 17/12/1962, for which voting breakdowns were not accessible. Of the remaining seven resolutions, Zanzibar was recorded as an "Abstention" for A/RES/1983(XVIII), on 17/12/1963, and "Non-voting" for six, passed on either 16/12/1963 or 17/12/1963.

On the basis that Tanganyika was recorded as a "Yes" vote for all seven of those eight resolutions for which voting breakdowns are accessible, I opted to consolidate the records of both entities and essentially regard Tanganyika and Tanzania as one continuous political entity.

The resolutions noted above are as follows:

| # | Resolution | Date | Tanganyika's Vote | Zanzibar's Vote |
| 01 | A/RES/1811(XVII) | 17/12/1962 | Not disclosed | N/A |
| 02 | A/RES/1978(XVIII)[\B] | 16/12/1963 | Yes | Non-voting |
| 03 | A/RES/1979(XVIII) | 17/12/1963 | Yes | Non-voting |
| 04 | A/RES/1983(XVIII) | 17/12/1963 | Yes | Abstention |
| 05 | A/RES/1990(XVIII) | 17/12/1963 | Yes | Non-voting |
| 06 | A/RES/1991(XVIII)[\A] | 17/12/1963 | Yes | Non-voting |
| 07 | A/RES/1991(XVIII)[\B] | 17/12/1963 | Yes | Non-voting |
| 08 | A/RES/1992(XVIII) | 17/12/1963 | Yes | Non-voting |

**Dissolved states**

Unless otherwise stated, I have not attempted to consolidate data relating to former member states that dissolved into two or more subsequent member states.

Examples in this category include Yugoslavia, which dissolved into several sovereign member states during the 1990s.

**Conversion table**

A full list of name conversions is contained within the table below; the second column contains member state names exactly as obtained from the original dataset.

Finally, the conversions in the third column have been made based on the principles outlined above; if in doing so I have unknowingly

| # | Name on UNGA voting Record | Name used in this dataset |
| 01 | 'BYELORUSSIAN SSR' | BELARUS |
| 02 | 'BOLIVIA (PLURINATIONAL STATE OF)' | BOLIVIA |
| 03 | 'BRUNEI DARUSSALAM' | BRUNEI |
| 04 | 'CABO VERDE' | CAPE VERDE |
| 05 | 'CENTRAL AFRICAN EMPIRE' | CENTRAL AFRICAN REPUBLIC |
| 06 | 'CEYLON' | SRI LANKA |
| 07 | 'CONGO (BRAZZAVILLE)' | CONGO (REPUBLIC OF) |
| 08 | 'CONGO (LEOPOLDVILLE)' | CONGO (DEMOCRATIC REPUBLIC OF) |
| 09 | '"CÔTE D\'IVOIRE"' | IVORY COAST |
| 10 | '"COTE D\'IVOIRE"' | IVORY COAST |
| 11 | 'CZECH REPUBLIC' | CZECHIA |
| 12 | 'DAHOMEY' | BENIN |
| 13 | 'DEMOCRATIC KAMPUCHEA' | CAMBODIA |
| 14 | '"DEMOCRATIC PEOPLE\'S REPUBLIC OF KOREA"' | NORTH KOREA |
| 15 | 'DEMOCRATIC REPUBLIC OF THE CONGO' | CONGO (DEMOCRATIC REPUBLIC OF) |
| 16 | 'GERMAN DEMOCRATIC REPUBLIC' | EAST GERMANY |
| 17 | 'GERMANY, FEDERAL REPUBLIC OF' | GERMANY |
| 18 | 'KHMER REPUBLIC' | CAMBODIA |
| 19 | 'IRAN (ISLAMIC REPUBLIC OF)' | IRAN |
| 20 | '"LAO PEOPLE\'S DEMOCRATIC REPUBLIC"' | LAOS |
| 21 | '"LAO PEOPLE\'s DEMOCRATIC REPUBLIC"' | LAOS |
| 22 | 'LAO' | LAOS |
| 23 | 'LIBYAN ARAB JAMAHIRIYA' | LIBYA |
| 24 | 'LIBYAN ARAB REPUBLIC' | LIBYA |
| 25 | 'MALDIVE ISLANDS' | MALDIVES |
| 26 | 'MICRONESIA (FEDERATED STATES OF)' | MICRONESIA |
| 27 | 'PHILIPPINE REPUBLIC' | PHILIPPINES |
| 28 | 'REPUBLIC OF KOREA' | SOUTH KOREA |
| 29 | 'REPUBLIC OF MOLDOVA' | MOLDOVA |
| 30 | 'RUSSIAN FEDERATION' | RUSSIA |
| 31 | 'SAINT CHRISTOPHER AND NEVIS' | ST KITTS AND NEVIS |
| 32 | 'SIAM' | THAILAND |
| 33 | 'SURINAM' | 'SURINAME' |
| 34 | 'SWAZILAND' | ESWATINI |
| 35 | 'SYRIAN ARAB REPUBLIC' | SYRIA |
| 36 | 'TANGANYIKA' | TANZANIA |  
| 37 | 'THE FORMER YUGOSLAV REPUBLIC OF MACEDONIA' | NORTH MACEDONIA |
| 38 | 'TÜRKİYE' | TURKIYE |
| 39 | 'TURKEY' | TURKIYE |
| 40 | 'UKRAINIAN SSR' | UKRAINE |
| 41 | 'UNION OF SOUTH AFRICA' | SOUTH AFRICA |
| 42 | 'UNITED REPUBLIC OF CAMEROON' | CAMEROON |
| 43 | 'UNITED REPUBLIC OF TANZANIA' | TANZANIA |
| 44 | 'UPPER VOLTA' | BURKINA FASO |
| 45 | 'VENEZUELA (BOLIVARIAN REPUBLIC OF)' | VENEZUELA |
| 46 | 'VIET NAM' | VIETNAM |
| 47 | 'ZAIRE' | CONGO (DEMOCRATIC REPUBLIC OF) |
| 48 | 'ZANZIBAR' | TANZANIA |

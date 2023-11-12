# UN General Assembly resolutions

### Acknowledgement

This repo makes use of data obtained with the approval of the UN Digital Library (Dag Hammarskjöld Library), and is © United Nations, 2023, https://digitallibrary.un.org, downloaded on 26/10/2023.

Any inferences, commentary or inaccuracies associated with the presentation of that data in this repo are my own; please consult the original source material made freely available by [Dag Hammarskjöld Library](https://digitallibrary.un.org/).

### Note on UN Member State names

To simplify analysis of this dataset, I consolidated country data by combining historic country names with their modern equivalents.

Take the example of Eswatini: admitted to the UN General Assembly (UNGA) as Swaziland on 24 September 1968, the country changed its official name in April 2018, and has since been identified as Eswatini.

Eswatini and Swaziland refer to the same territorial and political entity, and there is no overlap in their UNGA resolution voting records. Consolidation followed a simple process of merging the voting records associated with each name.

Most examples fit this pattern; a shortlist of examples includes:

| #   | Name on UNGA voting Record | Name used in this dataset |
| --- | -------------------------- | ------------------------- |
| 01  | 'BYELORUSSIAN SSR'         | BELARUS                   |
| 02  | 'CZECH REPUBLIC'           | CZECHIA                   |
| 03  | 'SIAM'                     | THAILAND                  |

**Special characters**

Entities with characters in their names beyond the 26 letters of the English alphabet have been converted, and consolidated in cases where multiple versions existed. For example:

| #   | Name on UNGA voting Record | Name used in this dataset |
| --- | -------------------------- | ------------------------- |
| 01  | "CÔTE D\'IVOIRE"           | IVORY COAST               |
| 02  | 'TÜRKİYE'                  | TURKIYE                   |
| 03  | 'TURKEY'                   | TURKIYE                   |

**Tanzania**

Tanzania was taken as a special case: Tanganyika and Zanzibar gained independence in 1961 and 1963, respectively, and in 1964 they merged to become the United Republic of Tanzania.

Zanzibar was identified with just eight UNGA resolutions, all between December 1962 and December 1963. It was the subject of A/RES/1811(XVII), passed on 17/12/1962, for which voting breakdowns were not accessible. Of the remaining seven resolutions, Zanzibar was recorded as an "Abstention" for A/RES/1983(XVIII), on 17/12/1963, and "Non-voting" for six, passed on either 16/12/1963 or 17/12/1963.

On the basis that Tanganyika was recorded as a "Yes" vote for all seven of those eight resolutions for which voting breakdowns are accessible, I opted to consolidate the records of both entities and essentially regard Tanganyika and Tanzania as one continuous political entity.

The resolutions noted above are as follows:

| #   | Resolution             | Date       | Tanganyika's Vote | Zanzibar's Vote |
| --- | ---------------------- | ---------- | ----------------- | --------------- |
| 01  | A/RES/1811(XVII)       | 17/12/1962 | Not disclosed     | N/A             |
| 02  | A/RES/1978(XVIII)[ B ] | 16/12/1963 | Yes               | Non-voting      |
| 03  | A/RES/1979(XVIII)      | 17/12/1963 | Yes               | Non-voting      |
| 04  | A/RES/1983(XVIII)      | 17/12/1963 | Yes               | Abstention      |
| 05  | A/RES/1990(XVIII)      | 17/12/1963 | Yes               | Non-voting      |
| 06  | A/RES/1991(XVIII)[ A ] | 17/12/1963 | Yes               | Non-voting      |
| 07  | A/RES/1991(XVIII)[ B ] | 17/12/1963 | Yes               | Non-voting      |
| 08  | A/RES/1992(XVIII)      | 17/12/1963 | Yes               | Non-voting      |

**Dissolved states**

Unless otherwise stated, I have not attempted to consolidate data relating to former member states that dissolved into two or more subsequent member states.

Examples in this category include the Federation of Malaya, which became today's Malaysia and Singapore; and Yugoslavia, which dissolved into several sovereign member states during the 1990s.

**Conversion table**

A full list of name conversions is contained within the table below; the second column contains member state names exactly as obtained from the original dataset.

Finally, the conversions in the third column have been made based on the principles outlined above, and do not reflect any political stance on my part. Should any of these conversions be in error, corrections are welcome.

| #   | Name on UNGA voting Record                  | Name used in this dataset |
| --- | ------------------------------------------- | ------------------------- |
| 01  | 'BYELORUSSIAN SSR'                          | BELARUS                   |
| 02  | 'BOLIVIA (PLURINATIONAL STATE OF)'          | BOLIVIA                   |
| 03  | 'BRUNEI DARUSSALAM'                         | BRUNEI                    |
| 04  | 'CABO VERDE'                                | CAPE VERDE                |
| 05  | 'CENTRAL AFRICAN EMPIRE'                    | CENTRAL AFRICAN REPUBLIC  |
| 06  | 'CEYLON'                                    | SRI LANKA                 |
| 07  | 'CONGO'                                     | CONGO (ROC)               |
| 08  | 'CONGO (BRAZZAVILLE)'                       | CONGO (ROC)               |
| 09  | 'CONGO (DEMOCRATIC REPUBLIC OF)'            | CONGO (DRC)               |
| 10  | 'CONGO (LEOPOLDVILLE)'                      | CONGO (DRC)               |
| 11  | '"CÔTE D\'IVOIRE"'                          | IVORY COAST               |
| 12  | '"COTE D\'IVOIRE"'                          | IVORY COAST               |
| 13  | 'CZECH REPUBLIC'                            | CZECHIA                   |
| 14  | 'DAHOMEY'                                   | BENIN                     |
| 15  | 'DEMOCRATIC KAMPUCHEA'                      | CAMBODIA                  |
| 16  | '"DEMOCRATIC PEOPLE\'S REPUBLIC OF KOREA"'  | NORTH KOREA               |
| 17  | 'DEMOCRATIC REPUBLIC OF THE CONGO'          | CONGO (DRC)               |
| 18  | 'GERMAN DEMOCRATIC REPUBLIC'                | EAST GERMANY              |
| 19  | 'GERMANY, FEDERAL REPUBLIC OF'              | GERMANY                   |
| 20  | 'KHMER REPUBLIC'                            | CAMBODIA                  |
| 21  | 'IRAN (ISLAMIC REPUBLIC OF)'                | IRAN                      |
| 22  | '"LAO PEOPLE\'S DEMOCRATIC REPUBLIC"'       | LAOS                      |
| 23  | '"LAO PEOPLE\'s DEMOCRATIC REPUBLIC"'       | LAOS                      |
| 24  | 'LAO'                                       | LAOS                      |
| 25  | 'LIBYAN ARAB JAMAHIRIYA'                    | LIBYA                     |
| 26  | 'LIBYAN ARAB REPUBLIC'                      | LIBYA                     |
| 27  | 'MALDIVE ISLANDS'                           | MALDIVES                  |
| 28  | 'MICRONESIA (FEDERATED STATES OF)'          | MICRONESIA                |
| 29  | 'PHILIPPINE REPUBLIC'                       | PHILIPPINES               |
| 30  | 'REPUBLIC OF KOREA'                         | SOUTH KOREA               |
| 31  | 'REPUBLIC OF MOLDOVA'                       | MOLDOVA                   |
| 32  | 'RUSSIAN FEDERATION'                        | RUSSIA                    |
| 33  | 'SAINT CHRISTOPHER AND NEVIS'               | ST KITTS AND NEVIS        |
| 34  | 'SIAM'                                      | THAILAND                  |
| 35  | 'SURINAM'                                   | SURINAME                  |
| 36  | 'SWAZILAND'                                 | ESWATINI                  |
| 37  | 'SYRIAN ARAB REPUBLIC'                      | SYRIA                     |
| 38  | 'TANGANYIKA'                                | TANZANIA                  |
| 39  | 'THE FORMER YUGOSLAV REPUBLIC OF MACEDONIA' | NORTH MACEDONIA           |
| 40  | 'TÜRKİYE'                                   | TURKIYE                   |
| 41  | 'TURKEY'                                    | TURKIYE                   |
| 42  | 'UKRAINIAN SSR'                             | UKRAINE                   |
| 43  | 'UNION OF SOUTH AFRICA'                     | SOUTH AFRICA              |
| 44  | 'UNITED REPUBLIC OF CAMEROON'               | CAMEROON                  |
| 45  | 'UNITED REPUBLIC OF TANZANIA'               | TANZANIA                  |
| 46  | 'UPPER VOLTA'                               | BURKINA FASO              |
| 47  | 'USSR'                                      | RUSSIA                    |
| 48  | 'VENEZUELA (BOLIVARIAN REPUBLIC OF)'        | VENEZUELA                 |
| 49  | 'VIET NAM'                                  | VIETNAM                   |
| 50  | 'ZAIRE'                                     | CONGO (DRC)               |
| 51  | 'ZANZIBAR'                                  | TANZANIA                  |

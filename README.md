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

**Egypt and Syria**

Egypt and Syria held separate UN Member State status until their unification as the United Arab Republic (UAR) on 1 February 1958.

A total of 244 UNGA resolutions were passed from that time, up until Syria exited the UAR via a military coup on 28 September 1961. Of those 244 resolutions, votes were disclosed for just 65.

Following Syria's independence it reappeared as Syria on UNGA voting records; Egypt retained UAR as its official title until 1971, when it renamed itself as Egypt.

To achieve continuity of data for these two states, I have adopted the following policy:

- All UAR votes from 1958 to 1970 (308 total) are counted as votes by Egypt.
- All UAR votes from 1958 to 25/08/1961 (65 total) are additionally counted as votes by Syria.

The table below details the dates of these changes as visible in the voting records.

| #   | Date       | Resolution         | Description                                         |
| --- | ---------- | ------------------ | --------------------------------------------------- |
| 01  | 14/12/1957 | A/RES/1226(XII)    | Last pre-UAR vote in which Egypt and Syria appear   |
| 02  | 01/02/1958 | N/A                | UAR established                                     |
| 03  | 21/08/1958 | A/RES/1238(ES-III) | First appearance of UAR in place of Egypt and Syria |
| 04  | 28/09/1961 | N/A                | Syria declared independence following military coup |
| 05  | 23/10/1961 | A/RES/1627(XVI)    | Syria returns to record as voting UN Member State   |
| 06  | 17/12/1970 | A/RES/2750(XXV)[C] | Last vote with UAR recorded as a UN Member State    |
| 07  | 21/09/1971 | A/RES/2753(XXVI)   | Egypt returns to record as voting UN Member State   |

**Tanzania**

Tanzania was taken as another special case: Tanganyika and Zanzibar gained independence in 1961 and 1963, respectively, and in 1964 they merged to become the United Republic of Tanzania.

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

| #   | Name on UNGA voting Record                  | Name used in this dataset | Note                         |
| --- | ------------------------------------------- | ------------------------- | ---------------------------- |
| 01  | 'BOLIVIA (PLURINATIONAL STATE OF)'          | BOLIVIA                   |                              |
| 02  | 'BRUNEI DARUSSALAM'                         | BRUNEI                    |                              |
| 03  | 'BURMA'                                     | MYANMAR                   |                              |
| 04  | 'BYELORUSSIAN SSR'                          | BELARUS                   |                              |
| 05  | 'CABO VERDE'                                | CAPE VERDE                |                              |
| 06  | 'CENTRAL AFRICAN EMPIRE'                    | CENTRAL AFRICAN REPUBLIC  |                              |
| 07  | 'CEYLON'                                    | SRI LANKA                 |                              |
| 08  | 'CONGO'                                     | CONGO (ROC)               |                              |
| 09  | 'CONGO (BRAZZAVILLE)'                       | CONGO (ROC)               |                              |
| 10  | 'CONGO (DEMOCRATIC REPUBLIC OF)'            | CONGO (DRC)               |                              |
| 11  | 'CONGO (LEOPOLDVILLE)'                      | CONGO (DRC)               |                              |
| 12  | '"CÔTE D\'IVOIRE"'                          | IVORY COAST               |                              |
| 13  | '"COTE D\'IVOIRE"'                          | IVORY COAST               |                              |
| 14  | 'CZECH REPUBLIC'                            | CZECHIA                   |                              |
| 15  | 'DAHOMEY'                                   | BENIN                     |                              |
| 16  | 'DEMOCRATIC KAMPUCHEA'                      | CAMBODIA                  |                              |
| 17  | '"DEMOCRATIC PEOPLE\'S REPUBLIC OF KOREA"'  | NORTH KOREA               |                              |
| 18  | 'DEMOCRATIC REPUBLIC OF THE CONGO'          | CONGO (DRC)               |                              |
| 19  | 'GERMAN DEMOCRATIC REPUBLIC'                | EAST GERMANY              |                              |
| 20  | 'GERMANY, FEDERAL REPUBLIC OF'              | GERMANY                   |                              |
| 21  | 'KHMER REPUBLIC'                            | CAMBODIA                  |                              |
| 22  | 'IRAN (ISLAMIC REPUBLIC OF)'                | IRAN                      |                              |
| 23  | '"LAO PEOPLE\'S DEMOCRATIC REPUBLIC"'       | LAOS                      |                              |
| 24  | '"LAO PEOPLE\'s DEMOCRATIC REPUBLIC"'       | LAOS                      |                              |
| 25  | 'LAO'                                       | LAOS                      |                              |
| 26  | 'LIBYAN ARAB JAMAHIRIYA'                    | LIBYA                     |                              |
| 27  | 'LIBYAN ARAB REPUBLIC'                      | LIBYA                     |                              |
| 28  | 'MALDIVE ISLANDS'                           | MALDIVES                  |                              |
| 29  | 'MICRONESIA (FEDERATED STATES OF)'          | MICRONESIA                |                              |
| 30  | 'PHILIPPINE REPUBLIC'                       | PHILIPPINES               |                              |
| 31  | 'REPUBLIC OF KOREA'                         | SOUTH KOREA               |                              |
| 32  | 'REPUBLIC OF MOLDOVA'                       | MOLDOVA                   |                              |
| 33  | 'RUSSIAN FEDERATION'                        | RUSSIA                    |                              |
| 34  | 'SAINT CHRISTOPHER AND NEVIS'               | ST KITTS AND NEVIS        |                              |
| 35  | 'SIAM'                                      | THAILAND                  |                              |
| 36  | 'SURINAM'                                   | SURINAME                  |                              |
| 37  | 'SWAZILAND'                                 | ESWATINI                  |                              |
| 38  | 'SYRIAN ARAB REPUBLIC'                      | SYRIA                     |                              |
| 39  | 'TANGANYIKA'                                | TANZANIA                  | See "Tanzania", above        |
| 40  | 'THE FORMER YUGOSLAV REPUBLIC OF MACEDONIA' | NORTH MACEDONIA           |                              |
| 41  | 'TÜRKİYE'                                   | TURKIYE                   |                              |
| 42  | 'TURKEY'                                    | TURKIYE                   |                              |
| 43  | 'UKRAINIAN SSR'                             | UKRAINE                   |                              |
| 44  | 'UNION OF SOUTH AFRICA'                     | SOUTH AFRICA              |                              |
| 45  | 'UNITED ARAB REPUBLIC'                      | EGYPT                     | See "Egypt and Syria", above |
| 46  | 'UNITED REPUBLIC OF CAMEROON'               | CAMEROON                  |                              |
| 47  | 'UNITED REPUBLIC OF TANZANIA'               | TANZANIA                  |                              |
| 48  | 'UPPER VOLTA'                               | BURKINA FASO              |                              |
| 49  | 'USSR'                                      | RUSSIA                    |                              |
| 50  | 'VENEZUELA (BOLIVARIAN REPUBLIC OF)'        | VENEZUELA                 |                              |
| 51  | 'VIET NAM'                                  | VIETNAM                   |                              |
| 52  | 'ZAIRE'                                     | CONGO (DRC)               |                              |
| 53  | 'ZANZIBAR'                                  | TANZANIA                  | See "Tanzania", above        |

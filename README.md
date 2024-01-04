# UN General Assembly resolutions

### Acknowledgement

This repo makes use of data obtained with the approval of the UN Digital Library (Dag Hammarskjöld Library), and is © United Nations, 2023, https://digitallibrary.un.org, downloaded on 3 January 2024.

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

**Yemen**

The Yemen Arab Republic assumed UN Member Status and first appears on voting records as "Yemen" in 1947. Between 1967 and 1990, the state of the People's Democratic Republic of Yemen emerged and maintained distinct UN membership.

From 14/12/1967 to 17/12/1970, the latter state was entered on UNGA voting records as "Southern Yemen" and from 21/09/1971 to 29/12/1989 as "Democratic Yemen". The two entities reuinited as one state in 1990.

The voting records for Southern Yemen and Democratic Yemen have been merged under the name "Yemen (PDR)". The voting records for Yemen and Yemen PDR are distinct, and have not been merged.

**Dissolved states**

Unless otherwise stated, I have not attempted to consolidate data relating to former member states that dissolved into two or more subsequent member states.

Examples in this category include the Federation of Malaya, which became today's Malaysia and Singapore; and Yugoslavia, which dissolved into several sovereign member states during the 1990s.

**Conversion table**

A full list of name conversions is contained within the table below; the second column contains member state names exactly as obtained from the original dataset.

Finally, the conversions in the third column have been made based on the principles outlined above, and are not reflective of any political stance. Should any of these conversions be in error, corrections are welcome.

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
| 19  | 'DEMOCRATIC YEMEN'                          | YEMEN (PDR)               | See "Yemen", above           |
| 20  | 'GERMAN DEMOCRATIC REPUBLIC'                | EAST GERMANY              |                              |
| 21  | 'GERMANY, FEDERAL REPUBLIC OF'              | GERMANY                   |                              |
| 22  | 'KHMER REPUBLIC'                            | CAMBODIA                  |                              |
| 23  | 'IRAN (ISLAMIC REPUBLIC OF)'                | IRAN                      |                              |
| 24  | '"LAO PEOPLE\'S DEMOCRATIC REPUBLIC"'       | LAOS                      |                              |
| 25  | '"LAO PEOPLE\'s DEMOCRATIC REPUBLIC"'       | LAOS                      |                              |
| 26  | 'LAO'                                       | LAOS                      |                              |
| 27  | 'LIBYAN ARAB JAMAHIRIYA'                    | LIBYA                     |                              |
| 28  | 'LIBYAN ARAB REPUBLIC'                      | LIBYA                     |                              |
| 29  | 'MALDIVE ISLANDS'                           | MALDIVES                  |                              |
| 30  | 'MICRONESIA (FEDERATED STATES OF)'          | MICRONESIA                |                              |
| 31  | 'NETHERLANDS (KINGDOM OF THE)'              | NETHERLANDS               |                              |
| 32  | 'PHILIPPINE REPUBLIC'                       | PHILIPPINES               |                              |
| 33  | 'REPUBLIC OF KOREA'                         | SOUTH KOREA               |                              |
| 34  | 'REPUBLIC OF MOLDOVA'                       | MOLDOVA                   |                              |
| 35  | 'RUSSIAN FEDERATION'                        | RUSSIA                    |                              |
| 36  | 'SAINT CHRISTOPHER AND NEVIS'               | SAINT KITTS AND NEVIS     |                              |
| 37  | 'SIAM'                                      | THAILAND                  |                              |
| 38  | 'SOUTHERN YEMEN'                            | YEMEN (PDR)               | See "Yemen", above           |
| 39  | 'SURINAM'                                   | SURINAME                  |                              |
| 40  | 'SWAZILAND'                                 | ESWATINI                  |                              |
| 41  | 'SYRIAN ARAB REPUBLIC'                      | SYRIA                     |                              |
| 42  | 'TANGANYIKA'                                | TANZANIA                  | See "Tanzania", above        |
| 43  | 'THE FORMER YUGOSLAV REPUBLIC OF MACEDONIA' | NORTH MACEDONIA           |                              |
| 44  | 'TÜRKİYE'                                   | TURKIYE                   |                              |
| 45  | 'TURKEY'                                    | TURKIYE                   |                              |
| 46  | 'UKRAINIAN SSR'                             | UKRAINE                   |                              |
| 47  | 'UNION OF SOUTH AFRICA'                     | SOUTH AFRICA              |                              |
| 48  | 'UNITED ARAB REPUBLIC'                      | EGYPT                     | See "Egypt and Syria", above |
| 49  | 'UNITED REPUBLIC OF CAMEROON'               | CAMEROON                  |                              |
| 50  | 'UNITED REPUBLIC OF TANZANIA'               | TANZANIA                  |                              |
| 51  | 'UPPER VOLTA'                               | BURKINA FASO              |                              |
| 52  | 'USSR'                                      | RUSSIA                    |                              |
| 53  | 'VENEZUELA (BOLIVARIAN REPUBLIC OF)'        | VENEZUELA                 |                              |
| 54  | 'VIET NAM'                                  | VIETNAM                   |                              |
| 55  | 'ZAIRE'                                     | CONGO (DRC)               |                              |
| 56  | 'ZANZIBAR'                                  | TANZANIA                  | See "Tanzania", above        |

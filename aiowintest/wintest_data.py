CONTEST_ID = {
    1: 'IARU_VHF',
    2: 'IARU_UHF',
    3: 'IARU_CW',
    4: 'IARU_HF',
    5: 'IARU_R1_50MHZ',
    10: 'REF_THF',
    11: 'REF_DDFM_50MHZ',
    20: 'THF_EU',
    21: 'THF_EU_50_70',
    30: 'THF_EU_GRIDSQUARE',
    31: 'THF_EU_GRIDSQUARE_50_70',
    32: 'THF_EU_GRIDSQUARE_NO_DIST',
    33: 'THF_EU_GRIDSQUARE_NO_DIST_50_70',
    100: 'REF_HF',
    101: 'ARRL_DX',
    102: 'ARRL_10',
    103: 'ARRL_160',
    104: 'ARRL_SWEEPSTAKES',
    105: 'ARRL_FD',
    106: 'ARRL_RU',
    130: 'ARRL_UHF_AUG',
    131: 'ARRL_VHF_JAN',
    132: 'ARRL_VHF_JUN',
    133: 'ARRL_VHF_SEP',
    150: 'REF_160',
    200: 'CQWW_DX',
    201: 'CQWW_WPX',
    202: 'CQWW_160',
    250: 'CQWW_VHF',
    300: 'RDXC',
    301: 'RDAC',
    302: 'CIS',
    303: 'R_160',
    304: 'RRTC',
    400: 'DXPEDITION_HF',
    410: 'DXPEDITION_VHF',
    500: 'ALL_ASIAN',
    600: 'SPDXC',
    700: 'JIDX',
    701: 'KCJ',
    702: 'KCJ_TOPBAND',
    800: 'YUDXC',
    900: 'CQM',
    1000: 'ARI',
    1001: 'ARI_SEZIONI',
    1002: 'ARI_40_80',
    1100: 'BALTIC',
    1200: 'KING_OF_SPAIN',
    1300: 'IOTA',
    1301: 'RSGB_160',
    1302: 'RSGB_80_CC',
    1303: 'RSGB_CMW',
    1304: 'RSGB_15_10',
    1305: 'RSGB_AFS',
    1400: 'WAEDC',
    1401: 'WAG',
    1402: 'DARC_XMAS',
    1403: 'DARC_10',
    1500: 'YODXC',
    1600: 'EU_HF',
    1601: 'SCC',
    1700: 'OCDXC',
    1800: 'TOECC',
    1900: 'SAC',
    1901: 'NRAU_BALTIC',
    1902: 'NAC',
    1903: 'SARTG',
    2000: 'QP_TX',
    2100: 'EU_SPRINT',
    2200: 'UKDXC',
    2300: 'OKOMDXC',
    2400: 'STEW_PERRY',
    2401: 'GACW_DX',
    2402: 'NINE_KCC_15',
    2403: 'FOC_MARATHON',
    2404: 'LOTW',
    2405: 'AP_SPRINT',
    2406: 'JARTS',
    2407: 'MARCONI_HF',
    2500: 'LZDX',
    2600: 'CROATIAN_CW',
    2700: 'UBADX',
    2701: 'UBA_SPRING_80M',
    2702: 'UBA_SPRING_6M',
    2703: 'UBA_SPRING_2M',
    2704: 'ON_80M',
    2705: 'ON_6M',
    2706: 'ON_2M',
    2800: 'RAC_DAY',
    2801: 'RAC_WINTER',
    2900: 'PACC',
    3000: 'HELVETIA',
    3001: 'HELVETIA_VHF',
    3100: 'IARU_FD_R1_GENERIC',
    3101: 'IARU_FD_R1_DARC',
    3102: 'IARU_FD_R1_RSGB',
    3200: 'UFT_HF',
    3300: 'AGCW_HNY',
    3400: 'HA_DX',
    3500: 'NAQP',
    3501: 'NA_SPRINT',
    3600: 'NCCC_SPRINT',
    3700: 'CQIR',
}

MODECATEGORY_ID = {
    0: 'CW',
    1: 'PHONE',
    2: 'MIXED',
    3: 'RTTY',
    4: 'DIGITAL',
    5: 'ALL',
}

CATEGORY_ID = {
    1: 'SINGLE_OP',
    2: 'SINGLE_OP_ASSISTED',
    3: 'MULTI_SINGLE',
    4: 'MULTI_TWO',
    5: 'MULTI_MULTI',
    6: 'ROVER_STATION',
    7: 'MARITIME_MOBILE',
    8: 'MOBILE_STATION',
    9: 'SCHOOL_CLUB',
}

OVERLAY_ID = {
    1: 'NONE',
    2: 'CLUB',
    3: 'ROOKIE',
    4: 'BAND',
    5: 'TB',
    6: 'HQ',
    7: 'DXPEDITION',
    8: 'OPEN',
    9: 'RESTRICTED',
    10: 'QRP',
    11: 'FIXED',
    12: 'WRTC',
}

POWERCLASS_ID = {
    0: 'HIGH',
    1: 'LOW',
    2: 'QRP',
}

HEADER_ID = {
    1: 'BAND',
    2: 'MODE_SSB',
    3: 'MODE_CW',
    4: 'MODE_ALL',
    5: 'QSO',
    6: 'DUPE',
    7: 'ITU',
    8: 'CQ',
    9: 'HQ',
    10: 'DXCC',
    11: 'DEPARTEMENT',
    12: 'MULTS',
    13: 'LOCATOR',
    14: 'POINTS',
    15: 'AVG',
    16: 'AVG_PTS',
    17: 'AVG_KMS',
    18: 'TOTAL',
    19: 'FINAL_SCORE',
    20: 'OBLAST',
    21: 'MODE_RTTY',
    22: 'MODE_DIGITAL',
    23: 'SECTION',
    24: 'PROVINCE',
    25: 'PREFECTURE',
    26: 'MODE_OTHERS',
    27: 'TOTAL_QSO',
    28: 'PREFIX',
    29: 'P150C',
    30: 'IOTA',
    31: 'IOTA_SSB',
    32: 'IOTA_CW',
    33: 'COUNTY',
    34: 'YEAR',
    35: 'QTC',
    36: 'RDA',
    37: 'QSO_PHONE',
    38: 'QSO_CW',
    39: 'DXCC_PHONE',
    40: 'DXCC_CW',
    41: 'STATE_PHONE',
    42: 'STATE_CW',
    43: 'COUNTY_PHONE',
    44: 'COUNTY_CW',
    45: 'EEC',
    46: 'PROV_PHONE',
    47: 'PROV_CW',
    48: 'DISTRICT',
    49: 'BONUS',
    50: 'CANTON',
    51: 'CIS',
    52: 'DOK',
    53: 'CONTINENT',
    54: 'STATES_PROVINCES',
    55: 'RRTC',
}

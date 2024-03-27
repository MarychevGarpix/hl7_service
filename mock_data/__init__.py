from mock_data.types import TStructureData

STRUCTURE_DATA: TStructureData = {
    'EXPIRATORY_TIME': 'Texp',
    'INSPIRATORY_TIME': 'Tinsp',
    'END_TIDAL_CO2': 'EtCO2',
    'PLATEAU_PRESSURE': 'Pplat',
    'MEAN_PRESSURE': 'Pmean',
    'MINUTE_VOLUME': 'Volume',
    'TIDAL_VOLUME': 'Vt',
    'RESPIRATORY_RATE_MANDATORY': 'RRmand',
    '?': 'f',
    'REAL_TIME_FIO2_FILTERED_2_HZ': 'FiO2',
    'RESPIRATORY_RATE_SPONTANEOUS': 'RRspon',
    'POSITIVE_END_EXPIRATORY_PRESSURE_0409': 'PEEP',
    '??': 'PPS.C',
    'PATIENT_VOLUME': 'Ppeak',
}


'''
Дыхательный объем    = Vt         = TIDAL_VOLUME
Минутный объем       = Volume     = MINUTE_VOLUME
PEEP                 = PEEP       = POSITIVE_END_EXPIRATORY_PRESSURE_0409
Pmean                = Pmean      = MEAN_PRESSURE
Pplat                = Pplat      = PLATEAU_PRESSURE
Ppeak                = Ppeak      = PATIENT_VOLUME
Отношение вдох:выдох = Tinsp|Texp = INSPIRATORY_TIME|EXPIRATORY_TIME
Compliance           = PPS.C      = PPS_COMPLIANCE
FiO2 (%)             = FiO2 (%)   = REAL_TIME_FIO2_FILTERED_2_HZ
ЧД общая             = RRtotal    = RESPIRATORY_RATE_TOTAL
ЧД мех               = RRmand     =  RESPIRATORY_RATE_MANDATORY
ЧД спонтанная        = RRspon     = RESPIRATORY_RATE_SPONTANEOUS
etCO2 (мм рт ст)     = EtCO2      = END_TIDAL_CO2 # Capnograph
Поток О2             = ...        = OXYGEN_FLOW_FILTERED... | OXYGEN_FLOW_SENSOR_VALUE  
Поток воздуха        = ...        = AIR_FLOW_SENSOR_VALUE  |  AIR_FLOW_FILTERED_10_HZ 
Расход O2            = ...        = PERCENTAGE_O2
Расход воздуха       = ...        = STROKEWISE_FIO2 | AIR_FLOW_FILTERED_10_HZ
'''
### Database
- Discussion with mentor
  - Data is unclassified, can use public cloud
  - Current challenge deals with static data
  - Needs to support ad hoc query by a small number of scientists
  - Data comes in as a stream
    - Few concurrent reads
    - Large amount of sequential writes
    - Approximately 5 GB/day
  - Long term would like real time stream processing capabilities
  - Public read permission
    - Write permission only for data importer
  - Once per day batch update to database
  - Data does not have to be updated once written

#### Azure Table Store
- Streaming: Azure Stream Analytics
  - SQL like query language
  - User defined functions with Javascript or C#
- Ad Hoc data analysis with Power BI

#### Azure SQL Serverless
- PowerBI
- R via ODBC driver
- Can PowerBI handle geo-queries?

### Data
- 7,400,731 lines
- 9 fields per record
- libais can correctly parse the whole dataset
- min 22 fields
  - {'cog',
    'id',
    'mmsi',
    'nav_status',
    'position_accuracy',
    'raim',
    'repeat_indicator',
    'rot',
    'rot_over_range',
    'slot_offset',
    'slot_timeout',
    'sog',
    'spare',
    'special_manoeuvre',
    'sync_state',
    'tagblock_C',
    'tagblock_station',
    'tagblock_timestamp',
    'timestamp',
    'true_heading',
    'x',
    'y'}
- 133 unique fields in parsed record
  - {'eta_hour', 'position_accuracy', 'text', 'wind_ave', 'aton_status', 'air_pres_trend', 'length', 'year', 'tagblock_station', 'txrx_mode', 'swell_period', 'precip_type', 'cur_dir_3', 'raim', 'dim_a', 'spare2', 'surf_cur_speed', 'callsign', 'second', 'ship_type', 'dim_b', 'day', 'reservations', 'beam', 'wind_gust', 'swell_height', 'interval_raw', 'hour', 'air_temp', 'dte', 'fix_type', 'cur_speed_3', 'received_stations', 'aton_type', 'salinity', 'utc_hour', 'type_and_cargo', 'utc_spare', 'seq', 'mmsi_dest', 'water_level_trend', 'ice', 'dsc_flag', 'water_temp', 'virtual_aton', 'quiet', 'reports', 'slot_increment', 'part_num', 'wave_height', 'month', 'dim_c', 'destination', 'rel_humid', 'ais_version', 'ack_required', 'sog', 'minute', 'repeat_indicator', 'mode_flag', 'sync_state', 'dest_mmsi', 'haz_cargo', 'wind_gust_dir', 'cur_depth_3', 'utc_day', 'timestamp', 'spare', 'course_qual', 'spare3', 'tagblock_timestamp', 'assigned_mode', 'imo_num', 'mmsi', 'eu_id', 'dac', 'water_level', 'slot_timeout', 'cur_depth_2', 'utc_min', 'eta_minute', 'wave_period', 'off_pos', 'station_type', 'm22_flag', 'id', 'wind_dir', 'tagblock_C', 'cur_dir_2', 'sea_state', 'eta_day', 'horz_vis', 'cog', 'slot_number', 'transmission_ctl', 'x2', 'cur_speed_2', 'true_heading', 'unit_flag', 'speed_qual', 'name', 'heading_qual', 'band_flag', 'dew_point', 'display_flag', 'dim_d', 'slot_offset', 'rot_over_range', 'nav_status', 'msg_seq', 'air_pres', 'rot', 'vendor_id', 'y1', 'ext_water_level', 'slots_to_allocate', 'eta_month', 'loaded', 'acks', 'surf_cur_dir', 'x', 'commstate_flag', 'x1', 'commstate_cs_fill', 'retransmit', 'keep_flag', 'swell_dir', 'y2', 'fi', 'y', 'draught', 'wave_dir', 'special_manoeuvre'}
  - Any given record may not have all of these

### Data Usage
- How is the data to be used?
  - Real time?
  - How many users expected?
  - What kind of queries (fixed or ad hoc)
- Only be concerned with terrestrial data
- Requirements DFO
  - Near real time snapshots
  - Individual vessel characteristics and tracks over hours, days, weeks
  - Seasonal variations
- Data products
  - Vessel densities
  - Environment usage
  - Vessel tracks
  - Vessel speed
  - Seasonal, annual statistics
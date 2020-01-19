# from google.cloud import bigquery
# from google.cloud.bigquery.client import Client
# import os
#
#
# class googleBigqueryHelper:
#     def __init__(self):
#         os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/junzheng/aisServer-46393937c62b.json"
#         print('Credendtials from environ: {}'.format(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')))
#         self.client = Client()
#         self.projectName = self.client.project
#         self.datasetName = "%s.aisDatasetTest" % self.projectName
#
#     def create_dataset(self):
#         dataset = bigquery.Dataset(self.datasetName)
#         # TODO(developer): Specify the geographic location where the dataset should reside.
#         dataset.location = "US"
#         # Send the dataset to the API for creation.
#         # Raises google.api_core.exceptions.Conflict if the Dataset already
#         # exists within the project.
#         dataset = self.client.create_dataset(dataset)  # Make an API request.
#         print("Created dataset {}.{}".format(self.client.project, dataset.dataset_id))

    # def create_table(self):
    #     schema = [
    #         bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
    #         bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
    #     ]
    #
    #     table = bigquery.Table(table_id, schema=schema)
    #     table = self.client.create_table(table)  # Make an API request.
    #     print(
    #         "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
    #     )

from google.cloud import storage
import os
from datetime import datetime
from google.cloud import bigquery
import json
import parse

class aisServer:
    def __init__(self):
        self.storage_client = storage.Client()
        self.bigquery_client = bigquery.Client()

        self.dataset = list(self.bigquery_client.list_datasets())[0]  # Make an API request.
        self.project = self.bigquery_client.project
        self.bucket_input = "candev-ais"
        self.bucket_output = "candev-ais-output"
        self.output_blob = "out.json"
        self.table_name = "aisTable"
        self.schemas = ['second', 'mmsi', 'cur_speed_2', 'imo_num', 'virtual_aton', 'haz_cargo', 'year', 'keep_flag', 'aton_type',
             'ack_required', 'ext_water_level', 'wind_ave', 'nav_status', 'quiet', 'unit_flag', 'timestamp', 'id',
             'callsign', 'course_qual', 'retransmitted', 'swell_period', 'horz_vis', 'spare2', 'reports', 'salinity',
             'interval_raw', 'water_level', 'beam', 'utc_day', 'repeat_indicator', 'fix_type', 'fi', 'cur_dir_2', 'x2',
             'utc_hour', 'slot_offset', 'spare', 'dew_point', 'ai_available', 'reservations', 'y2', 'length',
             'water_level_trend', 'water_temp', 'dest_mmsi', 'slot_increment', 'sync_state', 'tagblock_timestamp',
             'transmission_ctl', 'air_pres', 'acks', 'tagblock_C', 'ship_type', 'rel_humid', 'speed_qual', 'seq', 'day',
             'dac', 'rot_over_range', 'special_manoeuvre', 'slot_timeout', 'wave_dir', 'alt_sensor', 'wind_dir',
             'dsc_flag', 'display_flag', 'slot_number', 'air_pres_trend', 'wind_gust_dir', 'dim_b', 'eta_month',
             'assigned_mode', 'eu_id', 'slots_to_allocate', 'cur_speed_3', 'wave_period', 'x', 'swell_dir', 'wind_gust',
             'ice', 'retransmit', 'cog', 'txrx_mode', 'ack_dac', 'true_heading', 'sog', 'y1', 'destination',
             'commstate_cs_fill', 'aton_status', 'vendor_id', 'cur_depth_2', 'part_num', 'name', 'air_temp',
             'type_and_cargo', 'station_type', 'commstate_flag', 'wave_height', 'spare3', 'eta_hour', 'ai_response',
             'text', 'band_flag', 'mmsi_dest', 'surf_cur_dir', 'req_dac', 'precip_type', 'minute', 'off_pos', 'month',
             'sea_state', 'msg_seq', 'ack_fi', 'tagblock_station', 'dim_a', 'heading_qual', 'dte', 'draught',
             'ais_version', 'swell_height', 'dim_c', 'eta_minute', 'utc_spare', 'surf_cur_speed', 'cur_depth_3', 'y',
             'eta_day', 'received_stations', 'raim', 'utc_min', 'dim_d', 'req_fi', 'mode_flag', 'position_accuracy',
             'x1', 'm22_flag', 'hour', 'rot', 'loaded', 'seq_num', 'alt', 'cur_dir_3']

    def download_input(self):
        def sort_key(item):
            return -datetime.strptime(item.name.split('_')[-1].split('.')[0], "%Y-%m-%d").toordinal()
        blobs = self.storage_client.list_blobs(self.bucket_input)
        blobs = [blob for blob in blobs]
        blobs.sort(key=sort_key)
        self.latest_blob = blobs[0]
        self.input_file = self.latest_blob.name
        self.latest_blob.download_to_filename(self.input_file)
        print(self.input_file)
        print(os.path.exists(self.input_file))

    def upload_output(self):
        # print(filter_by_hour.write_json(self.input_file, self.output_blob))
        count = parse.write_json(self.input_file, 'temp.json')
        print(count)
        parse.write_speed('temp.json', self.output_blob)
        bucket = self.storage_client.get_bucket(self.bucket_output)
        blob = bucket.blob(self.output_blob)
        blob.upload_from_filename(self.output_blob)
        print('File {} uploaded to {}.'.format(self.output_blob, self.output_blob))
        os.remove(self.input_file)

    def wirte_query(self):
        job_config = bigquery.LoadJobConfig()
        job_config.autodetect = True
        job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
        try:
            self.bigquery_client.get_table(self.table_name)
            job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
        except:
            pass
        uri = "gs://%s/%s" % (self.bucket_output, self.output_blob)
        load_job = self.bigquery_client.load_table_from_uri(
            uri, self.dataset.table(self.table_name), job_config=job_config
        )  # API request
        print("Starting job {}".format(load_job.job_id))
        load_job.result()  # Waits for table load to complete.
        print("Job finished.")

        # destination_table = self.bigquery_client.get_table(self.dataset.table(self.table_name))
        # print("Loaded {} rows.".format(destination_table.num_rows))


if __name__ == '__main__':
    a = aisServer()
    a.download_input()
    a.upload_output()
    a.wirte_query()

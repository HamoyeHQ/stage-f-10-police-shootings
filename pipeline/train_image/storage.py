import os
import glob
from google.cloud import storage
import re
import logging


_GCS_PREFIX = "gs://"

class Storage(object):
    
    @classmethod
    def upload(cls, uri: str, out_dir: str = None) -> str:
        logging.info(f'copying contents from {uri} to {out_dir}')
        
        if out_dir.startswith(_GCS_PREFIX):
            cls._upload_gcs(uri, out_dir)
            
        else:
            raise Exception(f"cannot recognize storage type for {uri} \n {_GCS_PREFIX} is the only available storage type")
            
        logging.info(f'successfully copied {uri} to {out_dir}')
        return out_dir
    
    @classmethod
    def _upload_gcs(cls, uri: str, out_dir: str):
        try:
            storage_client = storage.Client()
        except exceptions.DefaultCredentialsError:
            storage_client = storage.Client().create_anonymous_client()
            
        bucket_args = out_dir.replace(_GCS_PREFIX, "", 1).split("/", 1)
        logging.info(f"Bucket arguments: {bucket_args}")
        bucket_name = bucket_args[0]
        gcs_path = bucket_args[1] if len(bucket_args) else ""
        bucket = storage_client.bucket(bucket_name)
        cls.upload_local_directory_to_gcs(uri, bucket, gcs_path)
        
        
    @classmethod
    def upload_local_directory_to_gcs(uri, bucket, gcs_path):
        assert os.path.isdir(local_path)
        for local_file in glob.glob(local_path + '/**'):
            if not os.path.isfile(local_file):
                cls.upload_local_directory_to_gcs(local_file, bucket, f'{gcs_path}/{os.path.basename(local_file)}')
                
            else:
                remote_path = os.path.join(gcs_path, local_file[len(local_path)+1 :])
                logging.info(f"Remote path: {remote_path}")
                blob = bucket.blob(remote_path)
                blob.upload_from_filename(local_file)
    
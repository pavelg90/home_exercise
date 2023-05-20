import streamlit as st
import boto3
import os

# Setup Minio connection
s3 = boto3.client('s3',
                  endpoint_url='http://host.docker.internal:333',
                  aws_access_key_id='minio',
                  aws_secret_access_key='minio123')

def upload_file(file):
    s3.upload_fileobj(file, 'mybucket', file.name)

file = st.file_uploader("Upload CSV file", type=['csv'])

if file is not None:
    upload_file(file)
    st.success('File uploaded successfully.')

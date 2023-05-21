from minio import Minio
from minio.error import S3Error
import time


def main():
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio(
        "s3_simulator",
        access_key="minio",
        secret_key="minio123",
    )

    # Make 'mybucket' bucket if not exist.
    if not client.bucket_exists("mybucket"):
        client.make_bucket("asiatrip")
    else:
        print("Bucket 'asiatrip' already exists")



if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print("error occurred.", e)

        time.sleep(1)

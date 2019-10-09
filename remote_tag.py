import os
import re
import requests
import sys

IMAGE_SOURCE = sys.argv[1]
IMAGE_DESTINATION = sys.argv[2]
TOKEN = os.environ['REGISTRY_AUTH']

HEADERS = {
    'Accept': 'application/vnd.docker.distribution.manifest.v2+json',
    'Authorization': 'Basic ' + TOKEN,
}

def extract_image_name(image_name):
    result = re.match(r'^(?P<registry>[^\/]+)/(?P<repository>.+):(?P<tag>.+)$', image_name)
    return (
        result.group('registry'),
        result.group('repository'),
        result.group('tag'),
    )

def get_tag_manifests_url(image_name):
    registry, repository, tag = extract_image_name(image_name)
    return 'https://{}/v2/{}/manifests/{}'.format(registry, repository, tag)

def get_manifest(image_name):
    url = get_tag_manifests_url(image_name)
    response = requests.get(url, headers=HEADERS)
    print('Get source tag manifest:', response.status_code)
    return response.content

def set_image_tag(source_image, destination_image):
    manifest = get_manifest(source_image)
    dest_url = get_tag_manifests_url(destination_image)

    response = requests.put(dest_url, headers=HEADERS, data=manifest)
    print('Set destination tag manifest:', response.status_code)

set_image_tag(IMAGE_SOURCE, IMAGE_DESTINATION)

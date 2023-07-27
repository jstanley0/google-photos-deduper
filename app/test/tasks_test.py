import pytest
import app.tasks
import app.config
import requests
import mongomock
from app.lib.duplicate_image_detector import DuplicateImageDetector
from app.lib.google_api_client import GoogleApiClient
from app.models.media_items_repository import MediaItemsRepository
from unittest.mock import Mock


# TODO: mongomock.patch doesn't seem to work - maybe it's the celery worker?
# @mongomock.patch(servers="mongodb://mongotest:27017/")
# @mongomock.patch(servers=(("mongotest", 27017),))
# @pytest.mark.skip(reason="TODO: times out even though worker has finished.")
def test_process_duplicates(
    mocker, celery_app, celery_worker, credentials, user_info, media_item
):
    print(f"app.config.MONGODB_URI: {app.config.MONGODB_URI}")
    print(f"app.config.DATABASE: {app.config.DATABASE}")

    p = mocker.patch.multiple(
        "app.lib.google_photos_client.GooglePhotosClient",
        get_user_info=Mock(return_value=user_info),
        local_media_items_count=Mock(return_value=0),
        fetch_media_items=Mock(return_value=None),
        get_local_media_items=Mock(return_value=[media_item]),
    )
    p2 = mocker.patch.multiple(
        "app.lib.duplicate_image_detector.DuplicateImageDetector",
        calculate_clusters=Mock(return_value=[[0]]),
    )

    async_result = app.tasks.process_duplicates.delay(
        credentials=credentials,
        refresh_media_items=True,
    )
    result = async_result.get()

    assert "groups" in result
    assert len(result["groups"]) == 1
    assert "media_items" in result["groups"][0]
    assert len(result["groups"][0]["media_items"]) == 1
    assert (
        result["groups"][0]["media_items"][0].items()
        >= {"id": media_item["id"]}.items()
    )
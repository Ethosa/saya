# -*- coding: utf-8 -*-
# author: Ethosa
from typing import Dict, Any, Union, Optional, Literal, List


class UnsupportedResponseFormat(Exception):
    pass


class Uploader:
    def __init__(self, vk):
        """Initializes new Uploader object.
        """
        self.session = vk.session
        self.call_method = vk.call_method
        self.logger = vk.logger

    def album_photo(
            self,
            files: Union[str, List[str]],
            album_id: int,
            group_id: Optional[int] = None,
            caption: str = ""
    ) -> Dict[str, Any]:
        """Uploads photo in album

        :param files: file path, file paths, file as bytes or files as bytes
        :param album_id: album ID.
        :param group_id: group ID.
        :param caption: photo caption
        """
        data = {
            "album_id": album_id
        }
        if group_id:
            data["group_id"] = group_id

        response = self._upload_files(data, files, "photos.getUploadServer")

        data["caption"] = caption
        data["server"] = response["server"]
        data["hash"] = response["hash"]
        data["photos_list"] = response["photos_list"]

        return self.call_method("photos.save", data)

    def audio(
            self,
            files: Union[str, List[str]],
            artist: str = "",
            title: str = ""
    ) -> Dict[str, Any]:
        """Uploads audio file

        :param files: file path, file paths, file as bytes or files as bytes
        :param artist: songwriter. The default is taken from ID3 tags.
        :param title: name of the composition. The default is taken from ID3 tags.
        """
        response = self._upload_files({}, files, "audio.getUploadServer")
        data = {
            "server": response["server"],
            "audio": response["audio"],
            "hash": response["hash"]
        }

        for field_name, value in (("artist", artist), ("title", title)):
            if value:
                data[field_name] = value

        return self.call_method("audio.save", data)

    def chat_photo(
            self,
            files: Union[str, List[str]],
            chat_id: int,
            crop_x: Optional[int] = None,
            crop_y: Optional[int] = None,
            crop_width: Optional[int] = None
    ) -> Dict[str, Any]:
        """Uploads chat photo

        :param files: file path, file paths, file as bytes or files as bytes
        :param chat_id: id of the conversation for which you want to upload a photo
        :param crop_x: x coordinate for cropping the photo (upper right corner).
        :param crop_y: y coordinate for cropping the photo (upper right corner).
        :param crop_width: Width of the photo after cropping in px.
        """
        data = {"chat_id": chat_id}
        if crop_x:
            data["crop_x"] = crop_x
        if crop_y:
            data["crop_y"] = crop_y
        if crop_width:
            data["crop_width"] = crop_width

        response = self._upload_files(
            data, files, "photos.getChatUploadServer")

        data = {"file": response["response"]}

        return self.call_method("messages.setChatPhoto", data)

    def cover_photo(
            self,
            files: Union[str, List[str]],
            group_id: int,
            crop_x: int = 0,
            crop_y: int = 0,
            crop_x2: int = 795,
            crop_y2: int = 200
    ) -> Dict[str, Any]:
        """Updates group cover photo

        :param files: file path, file paths, file as bytes or files as bytes
        :param group_id: community id.
        :param crop_x: X coordinate of the upper left corner to crop the image.
        :param crop_y: Y coordinate of the upper left corner to crop the image.
        :param crop_x2: X coordinate of the lower right corner to crop the image.
        :param crop_y2: Y coordinate of the lower right corner to crop the image.
        """
        data = {
            "group_id": group_id,
            "crop_x": crop_x,
            "crop_y": crop_y,
            "crop_x2": crop_x2,
            "crop_y2": crop_y2
        }

        response = self._upload_files(
            data, files, "photos.getOwnerCoverPhotoUploadServer")
        data = {
            "hash": response["hash"],
            "photo": response["photo"]
        }

        return self.call_method("photos.saveOwnerCoverPhoto", data)

    def document(
            self,
            files: Union[str, List[str]],
            group_id: Optional[int] = None,
            title: str = "",
            tags: str = "",
            return_tags: int = 0,
            is_wall: bool = False
    ) -> Dict[str, Any]:
        """Uploads document

        :param files: file path, file paths, file as bytes or files as bytes
        :param group_id: community identifier (if you need to upload a document to the list of community documents).
        :param title: document's name.
        :param tags: tags for search.
        :param is_wall: upload document in wall?
        """
        data = {}
        if group_id:
            data["group_id"] = group_id

        response = self._upload_files(
            data, files,
            "docs.get%sUploadServer" % ("Wall" if is_wall else "")
        )
        data = {
            "file": response["file"],
            "title": title,
            "tags": tags,
            "return_tags": return_tags
        }

        return self.call_method("docs.save", data)

    def document_message(
            self,
            files,
            peer_id,
            doc_type="doc",
            title="",
            tags="",
            return_tags=0
    ) -> Dict[str, Any]:
        """Uploads document in message.

        :param files: file path, file paths, file as bytes or files as bytes
        :param peer_id:  destination identifier.
        :param doc_type:  type of document. Possible values: doc, audio_message
        :param title:  document's name.
        :param tags:  tags for search.
        """
        data = {
            "peer_id": peer_id,
            "type": doc_type
        }

        response = self._upload_files(
            data, files, "docs.getMessagesUploadServer"
        )
        self.logger.debug(response)
        data = {
            "file": response["file"],
            "title": title,
            "tags": tags,
            "return_tags": return_tags
        }

        return self.call_method("docs.save", data)

    @staticmethod
    def format(
            response,
            formtype: Literal[
                'photo', 'video',
                'audio', 'doc', 'graffiti'
            ] = 'photo'
    ) -> str:
        """response formatting

        :param response: response after object saved
        """
        if isinstance(response, dict):
            response = response.get("response", response)
        if isinstance(response, dict):
            response = response.get("type", response)

        if isinstance(response, dict):
            if "owner_id" in response and "id" in response:
                return (
                    "%s%s_%s" % (formtype, response["owner_id"], response["id"])
                )
        elif isinstance(response, list):
            objs = []
            for obj in response:
                if "owner_id" in obj and "id" in obj:
                    objs.append(
                        "%s%s_%s" % (formtype, obj["owner_id"], obj["id"])
                    )
            return ",".join(objs)
        raise UnsupportedResponseFormat

    def message_photo(
            self,
            files: Union[str, List[str]],
            peer_id: int,
            group_id: int = 0
    ) -> Dict[str, Any]:
        """Uploads photo in message

        :param files: file path, file paths, file as bytes or files as bytes
        :param peer_id: destination identifier (for uploading photos in community posts).
        """
        data = {"peer_id": peer_id} if group_id else {}

        response = self._upload_files(
            data, files, "photos.getMessagesUploadServer"
        )

        data["server"] = response["server"]
        data["hash"] = response["hash"]
        data["photo"] = response["photo"]

        return self.call_method("photos.saveMessagesPhoto", data)

    def market_photo(
            self,
            files: Union[str, List[str]],
            group_id: int,
            main_photo: Optional[int] = None,
            crop_x: Optional[int] = None,
            crop_y: Optional[int] = None,
            crop_width: Optional[int] = None
    ) -> Dict[str, Any]:
        """upload product photo

        Allowed formats: JPG, PNG, GIF.
        Limitations: the minimum photo size is 400x400px,
        the sum of the height and width is no more than 14000px,
        the file is no more than 50 MB in size, and the aspect ratio is at least 1:20.

        :param files: file path, file paths, file as bytes or files as bytes
        :param group_id Community id for which you want to upload a product photo.
        :param main_photo: whether the photo is the cover
                           of the product (1 - cover photo, 0 - additional photo)
        :param crop_x: x coordinate for cropping the photo (upper right corner).
        :param crop_y: y coordinate for cropping the photo (upper right corner).
        :param crop_width: Width of the photo after cropping in px.
        """
        data = {"group_id": group_id}
        if crop_x:
            data["crop_x"] = crop_x
        if crop_y:
            data["crop_y"] = crop_y
        if crop_width:
            data["crop_width"] = crop_width
        if main_photo:
            data["main_photo"] = main_photo

        response = self._upload_files(
            data, files, "photos.getMarketUploadServer"
        )

        data = {
            "group_id": group_id,
            "server": response["server"],
            "hash": response["hash"],
            "photo": response["photo"],
            "crop_data": response["crop_data"],
            "crop_hash": response["crop_hash"]
        }

        return self.call_method("photos.saveMarketPhoto", data)

    def market_album_photo(
            self,
            files: Union[str, List[str]],
            group_id: int
    ) -> Dict[str, Any]:
        """Uploading photos for a selection of goods

        Allowed formats: JPG, PNG, GIF.
        Limitations: the minimum photo size is 400x400px,
        the sum of the height and width is no more than 14000px,
        the file is no more than 50 MB in size, and the aspect ratio is at least 1:20.

        :param files: file path, file paths, file as bytes or files as bytes
        :param group_id: Community id for which you want to upload a product photo.
        """
        data = {"group_id": group_id}

        response = self._upload_files(
            data, files, "photos.getMarketAlbumUploadServer"
        )

        data["server"] = response["server"]
        data["hash"] = response["hash"]
        data["photo"] = response["photo"]

        return self.call_method("photos.saveMarketAlbumPhoto", data)

    def profile_photo(self, files, owner_id=None):
        """update profile photo

        :param files: file path, file paths, file as bytes or files as bytes
        :param owner_id: id of the community or current user. (default id of current user)
        """
        data = {}
        if owner_id:
            data["owner_id"] = owner_id

        response = self._upload_files(
            data, files, "photos.getOwnerPhotoUploadServer"
        )
        del data["owner_id"]

        data["server"] = response["server"]
        data["hash"] = response["hash"]
        data["photo"] = response["photo"]

        return self.call_method("photos.saveOwnerPhoto", data)

    def video(
            self,
            files: Union[str, List[str]],
            album_id: int,
            name: str = "",
            description: str = "",
            is_private: int = 0,
            wallpost: int = 0,
            link: str = "",
            group_id: int = 0,
            privacy_view: str = "",
            privacy_comment: str = "",
            no_comments: int = 0,
            repeat: int = 0,
            compression: int = 0
    ) -> Dict[str, Any]:
        """Uploads video

        :param files: file path, file paths, file as bytes or files as bytes
        :param album_id: id of the album into which the video file will be uploaded.
        :param name: name of the video file.
        :param description: description of the video file.
        :param is_private: 1 is indicated if the video is uploaded for sending by personal message.
        :param wallpost: whether after saving it is required to publish a video recording on the wall
        :param link: url for embedding video from an external site. e.g. Youtube.
        :param group_id: id of the community where the video will be saved.
        :param privacy_view: privacy settings for viewing video in a special format.
        :param privacy_comment: privacy settings for commenting on a video in a special format.
        :param no_comments: 1 - close comments (for videos from communities).
        :param repeat: looping video playback.
        """
        data = {
            "name": name,
            "description": description,
            "is_private": is_private,
            "wallpost": wallpost,
            "link": link,
            "album_id": album_id,
            "privacy_view": privacy_view,
            "privacy_comment": privacy_comment,
            "no_comments": no_comments,
            "repeat": repeat,
            "compression": compression
        }
        if group_id:
            data["group_id"] = group_id

        upload_url = self.call_method(
            "video.save", data)["response"]["upload_url"]
        response = []

        if isinstance(files, str):
            files = [files]

        for _, file in enumerate(files):
            response.append(
                self.session.post(
                    upload_url, files={"file": open(file, "rb")}
                ).json()
            )

        return response

    def _upload_files(
            self,
            data: Dict[str, Any],
            files: Union[str, List[str]],
            method: str
    ) -> Dict[str, Any]:
        upload_url = self.call_method(method, data)["response"]["upload_url"]
        uplfiles = {}

        if not isinstance(files, list):
            files = [files]

        if len(files) > 1:
            for index, file in enumerate(files):
                if isinstance(file, str):
                    uplfiles["file%d" % (index+1)] = open(file, "rb")
                elif isinstance(file, bytes):
                    uplfiles["file%d" % (index+1)] = file
        else:
            if isinstance(files[0], str):
                uplfiles["file"] = open(files[0], "rb")
            elif isinstance(files[0], bytes):
                uplfiles["file"] = files[0]

        return self.session.post(upload_url, files=uplfiles).json()

    def wall_photo(
            self,
            files: Union[str, List[str]],
            group_id: Optional[int] = None,
            user_id: Optional[int] = None,
            caption: str =""
    ) -> Dict[str, Any]:
        """upload photo in wall post

        :param files: file path, file paths, file as bytes or files as bytes
        :param group_id: id of the community on whose wall you want to upload the photo (without a minus sign).
        :param user_id: id of the user whose wall you want to save the photo on.
        :param caption: photo description text (maximum 2048 characters)
        """
        data = {}
        if group_id:
            data["group_id"] = group_id

        response = self._upload_files(data, files, "photos.getWallUploadServer")

        if user_id:
            data["user_id"] = user_id
        data["caption"] = caption
        data["server"] = response["server"]
        data["hash"] = response["hash"]
        data["photo"] = response["photo"]

        return self.call_method("photos.saveWallPhoto", data)

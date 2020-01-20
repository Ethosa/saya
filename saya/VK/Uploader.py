# -*- coding: utf-8 -*-
# author: Ethosa


class Uploader:
    def __init__(self, vk):
        self.session = vk.session
        self.call_method = vk.call_method

    def album_photo(self, files, album_id,
                    group_id=None, caption=""):
        """upload photo in album

        Arguments:
            files {str or list} -- file path or file paths
            album_id {int}

        Keyword Arguments:
            group_id {int} -- (default: {None})
            caption {str} -- photo caption (default: {""})

        Returns:
            dict -- response after photo saved
        """
        data = {
            "album_id": album_id,
            "group_id": group_id
        }
        if not group_id:
            del data["group_id"]

        response = self.upload_files(data, files, "photos.getUploadServer")

        data["caption"] = caption
        data["server"] = response["server"]
        data["hash"] = response["hash"]
        data["photos_list"] = response["photos_list"]

        response = self.call_method("photos.save", data)
        return response

    def audio(self, files, artist="", title=""):
        """Upload audio file

        Arguments:
            files {str or list} -- file path or file paths

        Keyword Arguments:
            artist {str} -- songwriter. The default is taken from ID3 tags. (default: {""})
            title {str} -- name of the composition. The default is taken from ID3 tags. (default: {""})

        Returns:
            dict -- response after audio saved
        """
        response = self.upload_files({}, files, "audio.getUploadServer")
        data = {
            "server": response["server"],
            "audio": response["audio"],
            "hash": response["hash"]
        }

        response = self.call_method("audio.save", data)
        return response

    def chat_photo(self, files, chat_id, crop_x=None,
                   crop_y=None, crop_width=None):
        """upload chat photo

        Arguments:
            files {str or list} -- file path or file paths
            chat_id {int} -- id of the conversation for which you want to upload a photo

        Keyword Arguments:
            crop_x {int} -- x coordinate for cropping the photo (upper right corner). (default: {None})
            crop_y {int} -- y coordinate for cropping the photo (upper right corner). (default: {None})
            crop_width {int} -- Width of the photo after cropping in px. (default: {None})

        Returns:
            dict -- response after photo saved
        """
        data = {"chat_id": chat_id}
        if crop_x:
            data["crop_x"] = crop_x
        if crop_y:
            data["crop_y"] = crop_y
        if crop_width:
            data["crop_width"] = crop_width

        response = self.upload_files(data, files, "photos.getChatUploadServer")

        data = {"file": response["response"]}

        response = self.call_method("messages.setChatPhoto", data)
        return response

    def cover_photo(self, files, group_id, crop_x=0, crop_y=0, crop_x2=795, crop_y2=200):
        """update group cover photo

        Arguments:
            files {str or list} -- file path or file paths
            group_id {int} -- community id.

        Keyword Arguments:
            crop_x {int} -- X coordinate of the upper left corner to crop the image. (default: {0})
            crop_y {int} -- Y coordinate of the upper left corner to crop the image. (default: {0})
            crop_x2 {int} -- X coordinate of the lower right corner to crop the image. (default: {795})
            crop_y2 {int} -- Y coordinate of the lower right corner to crop the image. (default: {200})

        Returns:
            dict -- response after photo saved
        """
        data = {
            "group_id": group_id,
            "crop_x": crop_x,
            "crop_y": crop_y,
            "crop_x2": crop_x2,
            "crop_y2": crop_y2
        }

        response = self.upload_files(data, files, "photos.getOwnerCoverPhotoUploadServer")
        data = {
            "hash": response["hash"],
            "photo": response["photo"]
        }

        response = self.call_method("photos.saveOwnerCoverPhoto", data)
        return response

    def document(self, files, group_id=None, title="", tags="", return_tags=0, is_wall=False):
        """upload document

        Arguments:
            files {str or list} -- file path or file paths
            group_id {int} -- community identifier (if you need to upload a document to the list of community documents).

        Keyword Arguments:
            title {str} -- document's name. (default: {""})
            tags {str} -- tags for search. (default: {""})
            return_tags {number} (default: {0})
            is_wall {bool} -- upload document in wall? (default: {False})

        Returns:
            dict -- response after document saved
        """
        data = {}
        if group_id:
            data["group_id"] = group_id

        response = self.upload_files(data, files, "docs.get%sUploadServer" % ("Wall" if is_wall else ""))
        data = {
            "file": response["file"],
            "title": title,
            "tags": tags,
            "return_tags": return_tags
        }

        response = self.call_method("docs.save", data)
        return response

    def document_message(self, files, peer_id, doc_type="doc", title="",
                         tags="", return_tags=0):
        """upload document in message

        Arguments:
            files {str or list} -- file path or file paths
            peer_id {int} -- destination identifier.

        Keyword Arguments:
            doc_type {str} -- type of document. Possible values: doc, audio_message (default: {"doc"})
            title {str} -- document's name. (default: {""})
            tags {str} -- tags for search. (default: {""})
            return_tags {number} (default: {0})

        Returns:
            dict -- response after document saved
        """
        data = {
            "peer_id": peer_id,
            "type": doc_type
        }

        response = self.upload_files(data, files, "docs.getMessagesUploadServer")
        data = {
            "file": response["file"],
            "title": title,
            "tags": tags,
            "return_tags": return_tags
        }

        response = self.call_method("docs.save", data)
        return response

    def format(self, response, type_obj="photo"):
        """response formatting

        Arguments:
            response {dict} -- response after object saved

        Keyword Arguments:
            type_obj {str} -- "photo", "video", "audio" etc (default: {"photo"})
        """
        if "response" in response:
            response = response["response"]
        if "type" in response:
            response = response[response["type"]]
        if isinstance(response, dict):
            if "owner_id" in response and "id" in response:
                return "%s%s_%s" % (type_obj, response["owner_id"], response["id"])
        elif isinstance(response, list):
            photos = []
            for photo in response:
                if "owner_id" in photo and "id" in photo:
                    photos.append("%s%s_%s" % (type_obj, photo["owner_id"], photo["id"]))
            return ",".join(photos)

    def message_photo(self, files, peer_id):
        """upload photo in message

        Arguments:
            files {str or list} -- file path or file paths
            peer_id {int} -- destination identifier (for uploading photos in community posts).

        Returns:
            dict -- response after photo saved
        """
        data = {"peer_id": peer_id}

        response = self.upload_files(data, files, "photos.getMessagesUploadServer")
        del data["peer_id"]

        data["server"] = response["server"]
        data["hash"] = response["hash"]
        data["photo"] = response["photo"]

        response = self.call_method("photos.saveMessagesPhoto", data)
        return response

    def market_photo(self, files, group_id, main_photo=None,
                     crop_x=None, crop_y=None, crop_width=None):
        """upload product photo

        Allowed formats: JPG, PNG, GIF.
        Limitations: the minimum photo size is 400x400px,
        the sum of the height and width is no more than 14000px,
        the file is no more than 50 MB in size, and the aspect ratio is at least 1:20.

        Arguments:
            files {str or list} -- file path or file paths
            group_id {int} -- Community id for which you want to upload a product photo.

        Keyword Arguments:
            main_photo {int} -- whether the photo is the cover
                of the product (1 - cover photo, 0 - additional photo) (default: {None})
            crop_x {int} -- x coordinate for cropping the photo (upper right corner). (default: {None})
            crop_y {int} -- y coordinate for cropping the photo (upper right corner). (default: {None})
            crop_width {int} -- Width of the photo after cropping in px. (default: {None})

        Returns:
            dict -- response after photo saved
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

        response = self.upload_files(data, files, "photos.getMarketUploadServer")

        data = {"group_id": group_id}
        data["server"] = response["server"]
        data["hash"] = response["hash"]
        data["photo"] = response["photo"]
        data["crop_data"] = response["crop_data"]
        data["crop_hash"] = response["crop_hash"]

        response = self.call_method("photos.saveMarketPhoto", data)
        return response

    def market_album_photo(self, files, group_id):
        """Uploading photos for a selection of goods

        Allowed formats: JPG, PNG, GIF.
        Limitations: the minimum photo size is 400x400px,
        the sum of the height and width is no more than 14000px,
        the file is no more than 50 MB in size, and the aspect ratio is at least 1:20.

        Arguments:
            files {str or list} -- file path or file paths
            group_id {int} -- Community id for which you want to upload a product photo.

        Returns:
            dict -- response after photo saved
        """
        data = {"group_id": group_id}

        response = self.upload_files(data, files, "photos.getMarketAlbumUploadServer")

        data["server"] = response["server"]
        data["hash"] = response["hash"]
        data["photo"] = response["photo"]

        response = self.call_method("photos.saveMarketAlbumPhoto", data)
        return response

    def profile_photo(self, files, owner_id=None):
        """update profile photo

        Arguments:
            files {str or list} -- file path or file paths

        Keyword Arguments:
            owner_id {int} -- id of the community or current user. (default id of current user)

        Returns:
            dict -- response after photo saved
        """
        data = {}
        if owner_id:
            data["owner_id"] = owner_id

        response = self.upload_files(data, files, "photos.getOwnerPhotoUploadServer")
        del data["owner_id"]

        data["server"] = response["server"]
        data["hash"] = response["hash"]
        data["photo"] = response["photo"]

        response = self.call_method("photos.saveOwnerPhoto", data)
        return response

    def video(self, files, album_id, name="", description="", is_private=0,
              wallpost=0, link="", group_id=0, privacy_view="", privacy_comment="",
              no_comments=0, repeat=0, compression=0):
        """upload video

        Arguments:
            files {str or list} -- file path or file paths
            album_id {int} -- id of the album into which the video file will be uploaded.

        Keyword Arguments:
            name {str} -- name of the video file. (default: {""})
            description {str} -- description of the video file. (default: {""})
            is_private {number} -- 1 is indicated if the video is uploaded for sending by personal message. (default: {0})
            wallpost {number} -- whether after saving it is required to publish a video recording on the wall (default: {0})
            link {str} -- url for embedding video from an external site. e.g. Youtube. (default: {""})
            group_id {number} -- id of the community where the video will be saved. (default: {0})
            privacy_view {str} -- privacy settings for viewing video in a special format. (default: {""})
            privacy_comment {str} -- privacy settings for commenting on a video in a special format. (default: {""})
            no_comments {number} -- 1 - close comments (for videos from communities). (default: {0})
            repeat {number} -- looping video playback. (default: {0})
            compression {number} (default: {0})

        Returns:
            dict -- response after photo saved
        """
        data = {
            "name": name,
            "description": description,
            "is_private": is_private,
            "wallpost": wallpost,
            "link": link,
            "group_id": group_id,
            "album_id": album_id,
            "privacy_view": privacy_view,
            "privacy_comment": privacy_comment,
            "no_comments": no_comments,
            "repeat": repeat,
            "compression": compression
        }
        if not group_id:
            del data["group_id"]

        response = self.call_method("video.save", data)
        upload_url = response["response"]["upload_url"]
        response = []

        if isinstance(files, str):
            files = [files]

        for _, file in enumerate(files):
            response.append(self.session.post(upload_url, files={"file": open(file, "rb")}).json())

        return response

    def upload_files(self, data, files, method):
        upload_server = self.call_method(method, data)
        upload_url = upload_server["response"]["upload_url"]
        upload_files = {}

        if isinstance(files, str):
            files = [files]

        if len(files) > 1:
            for index, file in enumerate(files):
                upload_files["file%d" % (index+1)] = open(file, "rb")
        else:
            upload_files["file"] = open(files[0], "rb")

        response = self.session.post(upload_url, files=upload_files).json()
        return response

    def wall_photo(self, files, group_id=None,
                   user_id=None, caption=""):
        """upload photo in wall post

        Arguments:
            files {str or list} -- file path or file paths

        Keyword Arguments:
            group_id {int} -- id of the community on whose wall you want to upload the photo (without a minus sign). (default: {None})
            user_id {int} -- id of the user whose wall you want to save the photo on. (default: {None})
            caption {str} -- photo description text (maximum 2048 characters) (default: {""})

        Returns:
            dict -- response after photo saved
        """
        data = {"group_id": group_id}
        if not group_id:
            del data["group_id"]

        response = self.upload_files(data, files, "photos.getWallUploadServer")

        if user_id:
            data["user_id"] = user_id
        data["caption"] = caption
        data["server"] = response["server"]
        data["hash"] = response["hash"]
        data["photo"] = response["photo"]

        response = self.call_method("photos.saveWallPhoto", data)
        return response

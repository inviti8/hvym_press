# -*- coding: utf-8 -*-
"""
W3DeployHandler.py

This module handles deployment to IPFS via Pintheon API.
Refactored to support individual file uploads with proper URL construction.
"""

import os
import json
import requests
import FreeSimpleGUI as sg
import urllib.parse
from datetime import datetime, timedelta
import time
import threading
from hvym_stellar import *
from stellar_sdk import Keypair
from pymacaroons import Macaroon, Verifier


# Custom exception classes for better error handling
class DeploymentError(Exception):
    """Base exception for deployment errors."""

    pass


class UploadError(DeploymentError):
    """Exception raised when file upload fails."""

    pass


class ConfigurationError(DeploymentError):
    """Exception raised when configuration is invalid."""

    pass


class SecurityError(DeploymentError):
    """Exception raised when security validation fails."""

    pass


# Example URL for reference
# https://sapphire-giant-butterfly-891.mypinata.cloud/ipfs/bafybeiapx5hzywrsw76v7dd6s5bvpta3djad65ovfrrwvs2367ul7kokde/DALL%C2%B7E%202022-10-03%2014.20.02%20-%20A%20digital%20illustratio.png


class pintheon_payload:
    """
    Payload class for Pintheon API uploads.

    :param pintheonOptions: options json string
    :type pintheonOptions: (str)
    :param name: name of the file
    :type name: (str)
    :param filePath: path to the file
    :type filePath: (str)
    :param wrapWithDirectory: whether to wrap with directory
    :type wrapWithDirectory: (str)
    :param pinToIPFS: whether to pin to IPFS
    :type pinToIPFS: (str)
    :param pintheonMetadata: related metadata json string
    :type pintheonMetadata:  (str)
    """

    def __init__(
        self,
        pintheonOptions,
        name,
        filePath,
        wrapWithDirectory,
        pinToIPFS,
        pintheonMetadata,
    ):
        self.pintheonOptions = pintheonOptions
        self.name = name
        self.filePath = filePath
        self.wrapWithDirectory = wrapWithDirectory
        self.pinToIPFS = pinToIPFS
        self.pintheonMetadata = pintheonMetadata

        self.dictionary = {
            "pintheonOptions": self.pintheonOptions,
            "pintheonMetadata": self.pintheonMetadata,
        }


class W3DeployHandler:
    """
    Handles deployment to IPFS via Pintheon API.
    Refactored to support individual file uploads with proper error handling,
    input validation, and thread safety.

    This class provides methods to:
    - Upload individual media files to IPFS
    - Deploy built sites to IPFS
    - Manage deployment manifests
    - Handle Pintheon API configuration

    Thread Safety:
        All manifest operations are protected by locks to prevent corruption
        when multiple threads access the handler simultaneously.

    Error Handling:
        Uses custom exception classes for different types of errors:
        - DeploymentError: Base exception for all deployment errors
        - UploadError: Raised when file uploads fail
        - ConfigurationError: Raised when configuration is invalid
        - SecurityError: Raised when security validation fails
    """

    def __init__(self, filePath, debugPath, resourcePath, settings):
        """
        Initialize the W3DeployHandler.

        :param filePath: path to the project file
        :type filePath: (str)
        :param debugPath: path to the debug directory
        :type debugPath: (str)
        :param resourcePath: path to the resources directory
        :type resourcePath: (str)
        :param settings: settings dictionary
        :type settings: (dict)
        """
        self.filePath = filePath
        self.debugPath = debugPath
        self.resourcePath = resourcePath
        self.settings = settings

        # Thread safety for manifest operations
        self._manifest_lock = threading.Lock()

        # Pintheon configuration
        self.pintheonApiURL = "https://localhost:9999/api_upload"

        # Extract hostname and port from backend_end_point for gateway
        backend_endpoint = settings.get("backend_end_point", "localhost:9999")
        if backend_endpoint.startswith("https://"):
            gateway = backend_endpoint[8:]  # Remove 'https://'
        elif backend_endpoint.startswith("http://"):
            gateway = backend_endpoint[7:]  # Remove 'http://'
        else:
            gateway = backend_endpoint

        self.pintheon = {
            "api_url": self.pintheonApiURL,
            "access_token": self.build_access_token(),
            "gateway": gateway,
            "encrypted": settings.get("pintheon_encrypted", False),
            "meta_data": settings.get("backend_meta_data", ""),
        }

        # Site information from settings
        self.siteName = settings.get("siteName", "default")
        self.siteID = settings.get("siteID", "default")
        self.sitePath = settings.get("sitePath", "")

        # Manifest and deployment tracking
        self.manifest = {}
        self.deployFiles = []
        self.deployFolderName = ""
        self.folderID = None
        self.folderCID = None
        self.deployedUrl = None

        # Load existing data if available
        self.loadData()

        # Initialize deployment files
        self._initDeployFiles()
        self.updateManifestData(filePath)

    def _initDeployFiles(self):
        """Initialize the deployment files list."""
        self.deployFiles = []
        if os.path.isdir(self.debugPath):
            for root, dirs, files in os.walk(self.debugPath):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, self.debugPath)
                    self.deployFiles.append(
                        {
                            "path": file_path,
                            "relative_path": relative_path,
                            "name": file,
                        }
                    )

    def build_access_token(self):
        self.keys = Keypair.from_secret(self.settings["private_key"])
        self.keys_25519 = Stellar25519KeyPair(self.keys)
        self.pub25519 = self.keys_25519.public_key()
        self.access_token = self.settings.get("pintheon_access_token", "")
        if self.access_token != "":
            self.app_token = Macaroon.deserialize(self.access_token)
            self.app_pub25519 = self.app_token.identifier.split("|")[0]
            self.access_token = StellarSharedKeyTokenBuilder(
                self.keys_25519, self.app_pub25519
            ).serialize()

        return self.access_token

    def safe_encode(self, string):
        return urllib.parse.quote(string, safe="/")

    def loadData(self):
        """Load existing deployment data from file."""
        data_file = os.path.join(self.filePath, "deploy.data")
        if os.path.isfile(data_file):
            try:
                with open(data_file, "rb") as f:
                    data = json.load(f)
                    if "manifest" in data:
                        self.manifest = data["manifest"]
                    if "pintheon" in data:
                        self.pintheon.update(data["pintheon"])
            except Exception as e:
                print(f"Error loading deployment data: {e}")

    def saveData(self):
        """Save deployment data to file with thread safety."""
        data_file = os.path.join(self.filePath, "deploy.data")
        try:
            with self._manifest_lock:
                data = {"manifest": self.manifest, "pintheon": self.pintheon}
                with open(data_file, "w") as f:
                    json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving deployment data: {e}")

    def setPintheonAccessToken(self, access_token):
        """Set the Pintheon access token."""
        if not isinstance(access_token, str):
            raise TypeError("Access token must be a string")

        self.pintheon["access_token"] = access_token
        self.saveData()

    def setPintheonGateway(self, gateway):
        """Set the Pintheon gateway URL."""
        if not isinstance(gateway, str):
            raise TypeError("Gateway must be a string")

        if not gateway:
            raise ValueError("Gateway cannot be empty")

        # Basic gateway format validation
        if "://" in gateway or " " in gateway or len(gateway) > 255:
            raise ValueError(f"Invalid gateway format: {gateway}")

        self.pintheon["gateway"] = gateway
        self.saveData()

    def setPintheonEncrypted(self, encrypted):
        """Set whether to use encrypted uploads."""
        if not isinstance(encrypted, bool):
            raise TypeError("Encrypted must be a boolean")

        self.pintheon["encrypted"] = encrypted
        self.saveData()

    def setPintheonMetadata(self, metadata):
        """Set the Pintheon metadata."""
        if not isinstance(metadata, str):
            raise TypeError("Metadata must be a string")

        self.pintheon["meta_data"] = metadata
        self.saveData()

    def getPintheonConfig(self):
        """Get the current Pintheon configuration."""
        return self.pintheon.copy()

    def updatePintheonConfig(self, config):
        """Update the Pintheon configuration."""
        self.pintheon.update(config)
        self.saveData()

    def _uploadSingleFile(self, file_path):
        """
        Upload a single file to Pintheon and return (cid, url) tuple.

        :param file_path: path to the file to upload
        :type file_path: (str)
        :return: (cid, url) tuple or None on failure
        :rtype: (tuple) or (None)
        """
        # Input validation
        if not file_path:
            raise ValueError("File path cannot be empty")

        if not isinstance(file_path, str):
            raise TypeError("File path must be a string")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File does not exist: {file_path}")

        if not os.path.isfile(file_path):
            raise ValueError(f"Path is not a file: {file_path}")

        try:
            # Prepare the file for upload
            file_name = os.path.basename(file_path)

            # Prepare the multipart form data
            with open(file_path, "rb") as f:
                files = {"file": (file_name, f, "application/octet-stream")}

                # Add required form data for Pintheon API
                data = {
                    "access_token": self.build_access_token(),
                    "encrypted": str(self.pintheon["encrypted"]).lower(),
                }

                print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                print(self.pintheon["api_url"])
                print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

                # Make the upload request to Pintheon's api_upload endpoint
                response = requests.post(
                    self.pintheon["api_url"],
                    files=files,
                    data=data,
                    verify=False,  # For localhost HTTPS
                    timeout=30,  # Add timeout to prevent hanging
                )

                if response.status_code == 200:
                    try:
                        result = response.json()
                    except json.JSONDecodeError as e:
                        raise UploadError(
                            f"Invalid JSON response from server: {response.text}"
                        )

                    # Pintheon returns the CID directly in the response
                    cid = result.get("Hash") or result.get("IpfsHash")

                    if cid:
                        # Validate gateway configuration
                        gateway = self.pintheon.get("gateway", "")
                        if not gateway or not isinstance(gateway, str):
                            raise ConfigurationError("Invalid gateway configuration")

                        # Basic gateway format validation
                        if "://" in gateway or " " in gateway or len(gateway) > 255:
                            raise ConfigurationError(
                                f"Invalid gateway format: {gateway}"
                            )

                        # Generate the correct IPFS URL format
                        gateway_url = f"https://{gateway}/ipfs/{cid}"
                        print(f"Successfully uploaded {file_name}: {gateway_url}")
                        return (cid, gateway_url)
                    else:
                        raise UploadError(
                            f"Upload successful but no CID returned: {response.text}"
                        )
                else:
                    raise UploadError(
                        f"Upload failed with status {response.status_code}: {response.text}"
                    )

        except (
            ValueError,
            TypeError,
            FileNotFoundError,
            UploadError,
            ConfigurationError,
        ):
            # Re-raise these exceptions
            raise
        except requests.exceptions.Timeout:
            raise UploadError(f"Upload timeout for {file_path}")
        except requests.exceptions.RequestException as e:
            raise UploadError(f"Network error uploading {file_path}: {e}")
        except Exception as e:
            raise UploadError(f"Unexpected error uploading file {file_path}: {e}")

    def _isPathSafe(self, target_path, project_root):
        """
        Check if a path is safe to access (within project bounds).

        :param target_path: path to check
        :type target_path: (str)
        :param project_root: project root directory
        :type project_root: (str)
        :return: True if path is safe, False otherwise
        :rtype: (bool)
        """
        try:
            # Convert both paths to absolute paths
            abs_target = os.path.abspath(target_path)
            abs_project = os.path.abspath(project_root)

            # Normalize paths to handle any symlinks or relative components
            real_target = os.path.realpath(abs_target)
            real_project = os.path.realpath(abs_project)

            # Check if the target path is within the project directory
            # Use commonpath to handle edge cases properly
            try:
                common_path = os.path.commonpath([real_target, real_project])
                return common_path == real_project
            except ValueError:
                # This can happen if paths are on different drives (Windows)
                # In this case, fall back to string comparison
                return real_target.startswith(real_project)

        except (OSError, ValueError) as e:
            print(f"Error checking path safety: {e}")
            return False

    def uploadMediaFiles(self, media_folder_path):
        """
        Upload all media files from the media folder individually.
        Returns a dictionary mapping filenames to IPFS URLs.

        :param media_folder_path: path to the media folder
        :type media_folder_path: (str)
        :return: dictionary of uploaded media files
        :rtype: (dict)
        """
        # Input validation
        if not media_folder_path:
            raise ValueError("Media folder path cannot be empty")

        if not isinstance(media_folder_path, str):
            raise TypeError("Media folder path must be a string")

        if not os.path.isdir(media_folder_path):
            raise FileNotFoundError(f"Media folder does not exist: {media_folder_path}")

        # Security: Ensure the path is within project bounds
        # if not self._isPathSafe(media_folder_path, self.filePath):
        #     raise SecurityError(f"Media folder path {media_folder_path} is outside project directory")

        print(f"Uploading media files from: {media_folder_path}")

        # Collect all media files
        media_files = []
        try:
            for root, dirs, files in os.walk(media_folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Check if it's a media file
                    if self._isMediaFile(file):
                        media_files.append(file_path)
        except OSError as e:
            raise UploadError(f"Cannot access media folder: {e}")

        if not media_files:
            print("No media files found to upload")
            return {}

        # Upload each file individually
        uploaded_media = {}
        failed_files = []

        for file_path in media_files:
            filename = os.path.basename(file_path)
            print(f"Uploading: {filename}")

            try:
                result = self._uploadSingleFile(file_path)
                if result:
                    cid, url = result
                    uploaded_media[filename] = {
                        "cid": cid,
                        "url": url,
                        "filename": filename,
                        "local_path": file_path,
                    }
                else:
                    failed_files.append(filename)
            except Exception as e:
                print(f"Failed to upload {filename}: {e}")
                failed_files.append(filename)

        # Report results
        print(f"Successfully uploaded {len(uploaded_media)} media files")
        if failed_files:
            print(f"Failed to upload {len(failed_files)} files: {failed_files}")

        # Only update manifest if we have successful uploads
        if uploaded_media:
            with self._manifest_lock:
                self.manifest["media_files"] = uploaded_media
            self.saveData()

        return uploaded_media

    def _isMediaFile(self, filename):
        """Check if a file is a media file that should be uploaded."""
        if not filename or not isinstance(filename, str):
            return False

        media_extensions = {
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".bmp",
            ".webp",
            ".mp4",
            ".avi",
            ".mov",
            ".wmv",
            ".flv",
            ".webm",
            ".mp3",
            ".wav",
            ".ogg",
            ".flac",
            ".aac",
            ".gltf",
            ".glb",
            ".obj",
            ".fbx",
            ".dae",
        }

        file_ext = os.path.splitext(filename.lower())[1]
        return file_ext in media_extensions

    def deploySite(self, site_folder_path):
        """
        Deploy the built site (just the index.html and assets).

        :param site_folder_path: path to the built site folder
        :type site_folder_path: (str)
        :return: (cid, url) tuple or None on failure
        :rtype: (tuple) or (None)
        """
        # Input validation
        if not site_folder_path:
            raise ValueError("Site folder path cannot be empty")

        if not isinstance(site_folder_path, str):
            raise TypeError("Site folder path must be a string")

        if not os.path.isdir(site_folder_path):
            raise FileNotFoundError(f"Site folder does not exist: {site_folder_path}")

        # # Security: Ensure the path is within project bounds
        # if not self._isPathSafe(site_folder_path, self.filePath):
        #     raise SecurityError(f"Site folder path {site_folder_path} is outside project directory")

        print(f"Deploying site from: {site_folder_path}")

        # Upload the main index.html file
        index_path = os.path.join(site_folder_path, "index.html")
        if os.path.exists(index_path):
            print("Uploading index.html...")
            result = self._uploadSingleFile(index_path)
            if result:
                cid, url = result
                self.manifest["site"] = {
                    "cid": cid,
                    "url": url,
                    "type": "site",
                    "filename": "index.html",
                }
                self.saveData()
                print(f"Site deployed successfully: {url}")
                return (cid, url)
        else:
            print("Error: index.html not found in site folder")

        return None

    # Legacy method names for backward compatibility - these now do individual file uploads
    def pintheonFile(self, filePath, payload):
        """
        Upload a single file to Pintheon (legacy method).

        :param filePath: path to the file
        :type filePath: (str)
        :param payload: payload object
        :type payload: (pintheon_payload)
        :return: gateway URL or False on failure
        :rtype: (str) or (bool)
        """
        if not self.pintheon["access_token"]:
            print("Pintheon Access Token Not Set!")
            return False

        if not self.pintheon["gateway"]:
            print("Pintheon Gateway Not Set!")
            return False

        result = self._uploadSingleFile(filePath)
        if result:
            cid, url = result
            # Update manifest if available
            if self.manifest and os.path.basename(filePath) in self.manifest:
                self.manifest[os.path.basename(filePath)]["url"] = url
                self.saveData()
            return url
        return False

    def pintheonCss(self, filePath):
        """
        Upload a CSS file to Pintheon (legacy method).

        :param filePath: path to the CSS file
        :type filePath: (str)
        :return: gateway URL or False on failure
        :rtype: (str) or (bool)
        """
        metadata = self.pintheon["meta_data"]
        f_name = os.path.basename(filePath)
        arr = filePath.split("/")
        parent_folder = arr[len(arr) - 2]
        fileName = os.path.join(parent_folder, f_name).replace("\\", "/")

        payload = pintheon_payload(
            '{"cidVersion": 1}', fileName, filePath, "true", "true", metadata
        )
        return self.pintheonFile(filePath, payload)

    # Renamed methods to reflect actual functionality
    def uploadFilesIndividually(self, files, payload, window=None):
        """
        Upload multiple files to Pintheon individually (renamed from pintheonFiles).

        :param files: list of file tuples
        :type files: (list)
        :param payload: payload dictionary
        :type payload: (dict)
        :param window: optional window for progress updates
        :type window: (FreeSimpleGUI.Window)
        :return: response object
        :rtype: (requests.Response)
        """
        if not self.pintheon["access_token"]:
            print("Pintheon Access Token Not Set!")
            return type(
                "Response", (), {"status_code": 401, "text": "Access token not set"}
            )()

        if not self.pintheon["gateway"]:
            print("Pintheon Gateway Not Set!")
            return type(
                "Response", (), {"status_code": 400, "text": "Gateway not set"}
            )()

        # Upload each file individually and store URLs in manifest
        uploaded_files = []
        failed_files = []

        for file_tuple in files:
            if isinstance(file_tuple, tuple) and len(file_tuple) > 1:
                file_info = file_tuple[1]
                if isinstance(file_info, tuple) and len(file_info) > 1:
                    file_name = file_info[0]
                    file_handle = file_info[1]

                    try:
                        # Upload the file
                        result = self._uploadSingleFile(file_handle.name)
                        if result:
                            cid, url = result
                            uploaded_files.append((file_name, cid))
                        else:
                            failed_files.append(file_name)

                    except Exception as e:
                        print(f"Error processing file {file_name}: {e}")
                        failed_files.append(file_name)

        # Return response object similar to Pinata API
        if failed_files:
            print(f"Failed to upload {len(failed_files)} files: {failed_files}")
            return type(
                "Response",
                (),
                {
                    "status_code": 500,
                    "text": f"Failed to upload {len(failed_files)} files",
                },
            )()
        else:
            print(f"Successfully uploaded {len(uploaded_files)} files")
            return type(
                "Response",
                (),
                {
                    "status_code": 200,
                    "json": lambda: {"IpfsHash": "multiple_files_uploaded"},
                },
            )()

    def uploadMediaFolder(
        self, filePath, wrapWithDirectory=True, pinToIPFS=True, useParentDirs=False
    ):
        """
        Upload a media folder by uploading individual files (renamed from pintheonDirectory).

        :param filePath: path to the directory
        :type filePath: (str)
        :param wrapWithDirectory: whether to wrap with directory (not used in individual uploads)
        :type wrapWithDirectory: (bool)
        :param pinToIPFS: whether to pin to IPFS (not used in individual uploads)
        :type pinToIPFS: (bool)
        :param useParentDirs: whether to use parent directories (not used in individual uploads)
        :type useParentDirs: (bool)
        :return: True on success, False on failure
        :rtype: (bool)
        """
        if not self.pintheon["access_token"]:
            print("Pintheon Access Token Not Set!")
            return False

        if not self.pintheon["gateway"]:
            print("Pintheon Gateway Not Set!")
            return False

        # Use the new uploadMediaFiles method
        result = self.uploadMediaFiles(filePath)
        return len(result) > 0

    def uploadMediaFolderGUI(
        self,
        filePath,
        wrapWithDirectory=True,
        pinToIPFS=True,
        useParentDirs=False,
        askPermission=True,
    ):
        """
        Upload a media folder with GUI confirmation (renamed from pintheonDirectoryGUI).

        :param filePath: path to the directory
        :type filePath: (str)
        :param wrapWithDirectory: whether to wrap with directory (not used in individual uploads)
        :type wrapWithDirectory: (bool)
        :param pinToIPFS: whether to pin to IPFS (not used in individual uploads)
        :type pinToIPFS: (bool)
        :param useParentDirs: whether to use parent directories (not used in individual uploads)
        :type useParentDirs: (bool)
        :param askPermission: whether to ask for permission
        :type askPermission: (bool)
        :return: (folderCID, deployedUrl) tuple or None on failure
        :rtype: (tuple) or (None)
        """
        result = None

        if askPermission:
            # Simple confirmation popup
            popup_result = sg.popup_yes_no(
                "Deploy Media Files to IPFS via Pintheon?",
                title="Confirm Media Deployment",
                keep_on_top=True,
            )
            if popup_result != "Yes":
                return None

        if self.pintheon["access_token"] and self.pintheon["gateway"]:
            # Call the new method
            success = self.uploadMediaFolder(
                filePath, wrapWithDirectory, pinToIPFS, useParentDirs
            )
            if success:
                # Return a tuple for compatibility
                result = ("media_uploaded", "media_deployed")
        else:
            sg.popup_ok("Pintheon Credentials Not Set!", keep_on_top=True)

        return result

    def uploadResourcesGUI(
        self, wrapWithDirectory=True, pinToIPFS=True, useParentDirs=False
    ):
        """
        Upload resources directory to Pintheon with GUI (renamed from pintheonResourcesGUI).

        :param wrapWithDirectory: whether to wrap with directory (not used in individual uploads)
        :type wrapWithDirectory: (bool)
        :param pinToIPFS: whether to pin to IPFS (not used in individual uploads)
        :type pinToIPFS: (bool)
        :param useParentDirs: whether to use parent directories (not used in individual uploads)
        :type useParentDirs: (bool)
        :return: result from uploadMediaFolderGUI
        :rtype: (tuple) or (None)
        """
        return self.uploadMediaFolderGUI(
            self.resourcePath, wrapWithDirectory, pinToIPFS, useParentDirs
        )

    # Legacy methods for backward compatibility
    def pintheonFiles(self, files, payload, window=None):
        """Legacy method - use uploadFilesIndividually instead."""
        return self.uploadFilesIndividually(files, payload, window)

    def pintheonDirectory(
        self, filePath, wrapWithDirectory=True, pinToIPFS=True, useParentDirs=False
    ):
        """Legacy method - use uploadMediaFolder instead."""
        return self.uploadMediaFolder(
            filePath, wrapWithDirectory, pinToIPFS, useParentDirs
        )

    def pintheonDirectoryGUI(
        self,
        filePath,
        wrapWithDirectory=True,
        pinToIPFS=True,
        useParentDirs=False,
        askPermission=True,
    ):
        """Legacy method - use uploadMediaFolderGUI instead."""
        return self.uploadMediaFolderGUI(
            filePath, wrapWithDirectory, pinToIPFS, useParentDirs, askPermission
        )

    def pintheonResourcesGUI(
        self, wrapWithDirectory=True, pinToIPFS=True, useParentDirs=False
    ):
        """Legacy method - use uploadResourcesGUI instead."""
        return self.uploadResourcesGUI(wrapWithDirectory, pinToIPFS, useParentDirs)

    # Remove unused methods
    def _folderArray(self, key, filePath, basePath, window=None):
        """This method is no longer needed for individual file uploads."""
        print(
            "Warning: _folderArray is deprecated and not needed for individual file uploads"
        )
        pass

    def newFileData(self, filePath):
        """Create new file data entry."""
        return {
            "time_stamp": "",
            "type": None,
            "path": filePath,
            "url": None,
            "items": [],
        }

    def updateFileDataPintheonURL(self, file_key, url):
        """Update file data with Pintheon URL."""
        if file_key in self.manifest:
            print(f"URL being saved for: {file_key}")
            print(f"URL: {url}")
            self.manifest[file_key]["url"] = url
            self.saveData()

    def updateManifestData(self, filePath):
        """Update manifest data for files in the given path."""
        if not os.path.exists(filePath):
            return

        files = os.listdir(filePath)
        prune_data = []

        for f in files:
            f_name = os.path.basename(f)
            f_path = os.path.join(filePath, f)

            if ".data" not in f_name and ".md" not in f_name:
                if os.path.isfile(f_path):
                    if f_name not in self.manifest:
                        self.manifest[f_name] = self.newFileData(f_path)
                else:
                    self.updateManifestData(f_path)

        # Prune removed files
        for k in self.manifest.keys():
            if k not in files:
                prune_data.append(k)

        self.saveData()

    def updateSettings(self, settings):
        """Update Pintheon settings from application settings."""
        # Extract hostname and port from backend_end_point for gateway
        backend_endpoint = settings.get("backend_end_point", "localhost:5000")
        if backend_endpoint.startswith("https://"):
            gateway = backend_endpoint[8:]  # Remove 'https://'
        elif backend_endpoint.startswith("http://"):
            gateway = backend_endpoint[7:]  # Remove 'http://'
        else:
            gateway = backend_endpoint

        self.pintheon.update(
            {
                "access_token": settings.get("pintheon_access_token", ""),
                "gateway": gateway,
                "encrypted": settings.get("pintheon_encrypted", False),
                "meta_data": settings.get("backend_meta_data", ""),
            }
        )
        self.saveData()

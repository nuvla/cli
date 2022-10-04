from pathlib import Path

# Local files handling
LOCAL_PATH: Path = Path('~/.nuvla/').expanduser()
RELEASES_PATH: Path = LOCAL_PATH / 'releases'
RELEASES_LINK: str = 'https://api.github.com/repos/nuvlaedge/deployment/releases'
RELEASE_DOWNLOAD_LINK: str = 'https://github.com/nuvlaedge/deployment/releases/' \
                             'download/{version}/{file}'

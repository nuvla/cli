# Changelog

## Unreleased
### Added
 - Added decommissioning timeout
### Changed
 - Removed old action-entity build
 - Fixed force delete of single edges when bulk deleting
 - Updated dependencies version: typer, invoke, pydantic and fabric
## [0.0.1a6] - 14-11-2022
### Added
- Optional VPN edge configuration on creation
- Added optional Nuvla endpoint with https://nuvla.io as default.
### Changed
- Support for fleet starts in local machine (Limited functionality)

## [0.0.1a5] - 14-11-2022
### Changed
- Default refresh period from 10H to 1 week

## [0.0.1a4] - 10-11-2022
### Changed
- Fixed bug related to dummy fleet starts requiring docker-compose files
- Updated typer to the latest version
#!/bin/bash

directory_path="$1"

# Check if the argument was provided
if [ -z "$directory_path" ]; then
    echo "Usage: $0 <directory_path>"
    exit 1
fi

# Check if the directory exists
if [ ! -d "$directory_path" ]; then
    # The directory does not exist, create it
    echo "Creating directory: $directory_path"
    mkdir -p "$directory_path"
fi

# download syzygy tablebases https://syzygy-tables.info/
# ~1GB
wget -P endgame/syzygy --mirror --no-parent --no-directories -e robots=off http://tablebase.sesse.net/syzygy/3-4-5/
# ~81.4GB
wget -P endgame/syzygy --mirror --no-parent --no-directories -e robots=off http://tablebase.sesse.net/syzygy/6-DTZ/
# ~67.8GB
wget -P endgame/syzygy --mirror --no-parent --no-directories -e robots=off http://tablebase.sesse.net/syzygy/6-WDL/
# ~8.3TB
# wget -P endgame/syzygy --mirror --no-parent --no-directories -e robots=off http://tablebase.sesse.net/syzygy/7-DTZ/
# ~8.5TB
# wget -P endgame/syzygy --mirror --no-parent --no-directories -e robots=off http://tablebase.sesse.net/syzygy/7-WDL/

echo 'download complete, verifying checksums'
md5sum --check checksum.md5

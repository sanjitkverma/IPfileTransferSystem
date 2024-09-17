### README for BitTorrent File Transfer Experiment with libtorrent

#### Environment Setup

- **Python Version Required**: 3.12.X
- **Required Library**: libtorrent (Python bindings for the libtorrent library)
  
To install libtorrent, use the following command:
```bash
pip install python-libtorrent-rasterbar
```

#### Experiment Overview

This experiment involves using the BitTorrent protocol for file transfers, utilizing the libtorrent library. It consists of two main operations:

1. **Seeding a File**: The process where the original file is made available for download.
2. **Downloading a File**: The process where peers connect to the seeder (or other peers) to download the file.

#### Creating Torrent Files

Before starting the experiment, you must create torrent files for the files you wish to transfer. Use the `make_torrent` function provided in the script to generate torrent files. This process involves specifying the file path and the tracker information.

#### Seeding Files

To seed files, use the `seed_file` function. This function takes the file path and the path to its corresponding torrent file. It starts a BitTorrent session and shares the file with peers.

#### Downloading Files

Peers can download files using the provided script by adding the torrent file to their BitTorrent session and specifying the save path.

### Instructions

#### Seeding (Computer 1)

1. **Generate Torrent Files**: First, generate torrent files for your data using the `make_torrent` function. Specify the file path for each file you want to seed.

2. **Seed Files**: Use the `seed_file` function to share your files with peers. Ensure that the torrent file is accessible to peer machines.

#### Downloading (Remainder computer)

1. **Set Up Session**: On the peer machine, configure the BitTorrent session and add the torrent file to the session.

2. **Download File**: Specify the save path for the downloaded file. The script will automatically download the file using the BitTorrent protocol.

### Example Command

For seeding:
```bash
python3 bitorrent_seed.py
```

For downloading:
```bash
python3 bitorrent_peers.py
```

### Note

Be sure to adjust the file paths, sizes and iterations modifying file_name for the file name, iterations for the iterations and file size for the file size.

In order for our algorithmn to work, the peer computers must first be initialized and ran (run the bitorrent_peers.py first) and then the seeding file
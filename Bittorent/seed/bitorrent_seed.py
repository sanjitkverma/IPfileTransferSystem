import libtorrent as lt
import time
import os
import csv

# on seeder machine (where file is present), run make_torrent function first then create session and add the torrent file
# to the session and set the save_path to the path of file.

# on peer machines, start the session first, then add the torrent file to the session and set the save_path to the path of file

# this is the function to create torrents for the specified file
# it generates the hash for the file and creates a torrent file for the file
# it also adds a public tracker to the torrent file and a creator
def make_torrent(file_path):
    # Create torrent file
    fs = lt.file_storage()
    lt.add_files(fs, file_path)
    t = lt.create_torrent(fs)
    t.add_tracker("udp://tracker.dler.com:6969/announce") # public tracker
    t.set_creator('sarvesh')
    lt.set_piece_hashes(t, os.path.dirname(file_path))
    torrent = t.generate()
    f = open(file_path + '.torrent', 'wb')
    f.write(lt.bencode(torrent))
    f.close()

# this function seeds the file specified by file_path
def seed_file(file_path, torrent_path):
    ses = lt.session({'listen_interfaces': '0.0.0.0:6881'})
        # ses.listen_on(6881, 6891)
    info = lt.torrent_info(torrent_path)
    h = ses.add_torrent({'ti': info, 'save_path': './'})

    print(f"Seeding {file_path}")
    while True:
        s = h.status()

        print('%.2f%% complete (down: %.1f kB/s up: %.1f kB/s peers: %d seeds: %d) %s' % (
            s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000,
            s.num_peers, s.num_seeds, s.state))
                
                # if s.num_peers == 0:
                #     end_time = time.time()
                #     print(f"Seeding completed for {file_path}")
                #     return end_time - start_time


# comment or uncomment the below loop to create the torrent files for the files in file_sizes
# make sure the peer machines all have the torrent files for the files in file_sizes before trying to download the files
# file_sizes = ['./A_10kB', './A_100kB', './A_1MB', './A_10MB']  # Files to torrent and seed
# for file in file_sizes:
#     make_torrent(file)

# # modify these for each experiment
file_name = './A_10MB'

torrent_path = file_name + ".torrent"

# start seeding process
seed_file(file_name, torrent_path)

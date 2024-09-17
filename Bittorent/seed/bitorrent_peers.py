import libtorrent as lt
import time
import os
import numpy as np


# on seeder machine (where file is present), run make_torrent function first then create session and add the torrent file
# to the session and set the save_path to the path of file.
# on peer machines, start the session first, then add the torrent file to the session and set the save_path to the path of file

def peer(torrent_path, i):
    ses = lt.session({'listen_interfaces': '0.0.0.0:6881'}) 
    info = lt.torrent_info(torrent_path)
    h = ses.add_torrent({'ti': info, 'save_path': './'})

    while True:
        num_peers = h.status().num_peers
        s = h.status()
 
        start_time = time.time()
        tFlag = False
        while True:
            s = h.status()
            # print(s.progress)
            print(str(i) + '%.2f%% complete (down: %.1f kB/s up: %.1f kB/s peers: %d seeds: %d) %s' % (
                s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000,
                s.num_peers, s.num_seeds, s.state))

            if s.is_seeding:
                end_time = time.time()
                return end_time - start_time


# file_sizes = ['./A_10kB', './A_100kB', './A_1MB', './A_10MB']  # Files to torrent and seed
# iterations = [333, 33, 3, 1] # number of iterations to run for experiment
file = './A_10MB'  # File/home/sarvesh/Downloads/IPProject1/Bittorent/seed/A_1MB.torrent
iter_count = 333  # Number of iterations to run for experiment

print(f"Downloading {file} {iter_count} times")
filename = file
durations = []
file_size_kb = 10000
# this is the loop to download the file a certain number of times, change the value inside range to increase or decrease
for i in range(1):
    torrent_path = file + '.torrent'
    
    tot_time = peer(torrent_path, i)
    durations.append(tot_time)
    print(os.path.exists(file))
    # make sure to remove the file before trying to re-download it
    while os.path.exists(file):
        os.remove(file)

    print(i)

# calculate the average throughput and standard deviation throughput and store
average_throughput = np.mean([file_size_kb / duration for duration in durations])
std_dev_throughput = np.std([file_size_kb / duration for duration in durations])

with open('bittorrent_peer_10kB.txt', 'w') as f:
    f.write(f"Average throughput: {average_throughput} kB/s\n")
    f.write(f"Standard deviation throughput: {std_dev_throughput} kB/s\n")
print(f"Download completed for {torrent_path}")

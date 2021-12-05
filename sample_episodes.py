import minerl
import os
import argparse
import bz2
import _pickle as cPickle
​
## Arguments
parser = argparse.ArgumentParser(description='Sample Episodes from MineRL')
parser.add_argument('--enviourment', type=str, default='MineRLTreechop-v0')
#parser.add_argument('--dir', type=str, default="samples")
parser.add_argument('--max_frames', type=int, default=0)
parser.add_argument('--max_episodes', type=int, default=-1)
#parser.add_argument('--size', type=int, default=64)
args = parser.parse_args()
​
# YOU ONLY NEED TO DO THIS ONCE!
data_root = os.getenv('MINERL_DATA_ROOT', 'data/')
if args.enviourment not in os.listdir(data_root):
    print(f"Downloading {args.enviourment}")
    minerl.data.download(data_root, experiment=args.enviourment)
​
def main():
    data = minerl.data.make(args.enviourment, data_dir='data/')
    image_number = 0
    image_list = []
    action_list = []
    reward_list = []
    stream_list = os.listdir(data_root + args.enviourment)
    for stream_idx, stream in enumerate(stream_list[:args.max_episodes]):
        try:
            for current_state, action, reward, next_state, done in data.load_data(stream):
                if (image_number < args.max_frames or args.max_frames == 0):
                    image_list.append(current_state)
                    action_list.append(action)
                    reward_list.append(reward)
                    image_number += 1
        #if stream is corrupted
        except:
            continue
        print(len(image_list))
​
​
    with bz2.BZ2File('episodes.pbz2', 'w') as f:
        cPickle.dump((image_list, action_list, reward_list), f)
​
    ### read the compressed pickle
    #bz2_file = bz2.BZ2File('episodes.pbz2', 'rb')
    #pickle = cPickle.load(bz2_file)
    #####
​
if __name__ == '__main__':
    main()

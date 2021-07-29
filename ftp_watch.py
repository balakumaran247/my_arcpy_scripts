import pysftp, json
import argparse, time

time.sleep(10)

host = 'ftp.address'
port = 22
username = 'username'
password = 'password'
conn = pysftp.Connection(host=host,username=username, password=password)

regular = []
directory = []
unknown = []
conn.walktree('/',
        lambda x:regular.append(x),
        lambda y:directory.append(y),
        lambda z:unknown.append(z))

conn.close()

parser = argparse.ArgumentParser()
parser.add_argument("--update", help="if current list to be updated in database")
args = parser.parse_args()

current_file = './current.json'
to_download_file = './to_download.txt'
output_file = './output.txt'

regular_dict = {'files': regular}
to_download = []

if args.update==None:
    '''
    command if executed is :
    python ftp_watch.py
    '''
    with open (current_file, 'r') as json_file:
        current_json = json.load(json_file)
    for i in regular:
        if i not in current_json['files']:
            to_download.append(i)
    length = len(to_download)
    to_download_open = open(to_download_file,'w')
    for item in to_download:
        to_download_open.writelines(item+'\n')
    to_download_open.close()
    output_open = open(output_file,'w')
    output_open.write('%d' % length)
    output_open.close()

elif args.update=='yes':
    '''
    command if executed is :
    python ftp_watch.py --update yes
    '''
    with open(current_file, 'w') as json_file:
        json.dump(regular_dict, json_file, indent=4)

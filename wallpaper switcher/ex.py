# from json import load, dump
#
# x = ['风景', '自然', '清新', '简约', '山水', '创意']
# with open('data.json', 'r+') as fp:
#     data = load(fp)
#     data['api']['Ssyer']['cate_page'] = {y: 1 for y in x}
#     fp.seek(0)
#     dump(data, fp, indent=4)
#
# from re import search, findall, sub
# from requests import get, post, session
# #
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
#     # 'Cookie': 'SESSION=NDRmNTMyNTgtMTA3Yy00NGQ4LWI4ZWEtNDAzOTExODE2YzJm; _dg_playback.7b6028a56aac520d.ce42=1; _dg_abtestInfo.7b6028a56aac520d.ce42=1; _dg_check.7b6028a56aac520d.ce42=-1; _dg_antiBotFlag.7b6028a56aac520d.ce42=1; _dg_antiBotInfo.7b6028a56aac520d.ce42=10%7C%7C%7C3600; uid=129836; count=undefined; _dg_id.7b6028a56aac520d.ce42=3bcdb26013e1c132%7C%7C%7C1568552282%7C%7C%7C4%7C%7C%7C1569947280%7C%7C%7C1569947280%7C%7C%7C%7C%7C%7C6bc5cca980127be0%7C%7C%7C%7C%7C%7C%7C%7C%7C0%7C%7C%7Cundefined; _dg_antiBotMap.7b6028a56aac520d.ce42=201910020027%7C%7C%7C1'
# }
#
# r = ''.join(get('https://visualhunt.com/photos/nature/600').text.split())
# l = findall('divclass="vh-Collage-item".*?<atitle=.*?href="(.*?)"><img.*?src="(.*?)\?s=s"', r)
# for i in l:
#     r = ''.join(get('https://visualhunt.com'+i[0]).text.split())
#     print(search('.*<span>(\d*)x(\d*)\(.*?\).*?$', r).groups())
from multiprocessing import Process, Queue


def work(num, q):
    while True:
        print('waiting...')
        item = q.get(True)
        print('{0} has work: {1}'.format(num, item))
        print('done')

def main():
    queue = Queue()
    for i in range(20):
        queue.put(i)
    p1 = Process(target=work, args=(1, queue))
    p2 = Process(target=work, args=(2, queue))
    p1.start()
    p2.start()
    p2.join()
    p2.join()
    print('all done')

if __name__ == '__main__':
    main()

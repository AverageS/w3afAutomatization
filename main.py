import subprocess
import time
import logging

def make_string(url_name):
    start_sequence = '''profiles use sqli_and_xss\nplugins output config text_file'''
    start_sequence += "set output_file '~/" + url_name.replace('/', '') + ".txt'\n"
    start_sequence += '''save\nback\nplugins output config html_file\n'''
    start_sequence += "set output_file '~/" +  url_name.replace('/', '') + ".html'\n"
    start_sequence += "save\nback\ntarget set target " +  url_name + "\nsave\ncleanup\nstart\n"
    logging.debug(start_sequence)
    return start_sequence


def main(filename='urls'):
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    with open(filename, 'r') as fp:
        urls = fp.readlines()
    urls = list(map(lambda x: 'https://' + x.replace('\n', '') if 'https://' not in x else x.replace('\n', ''), urls))
    script_names = [x.replace('/', '') + '.w3af' for x in urls]
    for index, script_name in enumerate(script_names):
        with open(script_name, 'w') as fp:
            fp.write(make_string(urls[index]))

    for script_name in script_names:
        args = './w3af_console -s ' + script_name
        pop = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE)
        time.sleep(600)
        pop.poll()
        pop.kill()
        logging.info(script_name + 'has finished')






if __name__ == '__main__':
    main()
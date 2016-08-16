import subprocess
import time


def make_string(url_name):
    start_sequence = '''profiles use sqli_and_xss\nplugins output config text_file'''
    start_sequence += "set output_file '~/" + url_name.replace('/', '') + ".txt'\n"
    start_sequence += '''save\nback\nplugins output config html_file\n'''
    start_sequence += "set output_file '~/" +  url_name.replace('/', '') + ".html'\n"
    start_sequence += "save\nback\ntarget set " +  url_name.replace('/', '') + "\nstart\n"
    return start_sequence


def main(filename='urls'):
    urls = []
    with open(filename, 'r') as fp:
        urls = fp.readlines()
    script_names = [x.replace('\n', '') + '.w3af' for x in urls]
    for index, script_name in enumerate(script_names):
        with open(script_name, 'w') as fp:
            fp.write(make_string(urls[index]))

    pops = []

    for script_name in script_names:
        args = './w3af_console -s ' + script_name
        pops.append(subprocess.Popen(args, shell=True, stdout=subprocess.PIPE))

    time.sleep(3600)

    for pop in pops:
        pop.poll()
        pop.kill()


if __name__ == '__main__':
    main()
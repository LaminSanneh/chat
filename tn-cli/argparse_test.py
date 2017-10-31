import argparse
import shlex

def parse_command(cmd):
    """Parses command line input into a dictionary"""
    parts = shlex.split(cmd)
    parser = None
    if parts[0] == "acc":
        parser = argparse.ArgumentParser(prog=parts[0], description='Create or alter an account')
        parser.add_argument('--user', default=None, help='ID of the account to update')
        parser.add_argument('--scheme', default="basic", help='authentication scheme, default=basic')
        parser.add_argument('--secret', default=None, help='secret for authentication')
        parser.add_argument('--uname', default=None, help='user name for basic authentication')
        parser.add_argument('--password', default=None, help='password for basic authentication')
        parser.add_argument('--do-login', action='store_true', help='login with the newly created account')
        parser.add_argument('--tags', action=None, help='tags for user discovery, comma separated list without spaces')
        parser.add_argument('--fn', default=None, help='user\'s human name')
        parser.add_argument('--photo', default=None, help='avatar file name')
        parser.add_argument('--private', default=None, help='user\'s private info')
        parser.add_argument('--auth', default=None, help='default access mode for authenticated users')
        parser.add_argument('--anon', default=None, help='default access mode for anonymous users')
    elif parts[0] == "login":
        parser = argparse.ArgumentParser(prog=parts[0], description='Authenticate current session')
        parser.add_argument('--scheme', default="basic")
        parser.add_argument('secret', nargs='?', default=argparse.SUPPRESS)
        parser.add_argument('--secret', dest='secret', default=None)
        parser.add_argument('--uname', default=None)
        parser.add_argument('--password', default=None)
    elif parts[0] == "sub":
        parser = argparse.ArgumentParser(prog=parts[0], description='Subscribe to topic')
        parser.add_argument('topic', nargs='?', default=argparse.SUPPRESS, help='topic to subscribe to')
        parser.add_argument('--topic', dest='topic', default=None, help='topic to subscribe to')
        parser.add_argument('--fn', default=None, help='topic\'s user-visible name')
        parser.add_argument('--photo', default=None, help='avatar file name')
        parser.add_argument('--private', default=None, help='topic\'s private info')
        parser.add_argument('--auth', default=None, help='default access mode for authenticated users')
        parser.add_argument('--anon', default=None, help='default access mode for anonymous users')
        parser.add_argument('--get-query', default=None, help='query for topic metadata or messages')
    elif parts[0] == "leave":
        parser = argparse.ArgumentParser(prog=parts[0], description='Detach or unsubscribe from topic')
        parser.add_argument('topic', nargs='?', default=argparse.SUPPRESS, help='topic to detach from')
        parser.add_argument('--topic', dest='topic', default=None, help='topic to detach from')
        parser.add_argument('--unsub', action='store_true', help='detach and unsubscribe from topic')
    elif parts[0] == "pub":
        parser = argparse.ArgumentParser(prog=parts[0], description='Send message to topic')
        parser.add_argument('topic', nargs='?', default=argparse.SUPPRESS, help='topic to publish to')
        parser.add_argument('--topic', dest='topic', default=None, help='topic to publish to')
        parser.add_argument('content', nargs='?', default=argparse.SUPPRESS, help='message to send')
        parser.add_argument('--content', dest='content', help='message to send')
    elif parts[0] == "get":
        parser = argparse.ArgumentParser(prog=parts[0], description='Query topic for messages or metadata')
        parser.add_argument('topic', nargs='?', default=argparse.SUPPRESS, help='topic to update')
        parser.add_argument('--topic', dest='topic', default=None, help='topic to update')
        parser.add_argument('--desc', action='store_true', help='query topic description')
        parser.add_argument('--sub', action='store_true', help='query topic subscriptions')
        parser.add_argument('--data', action='store_true', help='query topic messages')
    elif parts[0] == "set":
        parser = argparse.ArgumentParser(prog=parts[0], description='Update topic metadata')
        parser.add_argument('topic', nargs='?', default=argparse.SUPPRESS, help='topic to update')
        parser.add_argument('--topic', dest='topic', default=None, help='topic to update')
        parser.add_argument('--fn', default=None, help='topic\'s name')
        parser.add_argument('--photo', default=None, help='avatar file name')
        parser.add_argument('--private', default=None, help='topic\'s private info')
        parser.add_argument('--auth', default=None, help='default access mode for authenticated users')
        parser.add_argument('--anon', default=None, help='default access mode for anonymous users')
        parser.add_argument('--user', default=None, help='ID of the account to update')
        parser.add_argument('--mode', default=None, help='new value of access mode')
    elif parts[0] == "del":
        parser = argparse.ArgumentParser(prog=parts[0], description='Delete message(s), subscription or topic')
        parser.add_argument('topic', nargs='?', default=argparse.SUPPRESS, help='topic being affected')
        parser.add_argument('--topic', dest='topic', default=None, help='topic being affected')
        parser.add_argument('what', choices=('msg', 'sub', 'topic'), nargs='?', help='what to delete')
        parser.add_argument('--what', choices=('msg', 'sub', 'topic'), help='what to delete')
        parser.add_argument('param', help='list of message IDs or a user ID of subscription to delete')
        group = parser.add_mutually_exclusive_group()
        group.add_argument('--before', dest='param', help='delete messages with id below or equal to this value')
        group.add_argument('--user', dest='param', help='delete subscription with the given user id')
        group.add_argument('--list', dest='param', help='comma separated list of message IDs to delete')
        parser.add_argument('--hard', help='hard-delete messages')
    elif parts[0] == "note":
        parser = argparse.ArgumentParser(prog=parts[0], description='Send notification to topic, ex "note kp"')
        parser.add_argument('topic', nargs='?', default=argparse.SUPPRESS, help='topic to notify')
        parser.add_argument('--topic', dest='topic', default=None, help='topic to notify')
        parser.add_argument('what', nargs='?', choices=('kp', 'read', 'recv'), help='notification type')
        parser.add_argument('--what', dest='what', choices=('kp', 'read', 'recv'), help='notification type')
        parser.add_argument('--seq', help='value being reported')
    else:
        print "Unrecognized:", parts[0]
        print "Possible commands:"
        print "\tacc\t- create account"
        print "\tlogin\t- authenticate"
        print "\tsub\t- subscribe to topic"
        print "\tleave\t- detach or unsubscribe from topic"
        print "\tpub\t- post message to topic"
        print "\tget\t- query topic for metadata or messages"
        print "\tset\t- update topic metadata"
        print "\tdel\t- delete message(s), topic or subscription"
        print "\tnote\t- send notification"
        print "\n\tType <command> -h for help"
        return None

    try:
        return parser.parse_args(parts[1:])
    except SystemExit:
        return None

def run():
    while True:
        inp = raw_input("tn> ")
        if inp == "":
            continue
        if inp == "exit" or inp == "quit":
            return
        cmd = parse_command(inp)
        if cmd != None:
            print cmd

if __name__ == '__main__':
    run()
import getpass
import argparse

import sys
import pathlib
import collections

import box
import requests
import requests_html

Emoji = collections.namedtuple('Emoji', 'name src')


class Slack:
    def __init__(self, workspace, email, password):
        self.session = requests_html.HTMLSession()
        self.url = f'https://{workspace}.slack.com'
        self.login(email, password)
        self.upload_crumb = self.get_upload_crumb()

    @property
    def login_form_url(self):
        return f'{self.url}/?no_sso=1'

    @property
    def upload_form_url(self):
        return f'{self.url}/admin/emoji'

    @property
    def upload_image_url(self):
        return f'{self.url}/customize/emoji'

    def _get_tokens(self):
        result = self.session.get(self.login_form_url)
        signin = result.html.find('#signin_form input[name="signin"]', first=True)
        redir = result.html.find('#signin_form input[name="redir"]', first=True)
        crumb = result.html.find('#signin_form input[name="crumb"]', first=True)
        assert all(x is not None for x in [signin, redir, crumb]), f"Could not get login form for {self.url}"
        return {
            'signin': signin.attrs['value'],
            'redir': redir.attrs['value'],
            'crumb': crumb.attrs['value'],
            'remember': 'on'
        }

    def login(self, email, password):
        tokens = self._get_tokens()
        payload = {**tokens, **{'email': email, 'password': password}}
        result = self.session.post(self.login_form_url, data=payload)
        if 'Enter your authentication code' in result.text:
            raise Exception("2FA currently not supported")

    def get_upload_crumb(self):
        result = self.session.get(self.upload_form_url)
        crumb = result.html.find('#addemoji > input[name="crumb"]', first=True)
        assert crumb is not None, 'Login error: could not get emoji upload crumb'
        return crumb.attrs['value']

    def upload(self, name, data):
        payload = {
            'add': '1',
            'crumb': self.upload_crumb,
            'name': name,
            'mode': 'data'
        }
        result = self.session.post(self.upload_image_url, data=payload, files={'img': data})
        assert result.status_code == 200


def iter_directory(path):
    dirpath = pathlib.Path(path)
    assert(dirpath.is_dir())
    for item in dirpath.iterdir():
        if item.is_file():
            yield Emoji(name=item.stem.replace('_', '-'), src=str(item))
        elif item.is_dir():
            yield from iter_directory(item)


def iter_hipchat(path):
    html = requests_html.HTML(html=open(path).read())
    for href in html.links:
        if 'emoticon' in href:
            name = '-'.join(pathlib.Path(href).stem.split('-')[:-1])
            src = href
            if name:
                yield Emoji(name, src)


def iter_emojipack(path):
    for emoji in box.Box.from_yaml(filename=path).emojis:
        yield Emoji(emoji.name, emoji.src)


def iter_emojis(emojis):
    for emoji in emojis:
        if pathlib.Path(emoji.src).is_file():
            data = open(emoji.src, 'rb')
        else:
            data = requests.get(emoji.src).content
        yield emoji.name, data


iterators = {
    'directory': iter_directory,
    'emojipack': iter_emojipack,
    'hipchat': iter_hipchat,
}


def convert_to_emojis(path, format):
    iterator_fn = iterators[format]
    return box.Box({'emojis': [dict(emoji._asdict()) for emoji in iterator_fn(path)]})


def upload_emojis(path, workspace, email, password, format, dry_run):
    emoji_box = convert_to_emojis(path, format)
    if dry_run:
        print(emoji_box.to_yaml())
        sys.exit()
    slack = Slack(workspace, email, password)
    print('Successfully logged in')
    for name, data in iter_emojis(emoji_box.emojis):
        slack.upload(name, data)
        print(f"Uploaded emoji {name}")


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='Filepath containing emojis')
    parser.add_argument('--workspace', required=True, help='Slack subdomain')
    parser.add_argument('--email', required=True, help='Email address for login')
    parser.add_argument('--format', default='directory', choices=['directory', 'emojipack', 'hipchat'])
    parser.add_argument('--dry-run', action='store_true', help='Print out emojis as emojipack')
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    if not args.dry_run:
        password = getpass.getpass(prompt='Password: ')
    else:
        password = None
    upload_emojis(password=password, **vars(args))


if __name__ == '__main__':
    main()

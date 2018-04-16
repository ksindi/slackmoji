# SlackMoji

Upload custom emojis to Slack. You can upload files from the following sources:
  - [Emojipacks](https://github.com/lambtron/emojipacks)
  - Directory
  - Hipchat

Requires Python 3.6+.

## Usage

```bash
git clone git@github.com:ksindi/slackmoji.git
cd slackmoji/
```

### Upload from directory

Below will upload all files inside a directory with the filename as the emoji name:

```bash
python slackmoji /path/to/emojis --workspace myworkspace --email foo@example.com
```

### Upload from emojipack

```bash
slackmoji /path/to/emojipack --workspace myworkspace --email foo@example.com --format emojipack
```

### Upload from Hipchat

Go to https://{you_workspace}.hipchat.com/emoticons and download the source url.

```bash
slackmoji /path/to/source_url --workspace myworkspace --email foo@example.com --format hipchat
```

## Debugging

You can see the emojis to be uploaded (without uploading) by using the option `--dry-run`.

## Limitations

Following features not supported:
  - 2FA
  - Emoji aliases

## Credit

Code inspired by [Emojipacks](https://github.com/lambtron/emojipacks).

## License

MIT

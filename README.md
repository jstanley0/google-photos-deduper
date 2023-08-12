# Google Photos Deduper

Locally run web app + Chrome extension to delete duplicates within Google Photos. [Watch a short demo](TODO).

Personal project by [Mack Talcott](https://github.com/mtalcott).

## Motivation

I've been a long-time user of [Google Photos](http://photos.google.com). When [Picasa Web Albums](https://picasa.google.com) retired, my cloud photos and albums moved to Google Photos. I have used nearly every desktop client Google provided from Picasa, to the old Google Photos desktop uploader, to [Google Drive's built-in Photos integration](https://www.blog.google/products/photos/simplifying-google-photos-and-google-drive/), and finally to [Backup and Sync](https://www.google.com/drive/download/backup-and-sync/).

Google has improved duplicate detection upon upload in recent years, but that wasn't always the case. I have thousands of photos across dozens of albums that, through one OS reinstall or another, were duplicated by a desktop client. Additionally, duplicates can still make their way in through other means. For example, deleting a photo, re-uploading it, then restoring the original results in a duplicate even today.

This could probably be solved by clearing out my Photos data and re-uploading everything. However, that would remove all album organization and photo descriptions. Instead, it's preferred to remove duplicates in-place. [Searches](https://support.google.com/photos/thread/3954223/is-there-an-easy-way-to-delete-duplicate-photos?hl=en) [show](https://www.quora.com/How-does-one-delete-duplicate-photos-in-Google-Photos-from-the-web-or-from-the-app-Is-there-feature-where-you-can-scan-and-delete-for-duplicates) interest in this feature from the Google Photos user base, but it hasn't ever made its way into the product.

The existing tools I could find for this problem did so only with media on the local computer, felt scammy, or didn't fully automate the deletion process. So I built my own.

It turns out the [Google Photos API](https://developers.google.com/photos) is quite limited. While apps can read limited metadata about the media items in a user's library, they cannot delete media items (photos and videos), and they can only modify media items uploaded by the app itself. This means we can't, for example, add all of the duplicates to an album for the user to review. This necessitates some kind of tool to automate the deletion of duplicates. Since we've already bought in to the Google ecosystem as a Photos user, I chose to do this with a complementary Chrome extension.

## Getting Started

For privacy and cost reasons, no public hosted solution is currently provided. Instead, follow these instructions to get the app up and running locally:

### Setup

1. Install [Docker Desktop](https://docs.docker.com/desktop/) on your system.
1. Clone this repository.
1. Generate an app client secret file. (No hosted solution currently provided.)
   a. Follow [these instructions](https://developers.google.com/identity/protocols/oauth2/web-server#creatingcred) to create a project and OAuth 2.0 Client ID for a web application using Google Developer Console.
   a. Download your client secret file.
   a. `cp .example.env .env`
   a. Generate [`FLASK_SECRET_KEY`](https://flask.palletsprojects.com/en/2.3.x/config/#SECRET_KEY) with `python -c 'import secrets; print(secrets.token_hex())'` and add it to `.env`.
   a. Add `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` from the `client_id` and `client_secret` values from the client secret file you downloaded.
1. Run `docker-compose build` from the project directory.

### Start

- Run `docker-compose up` from the project directory.
- Load [http://localhost](http://localhost) and follow the instructions from there!
- [Install the Chrome Extension](chrome_extension/README.md) once you want to delete duplicates.

## Support

If you found a bug or have a feature request, please [open an issue](https://github.com/mtalcott/google-photos-deduper/issues/new/choose).

If you have questions about the tool, please [post on the discussions page](https://github.com/mtalcott/google-photos-deduper/discussions).

## Development

- Python app
  - Flask is set to debug mode, so live reloading is enabled.
  - Debugging with `debugpy` is supported. See [`launch.json`](.vscode/launch.json).
- React app
  - Utilizes [Vite](https://vitejs.dev/) for HMR and building.
- Chrome extension
  - Utilizes the [CRXJS Vite Plugin](https://crxjs.dev/vite-plugin) for HMR and building.

# Useless Apps

## Overview
This repository collects small Python utilities and shell scripts that automate email workflows, manage files, integrate with public APIs, and convert media. Each tool can be run independently, making it easy to reuse the code snippets for personal tasks or as a starting point for new experiments.

## Features
### Email utilities
- **sendEmailAuto.py** – Sends preconfigured Gmail messages with optional attachments using credentials from environment variables.
- **sendEmailPrompt.py** – Prompts for recipients, subject, body, and optional attachments before sending mail through Gmail.
- **waiting_instruction.py** – Monitors a Gmail inbox for new commands, replies automatically, and can trigger local automation such as launching an alarm script.
- **emailLib.py** – Provides IMAP helpers for connecting to servers, listing folders, counting messages, searching, and deleting mail.

### File and text helpers
- **filelib.py** – Supplies reusable functions for creating, reading, and editing files with configurable defaults.
- **rename_files.py** – Renames files or folders by replacing text, deleting segments, or adding prefixes and suffixes.
- **reindent.py** – Rewrites files with a new indentation width based on command-line parameters.

### Automation scripts
- **chk_os.py** – Detects the host operating system and prints diagnostic messages via dedicated handlers.
- **createRepo.py** – Builds shell commands to create a GitHub repository and push the local project, reading the username from environment variables.
- **waiting_instruction.py** – Uses pyautogui and keyboard libraries to automate launching a separate alarm application when instructed by email.

### Data and API clients
- **iex.py** – Retrieves market data from the IEX Trading API, including batch requests, book data, and charts.
- **jsonToPanda.py** – Normalizes IEX JSON responses with pandas utilities to compose chart datasets and merged DataFrames.
- **weather.py** – Fetches Dark Sky forecasts for predefined cities, prints localized summaries, and speaks the forecast with macOS voices.

### Media and conversion tools
- **text_to_mp3/run.py** – Reads lines from text.txt, uses macOS say to generate AIFF files, converts them to MP3 with lame, and cleans up intermediates.
- **videoToMp3/*.sh** – Provide ffmpeg helpers for converting MKV, MP4, or WebM videos to MP3 audio or H.264 video streams.

### Miscellaneous examples
- **rpn.py** – Implements a simple stack-based calculator that prints debug information for each operation.

## Environment variables
Several scripts expect credentials or API tokens to be available as environment variables:
- `my_email`, `my_email_password` – Gmail account used by the email sender and watcher utilities.
- `githubUser` – GitHub username used when provisioning repositories from the CLI helper.
- `weather_api_key` – Dark Sky API key required for weather forecasts.

Ensure these values are exported in your shell before running the respective scripts.

## Requirements
Many scripts target macOS utilities such as `say` and rely on third-party binaries like `lame` and `ffmpeg` for media conversion. API-focused scripts use Python packages including `pandas`, `requests`, `darksky`, `pyautogui`, and `keyboard`. Install the necessary tools and libraries before executing the corresponding utilities.

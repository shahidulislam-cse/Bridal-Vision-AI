<<<<<<< HEAD
# BridalVision AI

AI-powered virtual bridal fitting room using fal.ai IDM-VTON.

## Real-world problem this solves
Brides often spend weeks visiting boutiques and trying on dozens of dresses.
This is expensive, time-consuming, and difficult for people who live far away
or want to narrow options before visiting in person. BridalVision AI lets a
bride upload a full-body photo, pick a dress, and instantly see a realistic
preview of herself wearing it. That reduces decision fatigue and improves
appointment conversion for the boutique.

## What this contributes to (industry level)
Most bridal websites still show static photos only. By providing a virtual
try-on, boutiques can collect leads, increase engagement, and position their
brand as modern and tech-forward. This project bridges the gap between online
inspiration and in-store purchase intent.

## Scope (AI module only)
This repo contains only the AI integration. The backend developer will handle
Django setup, database models, auth, admin, email delivery, and deployment.

AI responsibilities in this repo:
- fal.ai API integration for virtual try-on (IDM-VTON)
- Photo upload validation and preprocessing
- Prompt engineering for bridal output quality
- Session limit logic (max 3 try-ons per session)
- Clean response formatting and error handling

## Key AI features
- Photo upload and validation
- Dress selection by URL
- Realistic dress fitting with body and pose preservation
- Natural lighting and shadow rendering
- Background-neutral output for easy UI placement
- Session limit enforcement (3 per session)

## Project structure (AI module)

```
Bridal-Vision-AI/
├── app/
│   ├── api/
│   │   └── endpoints.py        FastAPI routes
│   ├── core/
│   │   ├── config.py           Settings and environment variables
│   │   └── prompts.py          Prompt engineering utilities
│   ├── services/
│   │   └── fal_service.py      Core fal.ai wrapper
│   └── utils/
│       ├── image_utils.py      Photo validation and upload
│       └── session_utils.py    Session limit logic
├── tests/
├── docs/
├── main.py                     FastAPI entry point
├── requirements.txt
├── .env.example
└── .gitignore
```

## Setup

1) Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

2) Install dependencies

```bash
pip install -r requirements.txt
```

3) Configure environment variables

```bash
copy .env.example .env
```

Edit `.env` and set:

```
FAL_KEY=your_fal_api_key_here
```

4) Run the AI service

```bash
uvicorn main:app --reload --port 8001
```

Open docs at:

```
http://localhost:8001/docs
```

## API endpoints

### GET /api/health
Simple health check.

Response:

```json
{
  "status": "ok",
  "service": "BridalVision AI"
}
```

### POST /api/tryon
Multipart form upload for a virtual try-on.

Form fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| session_id | string | yes | Unique session ID from backend |
| garment_image_url | string | yes | URL of the selected dress |
| dress_style | string | no | ball_gown, a_line, mermaid, sheath, lace, off_shoulder, default |
| lighting | string | no | studio, outdoor, church, default |
| human_image | file | yes | Full-body photo (max 5MB) |

Success response:

```json
{
  "success": true,
  "result_image_url": "https://fal.ai/results/...",
  "tries_remaining": 2,
  "message": "Your virtual try-on is ready!"
}
```

Limit reached response:

```json
{
  "success": false,
  "result_image_url": null,
  "tries_remaining": 0,
  "message": "You have reached the maximum of 3 try-ons for this session."
}
```

## Image upload support
Supported input formats: JPG, JPEG, PNG, WEBP, BMP, TIFF, GIF (non-animated).
Non-JPEG/PNG images are converted to PNG in memory before upload to fal.ai.
If an image is animated or corrupted, the API returns a clear 400 error.

## GDPR and data privacy
- No user images are stored by the AI module
- Images are passed to fal.ai using temporary URLs
- Session counts are in-memory only (cleared on restart)
- Backend is responsible for retention policies, deletion, and email delivery

## Tests

```bash
pytest tests/
```

## Author

Shahidul Islam
Jr AI Engineer, Betopia Group / Join Venture AI
Dhaka, Bangladesh
=======
# Bridal-Vision-AI  



## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/topics/git/add_files/#add-files-to-a-git-repository) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://gitlab.betopialimited.com/join-venture-ai/bridal-vision-ai.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](https://gitlab.betopialimited.com/join-venture-ai/bridal-vision-ai/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Set auto-merge](https://docs.gitlab.com/user/project/merge_requests/auto_merge/)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing (SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thanks to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README

Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
>>>>>>> daf5b10454d4b8ced6474dbef0e176b439f52150

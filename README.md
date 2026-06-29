# CI/CD Pipeline with Docker + GitHub Actions (Flask)

A minimal Flask app with an automated pipeline: every push to `main` installs
dependencies, runs tests, then builds and pushes a Docker image to Docker Hub.

## Project structure

```
cicd-flask-docker/
├── app.py                  # Flask app
├── requirements.txt
├── tests/
│   └── test_app.py         # Pytest tests
├── Dockerfile
├── .dockerignore
└── .github/workflows/
    └── ci-cd.yml           # GitHub Actions pipeline
```

## Run locally

```bash
pip install -r requirements.txt
python app.py               # http://localhost:5000
```

## Run tests

```bash
pytest -v
```

## Run with Docker

```bash
docker build -t cicd-flask-docker .
docker run -p 5000:5000 cicd-flask-docker
```

## Set up the pipeline on GitHub

1. Create a new GitHub repo and push this project to it:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Flask app + CI/CD pipeline"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git push -u origin main
   ```

2. Create a Docker Hub access token:
   - Go to Docker Hub → Account Settings → Security → New Access Token.

3. Add two repository secrets in GitHub (Settings → Secrets and variables →
   Actions → New repository secret):
   - `DOCKERHUB_USERNAME` — your Docker Hub username
   - `DOCKERHUB_TOKEN` — the access token you just created

4. Push to `main`. Go to the **Actions** tab to watch the pipeline:
   - `build-and-test` installs dependencies and runs pytest.
   - `push-docker-image` (only runs on push to `main`, after tests pass)
     builds the Docker image and pushes it as:
     - `<dockerhub-username>/cicd-flask-docker:latest`
     - `<dockerhub-username>/cicd-flask-docker:<commit-sha>`

5. Pull and run the published image from anywhere:
   ```bash
   docker pull <dockerhub-username>/cicd-flask-docker:latest
   docker run -p 5000:5000 <dockerhub-username>/cicd-flask-docker:latest
   ```

## Extending to deployment

To deploy automatically after the image is pushed, add a `deploy` job that
needs `push-docker-image`, and either:
- SSH into a server and run `docker pull && docker compose up -d`
  (using `appleboy/ssh-action`), or
- Deploy to a cloud platform (AWS ECS/EC2, Azure App Service, Render,
  Railway, etc.) using that platform's GitHub Action.

Ask if you'd like that job added for a specific target — server, AWS, Azure,
or a PaaS like Render/Railway.

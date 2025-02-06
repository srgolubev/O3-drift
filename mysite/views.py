from django.shortcuts import render


def home(request):
    roadmap = [
        "User Management and CustomUser Model",
        "API Endpoints for Competitions and Profiles",
        "Containerized Setup with Docker, Docker Compose, and .env",
        "CI/CD with GitHub Actions",
    ]
    return render(request, "home.html", {"roadmap": roadmap})

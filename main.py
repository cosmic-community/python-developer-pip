# main.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv
from cosmicpy import CosmicPy
from typing import List, Dict, Any, Optional
import logging

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Python Developer Portfolio",
    description="A professional portfolio showcasing Python development expertise",
    version="1.0.0",
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize templates
templates = Jinja2Templates(directory="templates")

# Initialize Cosmic
cosmic = CosmicPy()
bucket = cosmic.bucket(
    bucket_slug=os.getenv('COSMIC_BUCKET_SLUG'),
    read_key=os.getenv('COSMIC_READ_KEY'),
    write_key=os.getenv('COSMIC_WRITE_KEY')
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_projects() -> List[Dict[str, Any]]:
    """Fetch all projects from Cosmic CMS"""
    try:
        response = bucket.get_objects(type='projects')
        return response.get('objects', [])
    except Exception as e:
        logger.error(f"Error fetching projects: {e}")
        return []

async def get_project_by_slug(slug: str) -> Optional[Dict[str, Any]]:
    """Fetch a specific project by slug"""
    try:
        response = bucket.get_object(slug=slug, type='projects')
        return response.get('object')
    except Exception as e:
        logger.error(f"Error fetching project {slug}: {e}")
        return None

async def get_skills() -> List[Dict[str, Any]]:
    """Fetch all skills from Cosmic CMS"""
    try:
        response = bucket.get_objects(type='skills')
        return response.get('objects', [])
    except Exception as e:
        logger.error(f"Error fetching skills: {e}")
        return []

async def get_about() -> Optional[Dict[str, Any]]:
    """Fetch about information from Cosmic CMS"""
    try:
        response = bucket.get_objects(type='about')
        objects = response.get('objects', [])
        return objects[0] if objects else None
    except Exception as e:
        logger.error(f"Error fetching about info: {e}")
        return None

def group_skills_by_category(skills: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Group skills by category"""
    grouped = {}
    for skill in skills:
        category_key = skill['metadata']['category']['key']
        category_value = skill['metadata']['category']['value']
        
        if category_key not in grouped:
            grouped[category_key] = {
                'name': category_value,
                'skills': []
            }
        grouped[category_key]['skills'].append(skill)
    
    return grouped

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    """Portfolio homepage"""
    projects = await get_projects()
    skills = await get_skills()
    about = await get_about()
    
    # Group skills by category
    grouped_skills = group_skills_by_category(skills)
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "projects": projects,
        "skills": grouped_skills,
        "about": about
    })

@app.get("/api/projects")
async def get_projects_api():
    """Get all projects via API"""
    projects = await get_projects()
    return {"projects": projects}

@app.get("/api/projects/{slug}")
async def get_project_api(slug: str):
    """Get specific project by slug via API"""
    project = await get_project_by_slug(slug)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"project": project}

@app.get("/api/skills")
async def get_skills_api():
    """Get all skills grouped by category via API"""
    skills = await get_skills()
    grouped_skills = group_skills_by_category(skills)
    return {"skills": grouped_skills}

@app.get("/api/about")
async def get_about_api():
    """Get about information via API"""
    about = await get_about()
    if not about:
        raise HTTPException(status_code=404, detail="About information not found")
    return {"about": about}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Portfolio API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
# Python Developer Portfolio

![App Preview](https://imgix.cosmicjs.com/d9c4a2b0-b502-11f0-84b8-c1eed342c5b6-photo-1556742049-0cfed4f6a45d-1761768428496.jpg?w=1200&h=300&fit=crop&auto=format,compress)

A professional portfolio website built with FastAPI that showcases Python development expertise. This application dynamically displays your projects, skills, and professional information managed through Cosmic CMS.

## ✨ Features

- **Dynamic Project Showcase** - Display projects with screenshots, tech stacks, and live demo links
- **Interactive Skills Matrix** - Categorized skills with proficiency levels and experience indicators
- **Professional About Section** - Comprehensive bio with experience timeline and contact information
- **Fast API Backend** - High-performance API endpoints with automatic OpenAPI documentation
- **Responsive Design** - Mobile-first approach with modern CSS styling
- **Real-time Content** - Content updates instantly through Cosmic CMS
- **SEO Optimized** - Proper meta tags and structured data for search engines
- **Performance Optimized** - Fast loading with image optimization and caching

## Clone this Project

Want to create your own version of this project with all the content and structure? Clone this Cosmic bucket and code repository to get started instantly:

[![Clone this Project](https://img.shields.io/badge/Clone%20this%20Project-29abe2?style=for-the-badge&logo=cosmic&logoColor=white)](https://app.cosmicjs.com/projects/new?clone_bucket=69027397271316ad9f4cc8ed&clone_repository=69027528271316ad9f4cc938)

## Prompts

This application was built using the following prompts to generate the content structure and code:

### Content Model Prompt

> "Create a content model for a Python developer portfolio with:
- Projects (title, description, tech stack, github link)
- Skills (name, proficiency level, category)
- About section (bio, experience)

This will showcase Python web development capabilities."

### Code Generation Prompt

> Based on the content model I created, now build a complete Python web application that showcases this content using pip. 

Create a FastAPI application with:
- Modern, responsive design with proper navigation
- Content display from Cosmic CMS
- API endpoints for content retrieval
- Production-ready deployment configuration for Vercel
- Proper error handling and performance optimization

Use pip for all dependency management.

The app has been tailored to work with your existing Cosmic content structure and includes all the features requested above.

## 🛠️ Technologies Used

- **Backend**: FastAPI, Python 3.11+
- **CMS**: Cosmic Headless CMS
- **Frontend**: HTML5, CSS3, JavaScript ES6+
- **Styling**: Custom CSS with responsive design
- **Deployment**: Vercel (Serverless Functions)
- **Package Management**: pip with requirements.txt
- **API Documentation**: FastAPI auto-generated OpenAPI/Swagger docs

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- pip (Python package installer)
- A Cosmic account with your content model set up

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd python-portfolio
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment Setup**
Create a `.env` file in the root directory:
```env
COSMIC_BUCKET_SLUG=your-bucket-slug
COSMIC_READ_KEY=your-read-key
COSMIC_WRITE_KEY=your-write-key
```

5. **Run the application**
```bash
uvicorn main:app --reload
```

The application will be available at `http://localhost:8000`

## 📖 Cosmic SDK Examples

### Fetching Projects
```python
from cosmicpy import CosmicPy

cosmic = CosmicPy()
bucket = cosmic.bucket(
    bucket_slug='your-bucket-slug',
    read_key='your-read-key'
)

# Get all projects
projects = bucket.get_objects(type='projects')

# Get a specific project by slug
project = bucket.get_object(slug='project-slug', type='projects')
```

### Fetching Skills by Category
```python
# Get all skills
skills = bucket.get_objects(type='skills')

# Filter skills by category (done in application logic)
programming_skills = [
    skill for skill in skills['objects'] 
    if skill['metadata']['category']['key'] == 'programming_languages'
]
```

## 🌐 Cosmic CMS Integration

This application integrates with your Cosmic bucket using the following object types:

### Projects Object Type
- **title**: Project name
- **description**: HTML description with features
- **tech_stack**: Technologies used
- **github_url**: Repository link
- **demo_url**: Live demo link
- **category**: Project category (Web App, API, Data Science, etc.)
- **screenshot**: Project preview image

### Skills Object Type
- **name**: Skill name
- **proficiency**: Beginner, Intermediate, Advanced, Expert
- **category**: Programming Languages, Frameworks, Databases, Tools & DevOps, Cloud Platforms, Other
- **years_experience**: Years of experience with this skill

### About Object Type (Singleton)
- **bio**: Professional biography (HTML)
- **total_experience**: Total years of experience
- **current_role**: Current job title
- **location**: Current location
- **headshot**: Professional photo
- **resume**: Resume/CV file

## 🚀 Deployment Options

### Vercel (Recommended)
1. Connect your repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically on git push

### Manual Deployment
1. Build the application: `pip install -r requirements.txt`
2. Set production environment variables
3. Deploy using your preferred hosting service

The application includes a `vercel.json` configuration file for seamless Vercel deployment with proper routing for both the API and static assets.

## 📁 API Endpoints

- `GET /` - Portfolio homepage
- `GET /api/projects` - Get all projects
- `GET /api/projects/{slug}` - Get specific project
- `GET /api/skills` - Get all skills grouped by category
- `GET /api/about` - Get about information
- `GET /docs` - FastAPI auto-generated API documentation

Visit `/docs` when running locally to explore the interactive API documentation.

<!-- README_END -->
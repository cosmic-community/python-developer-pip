# utils/helpers.py
import re
from typing import Any, Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def clean_html(html_content: str) -> str:
    """Clean HTML content for safe display"""
    if not html_content:
        return ""
    
    # Remove script tags for security
    html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove potentially dangerous attributes
    dangerous_attrs = ['onload', 'onclick', 'onerror', 'onmouseover', 'javascript:']
    for attr in dangerous_attrs:
        html_content = re.sub(rf'{attr}[^>]*', '', html_content, flags=re.IGNORECASE)
    
    return html_content

def format_tech_stack(tech_stack: str) -> List[str]:
    """Format tech stack string into a list of technologies"""
    if not tech_stack:
        return []
    
    # Split by common delimiters and clean up
    technologies = re.split(r'[,;]', tech_stack)
    return [tech.strip() for tech in technologies if tech.strip()]

def get_proficiency_percentage(proficiency_key: str) -> int:
    """Convert proficiency level to percentage for progress bars"""
    proficiency_map = {
        'beginner': 25,
        'intermediate': 50,
        'advanced': 75,
        'expert': 100
    }
    return proficiency_map.get(proficiency_key.lower(), 0)

def get_proficiency_color(proficiency_key: str) -> str:
    """Get color class for proficiency level"""
    color_map = {
        'beginner': '#ef4444',
        'intermediate': '#f59e0b', 
        'advanced': '#2563eb',
        'expert': '#10b981'
    }
    return color_map.get(proficiency_key.lower(), '#64748b')

def format_years_experience(years: Any) -> str:
    """Format years of experience for display"""
    if not years:
        return ""
    
    try:
        years_int = int(years)
        if years_int == 1:
            return "1 year"
        else:
            return f"{years_int} years"
    except (ValueError, TypeError):
        return ""

def optimize_image_url(image_url: str, width: int = 400, height: int = 300, quality: int = 80) -> str:
    """Optimize image URL with imgix parameters"""
    if not image_url:
        return ""
    
    # Check if it's already an imgix URL
    if 'imgix.cosmicjs.com' in image_url:
        # Add or update parameters
        separator = '&' if '?' in image_url else '?'
        return f"{image_url}{separator}w={width}&h={height}&fit=crop&auto=format,compress&q={quality}"
    
    return image_url

def truncate_text(text: str, max_length: int = 150) -> str:
    """Truncate text to specified length with ellipsis"""
    if not text or len(text) <= max_length:
        return text
    
    # Remove HTML tags for length calculation
    clean_text = re.sub(r'<[^>]+>', '', text)
    
    if len(clean_text) <= max_length:
        return text
    
    # Truncate at word boundary
    truncated = clean_text[:max_length].rsplit(' ', 1)[0]
    return f"{truncated}..."

def extract_text_from_html(html_content: str) -> str:
    """Extract plain text from HTML content"""
    if not html_content:
        return ""
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', html_content)
    
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def validate_url(url: str) -> bool:
    """Validate URL format"""
    if not url:
        return False
    
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return url_pattern.match(url) is not None

def sort_projects_by_category(projects: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Sort projects by category"""
    categories = {}
    
    for project in projects:
        category = project['metadata'].get('category', {})
        category_key = category.get('key', 'other')
        category_name = category.get('value', 'Other')
        
        if category_key not in categories:
            categories[category_key] = {
                'name': category_name,
                'projects': []
            }
        
        categories[category_key]['projects'].append(project)
    
    # Sort projects within each category by title
    for category_data in categories.values():
        category_data['projects'].sort(key=lambda x: x.get('title', ''))
    
    return categories

def get_current_year() -> str:
    """Get current year as string"""
    return str(datetime.now().year)

def log_error(message: str, error: Exception = None) -> None:
    """Log error with consistent format"""
    if error:
        logger.error(f"{message}: {str(error)}")
    else:
        logger.error(message)

def safe_get_nested_value(data: Dict[str, Any], path: str, default: Any = None) -> Any:
    """Safely get nested dictionary value using dot notation"""
    try:
        keys = path.split('.')
        value = data
        for key in keys:
            value = value[key]
        return value
    except (KeyError, TypeError, AttributeError):
        return default
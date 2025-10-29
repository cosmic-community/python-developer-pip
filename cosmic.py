# cosmic.py
import os
from typing import List, Dict, Any, Optional
from cosmicpy import CosmicPy
import logging

logger = logging.getLogger(__name__)

class CosmicClient:
    def __init__(self):
        self.cosmic = CosmicPy()
        self.bucket = self.cosmic.bucket(
            bucket_slug=os.getenv('COSMIC_BUCKET_SLUG'),
            read_key=os.getenv('COSMIC_READ_KEY'),
            write_key=os.getenv('COSMIC_WRITE_KEY')
        )
    
    async def get_projects(self) -> List[Dict[str, Any]]:
        """Fetch all projects from Cosmic CMS"""
        try:
            response = self.bucket.get_objects(type='projects')
            return response.get('objects', [])
        except Exception as e:
            logger.error(f"Error fetching projects: {e}")
            return []
    
    async def get_project_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        """Fetch a specific project by slug"""
        try:
            response = self.bucket.get_object(slug=slug, type='projects')
            return response.get('object')
        except Exception as e:
            logger.error(f"Error fetching project {slug}: {e}")
            return None
    
    async def get_skills(self) -> List[Dict[str, Any]]:
        """Fetch all skills from Cosmic CMS"""
        try:
            response = self.bucket.get_objects(type='skills')
            return response.get('objects', [])
        except Exception as e:
            logger.error(f"Error fetching skills: {e}")
            return []
    
    async def get_about(self) -> Optional[Dict[str, Any]]:
        """Fetch about information from Cosmic CMS"""
        try:
            response = self.bucket.get_objects(type='about')
            objects = response.get('objects', [])
            return objects[0] if objects else None
        except Exception as e:
            logger.error(f"Error fetching about info: {e}")
            return None
    
    def group_skills_by_category(self, skills: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Group skills by category"""
        grouped = {}
        
        # Define category order for consistent display
        category_order = [
            'programming_languages',
            'frameworks', 
            'databases',
            'tools',
            'cloud',
            'other'
        ]
        
        # Group skills by category
        for skill in skills:
            category_key = skill['metadata']['category']['key']
            category_value = skill['metadata']['category']['value']
            
            if category_key not in grouped:
                grouped[category_key] = {
                    'name': category_value,
                    'skills': []
                }
            grouped[category_key]['skills'].append(skill)
        
        # Sort skills within each category by proficiency level
        proficiency_order = {'expert': 4, 'advanced': 3, 'intermediate': 2, 'beginner': 1}
        
        for category in grouped.values():
            category['skills'].sort(
                key=lambda x: (
                    proficiency_order.get(x['metadata']['proficiency']['key'], 0),
                    x['metadata'].get('years_experience', 0)
                ),
                reverse=True
            )
        
        # Return ordered by category preference
        ordered_grouped = {}
        for category_key in category_order:
            if category_key in grouped:
                ordered_grouped[category_key] = grouped[category_key]
        
        # Add any remaining categories not in the order
        for category_key, category_data in grouped.items():
            if category_key not in ordered_grouped:
                ordered_grouped[category_key] = category_data
        
        return ordered_grouped

# Create global instance
cosmic_client = CosmicClient()
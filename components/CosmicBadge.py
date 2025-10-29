# components/CosmicBadge.py
import os
from typing import Optional

class CosmicBadge:
    """Cosmic badge component for portfolio attribution"""
    
    @staticmethod
    def render_badge_script(bucket_slug: Optional[str] = None) -> str:
        """Generate the cosmic badge JavaScript for client-side rendering"""
        if not bucket_slug:
            bucket_slug = os.getenv('COSMIC_BUCKET_SLUG', 'your-bucket-slug')
        
        return f"""
        <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const createCosmicBadge = () => {{
                const isDismissed = localStorage.getItem('cosmic-badge-dismissed');
                if (isDismissed) return;
                
                const bucketSlug = '{bucket_slug}';
                
                const badge = document.createElement('a');
                badge.id = 'cosmic-badge';
                badge.href = `https://www.cosmicjs.com?utm_source=bucket_${{bucketSlug}}&utm_medium=referral&utm_campaign=app_badge&utm_content=built_with_cosmic`;
                badge.target = '_blank';
                badge.rel = 'noopener noreferrer';
                badge.innerHTML = `
                    <button id="cosmic-dismiss" style="
                        position: absolute;
                        top: -8px;
                        right: -8px;
                        width: 24px;
                        height: 24px;
                        background: #f3f4f6;
                        border: none;
                        border-radius: 50%;
                        color: #374151;
                        font-size: 16px;
                        font-weight: bold;
                        cursor: pointer;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        transition: background-color 0.2s;
                        z-index: 10;
                    ">×</button>
                    <img src="https://cdn.cosmicjs.com/b67de7d0-c810-11ed-b01d-23d7b265c299-logo508x500.svg" 
                         alt="Cosmic Logo" 
                         style="width: 20px; height: 20px;">
                    Built with Cosmic
                `;
                
                Object.assign(badge.style, {{
                    position: 'fixed',
                    bottom: '20px',
                    right: '20px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    color: '#11171A',
                    textDecoration: 'none',
                    fontSize: '14px',
                    fontWeight: '500',
                    backgroundColor: 'white',
                    border: '1px solid #e5e7eb',
                    padding: '12px 16px',
                    width: '180px',
                    borderRadius: '8px',
                    zIndex: '50',
                    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
                    transition: 'background-color 0.2s ease',
                    fontFamily: 'system-ui, -apple-system, sans-serif'
                }});
                
                document.body.appendChild(badge);
                
                // Add dismiss functionality
                document.getElementById('cosmic-dismiss').onclick = (e) => {{
                    e.preventDefault();
                    e.stopPropagation();
                    badge.remove();
                    localStorage.setItem('cosmic-badge-dismissed', 'true');
                }};
                
                // Add hover effect
                const dismissBtn = document.getElementById('cosmic-dismiss');
                dismissBtn.onmouseenter = () => dismissBtn.style.backgroundColor = '#e5e7eb';
                dismissBtn.onmouseleave = () => dismissBtn.style.backgroundColor = '#f3f4f6';
                
                badge.onmouseenter = () => badge.style.backgroundColor = '#f9fafb';
                badge.onmouseleave = () => badge.style.backgroundColor = 'white';
            }};
            
            // Show badge after delay
            setTimeout(createCosmicBadge, 1000);
        }});
        </script>
        """
    
    @staticmethod
    def get_badge_html(bucket_slug: Optional[str] = None) -> str:
        """Get the complete HTML for the cosmic badge including script"""
        return f"""
        <!-- Built with Cosmic badge -->
        {CosmicBadge.render_badge_script(bucket_slug)}
        """
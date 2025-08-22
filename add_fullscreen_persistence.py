#!/usr/bin/env python3
"""
Add fullscreen persistence to presentation slides
Remembers fullscreen state across page navigation
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

def update_slide_with_fullscreen_persistence(slide_file):
    """Update a single slide with fullscreen persistence"""
    
    with open(slide_file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find all navigation links
    nav_links = soup.find_all('a', class_=['nav-prev', 'nav-next', 'nav-home'])
    
    # Update each link to save fullscreen state before navigation
    for link in nav_links:
        if link.get('href'):
            # Add onclick handler to save state
            link['onclick'] = 'saveFullscreenState(); return true;'
    
    # Find the keyboard navigation script
    script_tags = soup.find_all('script')
    
    # Create enhanced script with fullscreen persistence
    enhanced_script = '''
    <script>
        // Save fullscreen state before navigation
        function saveFullscreenState() {
            if (document.fullscreenElement) {
                sessionStorage.setItem('wasFullscreen', 'true');
            } else {
                sessionStorage.removeItem('wasFullscreen');
            }
        }
        
        // Restore fullscreen state on page load
        function restoreFullscreenState() {
            if (sessionStorage.getItem('wasFullscreen') === 'true') {
                // Small delay to ensure page is fully loaded
                setTimeout(() => {
                    document.documentElement.requestFullscreen().then(() => {
                        console.log('Fullscreen restored');
                        // Clear the flag after successful restore
                        // Keep it for continuous navigation
                        // sessionStorage.removeItem('wasFullscreen');
                    }).catch(err => {
                        console.log('Could not restore fullscreen:', err);
                        // Clear on error to prevent repeated attempts
                        sessionStorage.removeItem('wasFullscreen');
                    });
                }, 100);
            }
        }
        
        // Enhanced keyboard navigation with state saving
        document.addEventListener('keydown', function(e) {
            switch(e.key) {
                case 'ArrowLeft':
                    const prevLink = document.querySelector('.nav-prev:not(.nav-disabled)');
                    if (prevLink) {
                        saveFullscreenState();
                        prevLink.click();
                    }
                    break;
                case 'ArrowRight':
                case ' ':
                    e.preventDefault();
                    const nextLink = document.querySelector('.nav-next:not(.nav-disabled)');
                    if (nextLink) {
                        saveFullscreenState();
                        nextLink.click();
                    }
                    break;
                case 'Home':
                    e.preventDefault();
                    const homeLink = document.querySelector('.nav-home');
                    if (homeLink) {
                        saveFullscreenState();
                        homeLink.click();
                    }
                    break;
                case 'f':
                case 'F':
                    if (document.fullscreenElement) {
                        document.exitFullscreen();
                        sessionStorage.removeItem('wasFullscreen');
                    } else {
                        document.documentElement.requestFullscreen();
                        sessionStorage.setItem('wasFullscreen', 'true');
                    }
                    break;
                case 'Escape':
                    // Clear fullscreen state when user explicitly exits
                    sessionStorage.removeItem('wasFullscreen');
                    break;
            }
        });
        
        // Listen for fullscreen changes
        document.addEventListener('fullscreenchange', function() {
            if (!document.fullscreenElement) {
                // User exited fullscreen
                sessionStorage.removeItem('wasFullscreen');
            }
        });
        
        // Restore fullscreen on page load
        document.addEventListener('DOMContentLoaded', function() {
            restoreFullscreenState();
        });
        
        // Also try to restore immediately in case DOM is already loaded
        if (document.readyState === 'complete' || document.readyState === 'interactive') {
            restoreFullscreenState();
        }
    </script>
    '''
    
    # Replace the existing keyboard navigation script
    script_replaced = False
    for script in script_tags:
        if script.string and 'addEventListener' in script.string and 'keydown' in script.string:
            # Replace the entire script tag
            new_script = soup.new_tag('script')
            new_script.string = enhanced_script.replace('<script>', '').replace('</script>', '')
            script.replace_with(new_script)
            script_replaced = True
            break
    
    # If no script was replaced, add it before closing body
    if not script_replaced:
        body = soup.find('body')
        if body:
            body.append(BeautifulSoup(enhanced_script, 'html.parser'))
    
    return str(soup)

def update_all_slides():
    """Update all slides in the presentation"""
    slides_dir = Path("vmg_presentation/slides")
    slide_files = sorted(slides_dir.glob("*.html"))
    
    print("🔄 Adding fullscreen persistence to all slides...")
    print("="*50)
    
    for slide_file in slide_files:
        print(f"  Updating: {slide_file.name}")
        
        updated_html = update_slide_with_fullscreen_persistence(slide_file)
        
        # Write back the updated file
        with open(slide_file, 'w', encoding='utf-8') as f:
            f.write(updated_html)
    
    print("="*50)
    print("✨ All slides updated with fullscreen persistence!")
    print("\nHow it works:")
    print("  • Fullscreen state is saved when navigating")
    print("  • State is restored automatically on new page")
    print("  • Works with both click and keyboard navigation")
    print("  • Clears state when user exits fullscreen with Esc")

def update_index_page():
    """Update index page to clear fullscreen state"""
    index_file = Path("vmg_presentation/index.html")
    
    with open(index_file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Add script to clear fullscreen state on index page
    clear_script = '''
    <script>
        // Clear fullscreen state when returning to index
        sessionStorage.removeItem('wasFullscreen');
    </script>
    '''
    
    body = soup.find('body')
    if body:
        body.append(BeautifulSoup(clear_script, 'html.parser'))
    
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print("✅ Index page updated to clear fullscreen state")

if __name__ == "__main__":
    update_all_slides()
    update_index_page()
    print("\n📝 Note: Refresh your browser to see the changes!")
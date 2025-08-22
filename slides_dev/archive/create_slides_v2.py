#!/usr/bin/env python3
"""
Advanced slide generator that creates sophisticated HTML slides from markdown content.
Generates professional-quality slides matching the VMG presentation style.
"""

import re
import os
from pathlib import Path
import argparse

class AdvancedSlideGenerator:
    def __init__(self):
        self.base_styles = """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: #f5f5f5;
            overflow: hidden;
            margin: 0;
            padding: 0;
        }

        .presentation-container {
            width: 100vw;
            height: 100vh;
            display: flex;
            flex-direction: column;
            position: relative;
        }

        .slide {
            display: none;
            width: 100vw;
            height: 100vh;
            padding: 3vh 4vw;
            background: white;
            position: relative;
            overflow-y: auto;
            overflow-x: hidden;
        }

        .slide.active {
            display: flex;
            flex-direction: column;
        }
        
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes slideIn {
            from { transform: translateX(-20px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        h1 {
            font-size: 2.8vw;
            margin-bottom: 1.5vh;
            color: #1a1a1a;
            text-align: center;
            font-weight: 300;
            letter-spacing: -0.5px;
            animation: fadeInDown 0.8s ease-out;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            font-size: 1.2vw;
            margin-bottom: 2.5vh;
            font-weight: 400;
            animation: fadeInDown 0.8s ease-out 0.2s both;
        }

        .footer-note {
            position: absolute;
            bottom: 2vh;
            right: 4vw;
            font-size: 0.8vw;
            color: #999;
            font-style: italic;
        }
        """

    def parse_markdown(self, content):
        """Parse markdown content into structured data."""
        lines = content.strip().split('\n')
        slides = []
        current_slide = None
        
        for line in lines:
            # Check for slide header (## Slide X:)
            if line.startswith('## Slide'):
                if current_slide:
                    slides.append(current_slide)
                title = line.replace('## Slide ', '').replace(':', '').strip()
                # Remove "Slide X:" prefix
                title = re.sub(r'^\d+:\s*', '', title)
                current_slide = {
                    'title': title,
                    'subtitle': None,
                    'sections': [],
                    'footer': None,
                    'type': 'generic'
                }
            elif current_slide:
                if line.startswith('### '):
                    # Subtitle or section header
                    if not current_slide['subtitle'] and not current_slide['sections']:
                        current_slide['subtitle'] = line[4:].strip()
                    else:
                        current_slide['sections'].append({
                            'title': line[4:].strip(),
                            'content': [],
                            'type': 'section'
                        })
                elif line.startswith('#### '):
                    # Subsection
                    if current_slide['sections']:
                        current_slide['sections'][-1]['content'].append({
                            'type': 'subsection',
                            'title': line[5:].strip(),
                            'items': []
                        })
                elif line.startswith('- '):
                    # List item
                    if current_slide['sections'] and current_slide['sections'][-1]['content']:
                        last_content = current_slide['sections'][-1]['content'][-1]
                        if last_content['type'] == 'subsection':
                            last_content['items'].append(line[2:].strip())
                elif line.startswith('*') and line.endswith('*') and not line.startswith('**'):
                    # Footer note
                    current_slide['footer'] = line.strip('*').strip()
                elif line.strip() and current_slide['sections']:
                    # Regular paragraph
                    current_slide['sections'][-1]['content'].append({
                        'type': 'paragraph',
                        'text': line.strip()
                    })
        
        if current_slide:
            slides.append(current_slide)
        
        return slides

    def detect_slide_type(self, slide):
        """Detect the type of slide based on content."""
        title = slide['title'].lower()
        
        # Check for competitive/competitor content
        if 'compet' in title or 'threat' in title:
            # Check if it's strategy or landscape
            if 'strategy' in title or 'wins' in title or 'differentiation' in title:
                return 'competitive_strategy'
            else:
                return 'competitive_landscape'
        elif 'timeline' in title or 'roadmap' in title:
            return 'timeline'
        elif 'metric' in title or 'kpi' in title:
            return 'metrics'
        elif any(word in title for word in ['table', 'comparison', 'matrix']):
            return 'table'
        else:
            return 'generic'

    def generate_competitive_landscape(self, slide, slide_num):
        """Generate a competitive landscape slide with threat cards."""
        threat_levels = {
            'high threat': ('threat-high', '#dc3545'),
            'medium threat': ('threat-medium', '#f39c12'),
            'low threat': ('threat-low', '#28a745'),
            'emerging threat': ('threat-emerging', '#e67e22'),
            'indirect threat': ('threat-indirect', '#95a5a6')
        }
        
        additional_styles = """
        .competitor-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.5vw;
            margin-bottom: 2vh;
            animation: fadeInUp 0.8s ease-out 0.4s both;
        }

        .competitor-card {
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            padding: 1.5vh 1.2vw;
            position: relative;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }

        .competitor-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        }

        .threat-level {
            position: absolute;
            top: 1vh;
            right: 1vw;
            padding: 0.3vh 0.6vw;
            border-radius: 4px;
            font-size: 0.7vw;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .threat-high {
            background: rgba(220, 53, 69, 0.1);
            color: #dc3545;
            border: 1px solid rgba(220, 53, 69, 0.3);
        }

        .threat-medium {
            background: rgba(255, 193, 7, 0.1);
            color: #f39c12;
            border: 1px solid rgba(255, 193, 7, 0.3);
        }

        .threat-low {
            background: rgba(40, 167, 69, 0.1);
            color: #28a745;
            border: 1px solid rgba(40, 167, 69, 0.3);
        }

        .threat-emerging {
            background: rgba(243, 156, 18, 0.1);
            color: #e67e22;
            border: 1px solid rgba(243, 156, 18, 0.3);
        }

        .threat-indirect {
            background: rgba(149, 165, 166, 0.1);
            color: #95a5a6;
            border: 1px solid rgba(149, 165, 166, 0.3);
        }

        .competitor-name {
            font-size: 1.2vw;
            font-weight: 600;
            color: #0076a8;
            margin-bottom: 0.8vh;
            margin-top: 0.5vh;
        }

        .competitor-info {
            font-size: 0.9vw;
            line-height: 1.6;
            color: #555;
            margin-bottom: 0.8vh;
        }

        .competitor-info strong {
            color: #333;
            font-weight: 600;
        }

        .strength {
            color: #28a745;
            font-weight: 500;
            font-size: 0.85vw;
            margin: 0.3vh 0;
            padding-left: 0.5vw;
        }

        .weakness {
            color: #dc3545;
            font-weight: 500;
            font-size: 0.85vw;
            margin: 0.3vh 0;
            padding-left: 0.5vw;
        }

        .competitive-moat {
            background: linear-gradient(135deg, rgba(0, 167, 79, 0.05) 0%, rgba(0, 118, 168, 0.05) 100%);
            border: 2px solid #00a74f;
            border-radius: 12px;
            padding: 2vh 2vw;
            margin-top: 2vh;
            animation: fadeInUp 0.8s ease-out 0.6s both;
        }

        .moat-title {
            color: #00a74f;
            font-weight: 600;
            font-size: 1.3vw;
            margin-bottom: 1vh;
        }

        .moat-content {
            font-size: 1vw;
            color: #333;
            line-height: 1.6;
        }

        .moat-content strong {
            color: #0076a8;
            font-weight: 600;
        }
        """
        
        content_html = f'<div class="subtitle">{slide["subtitle"]}</div>' if slide['subtitle'] else ''
        content_html += '<div class="competitor-grid">'
        
        for section in slide['sections']:
            # Determine threat level
            threat_class = 'threat-medium'
            threat_text = 'Medium Threat'
            for level, (css_class, color) in threat_levels.items():
                if level in section['title'].lower():
                    threat_class = css_class
                    threat_text = section['title'].split(':')[0].strip()
                    break
            
            # Extract competitor name
            competitor_name = section['title'].split(':')[-1].strip()
            
            content_html += f'''
            <div class="competitor-card">
                <span class="threat-level {threat_class}">{threat_text}</span>
                <div class="competitor-name">{competitor_name}</div>
                <div class="competitor-info">
            '''
            
            for content_item in section['content']:
                if content_item['type'] == 'subsection':
                    if 'strengths' in content_item['title'].lower():
                        for item in content_item['items']:
                            content_html += f'<div class="strength">✓ {item}</div>'
                    elif 'weaknesses' in content_item['title'].lower():
                        for item in content_item['items']:
                            content_html += f'<div class="weakness">✗ {item}</div>'
                    else:
                        for item in content_item['items']:
                            key_val = item.split(':', 1)
                            if len(key_val) == 2:
                                content_html += f'<strong>{key_val[0]}:</strong> {key_val[1]}<br>'
                            else:
                                content_html += f'{item}<br>'
            
            content_html += '''
                </div>
            </div>
            '''
        
        content_html += '</div>'
        
        # Add competitive moat if present
        for section in slide['sections']:
            if 'defensible' in section['title'].lower() or 'moat' in section['title'].lower():
                content_html += f'''
                <div class="competitive-moat">
                    <div class="moat-title">{section['title']}</div>
                    <div class="moat-content">
                '''
                for content_item in section['content']:
                    if content_item['type'] == 'paragraph':
                        # Bold key phrases
                        text = content_item['text']
                        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
                        content_html += text
                content_html += '''
                    </div>
                </div>
                '''
        
        return content_html, additional_styles

    def generate_competitive_strategy(self, slide, slide_num):
        """Generate a competitive strategy slide."""
        additional_styles = """
        .content-wrapper {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2vw;
            flex: 1;
            animation: fadeInUp 0.8s ease-out 0.3s both;
        }

        .section {
            display: flex;
            flex-direction: column;
            gap: 1.5vh;
        }

        .section-title {
            color: #0076a8;
            font-size: 1.4vw;
            font-weight: 600;
            margin-bottom: 1vh;
            padding-bottom: 0.8vh;
            border-bottom: 2px solid #e0e0e0;
        }

        .strategy-card {
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 1.2vh 1.2vw;
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
        }

        .strategy-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.12);
        }

        .move-counter {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1vw;
            margin-bottom: 0.8vh;
        }

        .their-move, .our-counter {
            padding: 0.8vh 0.8vw;
            border-radius: 6px;
            font-size: 0.9vw;
            line-height: 1.5;
        }

        .their-move {
            background: rgba(220, 53, 69, 0.08);
            border-left: 3px solid #dc3545;
        }

        .our-counter {
            background: rgba(40, 167, 69, 0.08);
            border-left: 3px solid #28a745;
        }

        .move-label, .counter-label {
            font-weight: 600;
            font-size: 0.75vw;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.3vh;
        }

        .move-label {
            color: #dc3545;
        }

        .counter-label {
            color: #28a745;
        }

        .advantage-card {
            background: linear-gradient(135deg, rgba(0, 118, 168, 0.05) 0%, rgba(0, 167, 79, 0.05) 100%);
            border: 2px solid #0076a8;
            border-radius: 10px;
            padding: 1.5vh 1.5vw;
            margin-bottom: 1.2vh;
        }

        .competitor-type {
            color: #0076a8;
            font-weight: 600;
            font-size: 1.1vw;
            margin-bottom: 0.5vh;
        }

        .advantage-text {
            font-size: 0.95vw;
            color: #333;
            line-height: 1.6;
        }

        .advantage-text strong {
            color: #00a74f;
            font-weight: 600;
        }

        .strategy-title {
            font-size: 1vw;
            font-weight: 600;
            color: #1a1a1a;
            margin-bottom: 0.8vh;
        }

        .timeline-section {
            grid-column: 1 / -1;
            margin-top: 2vh;
            animation: fadeInUp 0.8s ease-out 0.5s both;
        }

        .timeline-header {
            color: #00a74f;
            font-size: 1.3vw;
            font-weight: 600;
            margin-bottom: 1.5vh;
            text-align: center;
        }

        .timeline-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1vw;
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            padding: 1.5vh 1.5vw;
        }

        .timeline-phase {
            padding: 1vh 0.8vw;
            border-right: 1px solid #e0e0e0;
            text-align: center;
        }

        .timeline-phase:last-child {
            border-right: none;
        }

        .phase-period {
            background: linear-gradient(135deg, #0076a8, #00a74f);
            color: white;
            padding: 0.5vh 0.8vw;
            border-radius: 6px;
            font-size: 0.9vw;
            font-weight: 600;
            margin-bottom: 0.8vh;
        }

        .phase-content {
            font-size: 0.85vw;
            color: #555;
            line-height: 1.5;
        }
        """
        
        content_html = '<div class="content-wrapper">'
        
        # Split sections into two columns
        moves_section = None
        advantages_section = None
        timeline_section = None
        
        for section in slide['sections']:
            if 'moves' in section['title'].lower() or 'counter' in section['title'].lower():
                moves_section = section
            elif 'advantage' in section['title'].lower():
                advantages_section = section
            elif 'timeline' in section['title'].lower() or 'roadmap' in section['title'].lower():
                timeline_section = section
        
        # Generate moves column
        if moves_section:
            content_html += f'''
            <div class="section">
                <div class="section-title">{moves_section['title']}</div>
            '''
            
            for content_item in moves_section['content']:
                if content_item['type'] == 'subsection':
                    strategy_title = content_item['title']
                    items = content_item['items']
                    
                    their_move = ''
                    our_counter = ''
                    
                    for item in items:
                        if 'their move:' in item.lower():
                            their_move = item.split(':', 1)[1].strip()
                        elif 'our counter:' in item.lower():
                            our_counter = item.split(':', 1)[1].strip()
                    
                    content_html += f'''
                    <div class="strategy-card">
                        <div class="strategy-title">{strategy_title}</div>
                        <div class="move-counter">
                            <div class="their-move">
                                <div class="move-label">Their Move</div>
                                {their_move}
                            </div>
                            <div class="our-counter">
                                <div class="counter-label">Our Counter</div>
                                {our_counter}
                            </div>
                        </div>
                    </div>
                    '''
            
            content_html += '</div>'
        
        # Generate advantages column
        if advantages_section:
            content_html += f'''
            <div class="section">
                <div class="section-title">{advantages_section['title']}</div>
            '''
            
            for content_item in advantages_section['content']:
                if content_item['type'] == 'subsection':
                    competitor = content_item['title']
                    description = ' '.join(content_item['items']) if content_item['items'] else ''
                elif content_item['type'] == 'paragraph':
                    description = content_item['text']
                    # Extract competitor type from bold text
                    match = re.search(r'vs\.\s*(.*?)(?:\n|$)', content_item['text'])
                    if match:
                        competitor = match.group(1)
                        description = re.sub(r'vs\.\s*.*?(?:\n|$)', '', description).strip()
                    else:
                        continue
                else:
                    continue
                
                # Bold important phrases
                description = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', description)
                
                content_html += f'''
                <div class="advantage-card">
                    <div class="competitor-type">{competitor}</div>
                    <div class="advantage-text">{description}</div>
                </div>
                '''
            
            content_html += '</div>'
        
        content_html += '</div>'  # Close content-wrapper
        
        # Add timeline if present
        if timeline_section:
            content_html += f'''
            <div class="timeline-section">
                <div class="timeline-header">{timeline_section['title']}</div>
                <div class="timeline-grid">
            '''
            
            # Parse timeline from table or list
            for content_item in timeline_section['content']:
                if content_item['type'] == 'paragraph':
                    # Parse table row
                    parts = content_item['text'].split('|')
                    if len(parts) >= 2:
                        period = parts[0].strip()
                        content = parts[1].strip() if len(parts) > 1 else ''
                        
                        content_html += f'''
                        <div class="timeline-phase">
                            <div class="phase-period">{period}</div>
                            <div class="phase-content">{content}</div>
                        </div>
                        '''
            
            content_html += '''
                </div>
            </div>
            '''
        
        return content_html, additional_styles

    def generate_slide_html(self, slide, slide_num):
        """Generate HTML for a single slide."""
        slide['type'] = self.detect_slide_type(slide)
        
        # Generate type-specific content
        if slide['type'] == 'competitive_landscape':
            content_html, additional_styles = self.generate_competitive_landscape(slide, slide_num)
        elif slide['type'] == 'competitive_strategy':
            content_html, additional_styles = self.generate_competitive_strategy(slide, slide_num)
        else:
            # Generic slide generation
            content_html = ''
            additional_styles = ''
            
            if slide['subtitle']:
                content_html += f'<div class="subtitle">{slide["subtitle"]}</div>'
            
            content_html += '<div class="content">'
            for section in slide['sections']:
                content_html += f'<h3>{section["title"]}</h3>'
                for content_item in section['content']:
                    if content_item['type'] == 'subsection':
                        content_html += f'<h4>{content_item["title"]}</h4><ul>'
                        for item in content_item['items']:
                            content_html += f'<li>{item}</li>'
                        content_html += '</ul>'
                    elif content_item['type'] == 'paragraph':
                        content_html += f'<p>{content_item["text"]}</p>'
            content_html += '</div>'
        
        # Build complete HTML
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{slide['title']}</title>
    <style>
        {self.base_styles}
        {additional_styles}
    </style>
</head>
<body>
    <div class="presentation-container">
        <div class="slide active" id="slide{slide_num}">
            <h1>{slide['title']}</h1>
            {content_html}
            {'<div class="footer-note">' + slide["footer"] + '</div>' if slide["footer"] else ''}
        </div>
    </div>
</body>
</html>'''
        
        return html

    def generate_slides(self, markdown_file, output_dir='slides_dev'):
        """Generate HTML slides from markdown file."""
        # Read markdown content
        with open(markdown_file, 'r') as f:
            content = f.read()
        
        # Parse slides
        slides = self.parse_markdown(content)
        
        # Create output directory
        Path(output_dir).mkdir(exist_ok=True)
        
        # Generate HTML for each slide
        generated_files = []
        for i, slide in enumerate(slides, 1):
            # Generate filename
            title_slug = re.sub(r'[^\w\s-]', '', slide['title'].lower())
            title_slug = re.sub(r'[-\s]+', '_', title_slug)
            filename = f"slide_{i:02d}_{title_slug[:50]}.html"
            filepath = os.path.join(output_dir, filename)
            
            # Generate HTML
            html = self.generate_slide_html(slide, i)
            
            # Write file
            with open(filepath, 'w') as f:
                f.write(html)
            
            generated_files.append(filepath)
            print(f"Generated: {filepath}")
        
        return generated_files

def main():
    parser = argparse.ArgumentParser(description='Generate sophisticated HTML slides from markdown')
    parser.add_argument('markdown_file', help='Path to markdown file')
    parser.add_argument('--output-dir', default='slides_dev', help='Output directory for slides')
    
    args = parser.parse_args()
    
    generator = AdvancedSlideGenerator()
    files = generator.generate_slides(args.markdown_file, args.output_dir)
    
    print(f"\nGenerated {len(files)} slides successfully!")
    print("\nTo view slides, open them in a browser:")
    for f in files:
        print(f"  open {f}")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Create styled HTML slides from markdown content
Automatically detects slide type and applies appropriate template
Follows the style guide in README_STYLE.md
"""

import sys
import re
import json
from pathlib import Path
from datetime import datetime
import markdown
from typing import List, Dict, Tuple

class SlideGenerator:
    def __init__(self):
        self.slides_created = []
        self.next_slide_num = self.get_next_slide_number()
        
    def get_next_slide_number(self):
        """Find the highest slide number in slides_complete and slides_dev"""
        max_num = 13  # Start after existing slides
        
        for directory in ['../slides_complete', '.']:
            dir_path = Path(directory)
            if dir_path.exists():
                for file in dir_path.glob('slide_*.html'):
                    match = re.match(r'slide_(\d+)_', file.name)
                    if match:
                        num = int(match.group(1))
                        max_num = max(max_num, num)
        
        return max_num + 1
    
    def parse_markdown_file(self, filepath: str) -> List[Dict]:
        """Parse markdown file into individual slides"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by slide markers (---, ===, or ## Slide:)
        slide_pattern = r'(?:^---+$|^===+$|^## Slide:)'
        parts = re.split(slide_pattern, content, flags=re.MULTILINE)
        
        slides = []
        for part in parts:
            if part.strip():
                slide_data = self.parse_slide_content(part.strip())
                if slide_data:
                    slides.append(slide_data)
        
        return slides
    
    def parse_slide_content(self, content: str) -> Dict:
        """Parse individual slide content"""
        lines = content.split('\n')
        slide = {
            'title': '',
            'subtitle': '',
            'content': [],
            'type': None,
            'raw_content': content
        }
        
        # Extract title (first # or ## that's not "## Slide:")
        for i, line in enumerate(lines):
            if line.startswith('# ') and not line.startswith('## Slide:'):
                slide['title'] = line[2:].strip()
                lines[i] = ''
            elif line.startswith('## ') and not line.startswith('## Slide:'):
                if not slide['title']:
                    slide['title'] = line[3:].strip()
                    lines[i] = ''
            elif line.startswith('### Subtitle:') or line.startswith('**Subtitle:**'):
                slide['subtitle'] = line.replace('### Subtitle:', '').replace('**Subtitle:**', '').strip()
                lines[i] = ''
        
        # Rejoin content
        remaining_content = '\n'.join(lines).strip()
        slide['content'] = remaining_content
        
        # Detect slide type
        slide['type'] = self.detect_slide_type(remaining_content)
        
        return slide if slide['title'] else None
    
    def detect_slide_type(self, content: str) -> str:
        """Detect which template to use based on content"""
        
        # Check for table (markdown table syntax)
        if '|' in content and '---|' in content:
            return 'table'
        
        # Check for data that suggests a chart
        if any(word in content.lower() for word in ['chart:', 'graph:', 'plot:', 'data:', 'trend', 'growth rate', 'percentage']):
            if 'input:' in content.lower() or 'adjustable:' in content.lower():
                return 'interactive'
            return 'chart'
        
        # Check for timeline indicators
        if any(word in content.lower() for word in ['phase', 'quarter', 'timeline', 'roadmap', 'milestone', 'q1', 'q2', 'q3', 'q4']):
            return 'timeline'
        
        # Check for metrics/KPIs
        if any(word in content.lower() for word in ['kpi', 'metric', 'roi', 'npv', 'irr', 'payback', '$', '%']) and len(content.split('\n')) < 15:
            return 'metrics'
        
        # Default to text/content slide
        return 'text'
    
    def generate_slide_html(self, slide_data: Dict, slide_num: int) -> Tuple[str, str]:
        """Generate HTML for a slide based on its type"""
        
        template_generators = {
            'table': self.generate_table_slide,
            'chart': self.generate_chart_slide,
            'interactive': self.generate_interactive_slide,
            'timeline': self.generate_timeline_slide,
            'metrics': self.generate_metrics_slide,
            'text': self.generate_text_slide
        }
        
        generator = template_generators.get(slide_data['type'], self.generate_text_slide)
        html_content = generator(slide_data, slide_num)
        
        # Generate filename
        title_slug = re.sub(r'[^a-z0-9]+', '_', slide_data['title'].lower())
        title_slug = title_slug[:50].rstrip('_')  # Limit length
        filename = f"slide_{slide_num:02d}_{title_slug}.html"
        
        return html_content, filename
    
    def get_base_styles(self) -> str:
        """Return base CSS styles common to all slides"""
        return """
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

        h1 {
            font-size: 3vw;
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
            font-size: 1.3vw;
            margin-bottom: 3vh;
            font-weight: 400;
            animation: fadeInDown 0.8s ease-out 0.2s both;
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
        """
    
    def generate_table_slide(self, slide_data: Dict, slide_num: int) -> str:
        """Generate HTML for a table slide (Template 2)"""
        base_styles = self.get_base_styles()
        
        # Parse markdown table
        md = markdown.Markdown(extensions=['tables'])
        table_html = md.convert(slide_data['content'])
        
        # Add our custom classes to the table
        table_html = table_html.replace('<table>', '<table class="data-table">')
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{slide_data['title']}</title>
    <style>
        {base_styles}
        
        .table-container {{
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            animation: fadeInUp 0.8s ease-out 0.4s both;
        }}
        
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 16px;
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            overflow: hidden;
        }}
        
        .data-table th {{
            background: linear-gradient(135deg, #0076a8 0%, #00a74f 100%);
            color: white;
            padding: 12px 15px;
            text-align: left;
            font-weight: 600;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .data-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e0e0e0;
            transition: all 0.2s ease;
        }}
        
        .data-table tr:nth-child(even) {{
            background: #f8f9fa;
        }}
        
        .data-table tbody tr:hover {{
            background: linear-gradient(135deg, #f0f7ff 0%, #f5fff8 100%);
            transform: scale(1.01);
        }}
    </style>
</head>
<body>
    <div class="presentation-container">
        <div class="slide active" id="slide{slide_num}">
            <h1>{slide_data['title']}</h1>
            {f'<div class="subtitle">{slide_data["subtitle"]}</div>' if slide_data['subtitle'] else ''}
            
            <div class="table-container">
                {table_html}
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def generate_chart_slide(self, slide_data: Dict, slide_num: int) -> str:
        """Generate HTML for a chart slide (Template 1)"""
        base_styles = self.get_base_styles()
        
        # Parse any data from the markdown
        # This is a simplified version - you might need to parse specific data formats
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{slide_data['title']}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        {base_styles}
        
        .chart-container {{
            flex: 1;
            display: flex;
            gap: 2vw;
            animation: fadeInUp 0.8s ease-out 0.4s both;
        }}
        
        .chart-area {{
            flex: 1.5;
            background: white;
            border-radius: 12px;
            padding: 2vh;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        .chart-legend {{
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 1vh;
        }}
        
        .legend-item {{
            background: white;
            border-radius: 8px;
            padding: 1.5vh 1.5vw;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }}
        
        .legend-item:hover {{
            transform: translateX(5px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
    </style>
</head>
<body>
    <div class="presentation-container">
        <div class="slide active" id="slide{slide_num}">
            <h1>{slide_data['title']}</h1>
            {f'<div class="subtitle">{slide_data["subtitle"]}</div>' if slide_data['subtitle'] else ''}
            
            <div class="chart-container">
                <div class="chart-area" id="chartDiv"></div>
                <div class="chart-legend">
                    <!-- Legend items would be generated based on data -->
                    <div class="legend-item">Data visualization will be configured based on provided data</div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Chart initialization would go here based on parsed data
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('Chart slide ready for data visualization');
            // Plotly.newPlot('chartDiv', data, layout, config);
        }});
    </script>
</body>
</html>"""
    
    def generate_text_slide(self, slide_data: Dict, slide_num: int) -> str:
        """Generate HTML for a text/content slide (Template 6)"""
        base_styles = self.get_base_styles()
        
        # Convert markdown content to HTML
        md = markdown.Markdown(extensions=['extra'])
        content_html = md.convert(slide_data['content'])
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{slide_data['title']}</title>
    <style>
        {base_styles}
        
        .content-container {{
            flex: 1;
            animation: fadeInUp 0.8s ease-out 0.4s both;
        }}
        
        .content-container h2 {{
            color: #0076a8;
            font-size: 1.8vw;
            margin-top: 2vh;
            margin-bottom: 1vh;
            font-weight: 600;
        }}
        
        .content-container h3 {{
            color: #333;
            font-size: 1.4vw;
            margin-top: 1.5vh;
            margin-bottom: 0.8vh;
            font-weight: 600;
        }}
        
        .content-container p {{
            color: #666;
            font-size: 1.1vw;
            line-height: 1.6;
            margin-bottom: 1vh;
        }}
        
        .content-container ul, .content-container ol {{
            margin-left: 2vw;
            margin-bottom: 1.5vh;
        }}
        
        .content-container li {{
            color: #555;
            font-size: 1.1vw;
            line-height: 1.8;
            margin-bottom: 0.5vh;
        }}
        
        .content-container strong {{
            color: #333;
            font-weight: 600;
        }}
        
        .content-container blockquote {{
            border-left: 4px solid #0076a8;
            padding-left: 1.5vw;
            margin: 1.5vh 0;
            color: #555;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="presentation-container">
        <div class="slide active" id="slide{slide_num}">
            <h1>{slide_data['title']}</h1>
            {f'<div class="subtitle">{slide_data["subtitle"]}</div>' if slide_data['subtitle'] else ''}
            
            <div class="content-container">
                {content_html}
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def generate_interactive_slide(self, slide_data: Dict, slide_num: int) -> str:
        """Generate HTML for an interactive slide (Template 3)"""
        # Simplified version - would need more logic for actual interactivity
        return self.generate_chart_slide(slide_data, slide_num)
    
    def generate_timeline_slide(self, slide_data: Dict, slide_num: int) -> str:
        """Generate HTML for a timeline slide (Template 4)"""
        # Simplified version - would need timeline-specific styling
        return self.generate_text_slide(slide_data, slide_num)
    
    def generate_metrics_slide(self, slide_data: Dict, slide_num: int) -> str:
        """Generate HTML for a metrics dashboard slide (Template 5)"""
        base_styles = self.get_base_styles()
        
        # Parse metrics from content (looking for key: value patterns)
        lines = slide_data['content'].split('\n')
        metrics = []
        for line in lines:
            if ':' in line:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    metrics.append({
                        'label': parts[0].strip().strip('-').strip('*').strip(),
                        'value': parts[1].strip()
                    })
        
        # Generate metric cards HTML
        metrics_html = ''
        for metric in metrics:
            metrics_html += f"""
                <div class="metric-card">
                    <div class="metric-label">{metric['label']}</div>
                    <div class="metric-value">{metric['value']}</div>
                </div>
            """
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{slide_data['title']}</title>
    <style>
        {base_styles}
        
        .metrics-container {{
            flex: 1;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2vh 2vw;
            animation: fadeInUp 0.8s ease-out 0.4s both;
        }}
        
        .metric-card {{
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            padding: 2vh 1.5vw;
            text-align: center;
            transition: all 0.3s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            border-color: #0076a8;
        }}
        
        .metric-label {{
            color: #666;
            font-size: 1vw;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 1vh;
        }}
        
        .metric-value {{
            color: #0076a8;
            font-size: 2.5vw;
            font-weight: 700;
            line-height: 1.2;
        }}
    </style>
</head>
<body>
    <div class="presentation-container">
        <div class="slide active" id="slide{slide_num}">
            <h1>{slide_data['title']}</h1>
            {f'<div class="subtitle">{slide_data["subtitle"]}</div>' if slide_data['subtitle'] else ''}
            
            <div class="metrics-container">
                {metrics_html if metrics_html else '<div class="metric-card"><div class="metric-label">Metrics</div><div class="metric-value">Will be parsed from content</div></div>'}
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def process_markdown_file(self, filepath: str):
        """Main method to process a markdown file and generate slides"""
        print(f"\n📄 Processing markdown file: {filepath}")
        print("="*50)
        
        # Parse the markdown file
        slides = self.parse_markdown_file(filepath)
        
        if not slides:
            print("❌ No slides found in the markdown file")
            return
        
        print(f"Found {len(slides)} slide(s) to generate\n")
        
        # Generate HTML for each slide
        for slide_data in slides:
            slide_num = self.next_slide_num
            html_content, filename = self.generate_slide_html(slide_data, slide_num)
            
            # Save the file
            output_path = Path(filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Record what was created
            self.slides_created.append({
                'number': slide_num,
                'filename': filename,
                'title': slide_data['title'],
                'type': slide_data['type']
            })
            
            print(f"✅ Created: {filename}")
            print(f"   Title: {slide_data['title']}")
            print(f"   Type: {slide_data['type'].upper()} template")
            print()
            
            self.next_slide_num += 1
        
        # Summary
        print("="*50)
        print(f"✨ Successfully created {len(self.slides_created)} slide(s)")
        print("\nSlides created:")
        for slide in self.slides_created:
            print(f"  {slide['number']:02d}. {slide['title']} ({slide['type']})")
        
        print("\nNext steps:")
        print("1. Review the generated slides in slides_dev/")
        print("2. Move approved slides to slides_complete/")
        print("3. Update slides.db with new slide information")
        print("4. Run build_linked_presentation.py to rebuild")

def main():
    if len(sys.argv) < 2:
        print("Usage: python create_slides.py <markdown_file>")
        print("\nExample markdown format:")
        print("---")
        print("## Slide: Title Here")
        print("### Subtitle: Optional subtitle")
        print("Content goes here...")
        print("---")
        sys.exit(1)
    
    md_file = sys.argv[1]
    
    if not Path(md_file).exists():
        print(f"Error: File '{md_file}' not found")
        sys.exit(1)
    
    generator = SlideGenerator()
    generator.process_markdown_file(md_file)

if __name__ == "__main__":
    main()
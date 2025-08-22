# Slide Style Guide for VMG Presentation

## Purpose
This guide ensures consistency when creating new slides that match the style of the existing VMG presentation slides (specifically slides 5-13 from slides_complete/).

## Core Style Requirements

### Color Palette
- **Primary Gradient**: `linear-gradient(135deg, #0076a8 0%, #00a74f 100%)`
- **Purple Gradient**: `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`
- **Accent Colors**:
  - Primary Blue: `#0076a8`
  - Primary Green: `#00a74f`
  - Purple: `#667eea`, `#764ba2`
  - Success Green: `#2e7d32`, `#28a745`
  - Error Red: `#d32f2f`, `#dc3545`
  - Warning Orange: `#ff6f00`, `#f39c12`, `#e67e22`
  - Text Dark: `#1a1a1a`, `#333`, `#495057`
  - Text Light: `#666`, `#6c757d`
  - Background: `#f5f5f5`, `#f8f9fa`

### Typography
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;

/* Heading Sizes */
h1: 3vw
subtitle: 1.2vw - 1.3vw
body text: 16px or 1.1vw
small text: 0.9vw

/* Font Weights */
h1: 300 (light)
subtitle: 400 (normal)
emphasis: 600 (semi-bold)
strong: 700 (bold)
```

### Layout Structure
```css
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
```

### Animations
```css
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

/* Standard timing */
h1: animation: fadeInDown 0.8s ease-out;
subtitle: animation: fadeInDown 0.8s ease-out 0.2s both;
content: animation: fadeInUp 0.8s ease-out 0.4s both;
```

### Common Components

#### Panel/Card Style
```css
.panel {
    background: white;
    border: 2px solid #e0e0e0;
    padding: 20px;
    border-radius: 12px;
    transition: all 0.3s ease;
}

.panel:hover {
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}
```

#### Button Style
```css
.button {
    padding: 6px 15px;
    background: linear-gradient(135deg, #0076a8 0%, #00a74f 100%);
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 118, 168, 0.3);
}
```

#### Table Style
```css
.table {
    width: 100%;
    border-collapse: collapse;
    font-size: 16px;
    background: white;
    border: 2px solid #e0e0e0;
    border-radius: 12px;
    overflow: hidden;
}

.table th {
    background: linear-gradient(135deg, #0076a8 0%, #00a74f 100%);
    color: white;
    padding: 12px 15px;
    text-align: left;
    font-weight: 600;
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.table td {
    padding: 12px 15px;
    border-bottom: 1px solid #e0e0e0;
    transition: all 0.2s ease;
}

.table tbody tr:hover {
    background: linear-gradient(135deg, #f0f7ff 0%, #f5fff8 100%);
    transform: scale(1.01);
}
```

## Slide Type Templates

### 1. Chart Slide (Reference: slide_05_strategic_initiative_prioritization.html)
- Uses Plotly.js for interactive charts
- Split layout: chart on left (flex: 1.5), list on right (flex: 1)
- Chart container with white background and border
- Initiative items with hover effects and priority highlighting

### 2. Table Slide (Reference: slide_09_customer_growth_assumptions.html)
- Full-width table with gradient header
- Hover effects on rows
- Color-coded values (growth rates)
- Clean borders and spacing

### 3. Interactive Slide (Reference: slide_10_return_on_investment_analysis.html)
- Input controls with gradient buttons
- Split layout: metrics panel left, chart right
- Real-time updates via JavaScript
- Chart.js for bar/line combination charts

### 4. Timeline Slide (Reference: slide_11_development_timeline.html)
- Horizontal timeline with milestone markers
- Phase blocks with gradient backgrounds
- Animated progress indicators

### 5. Metrics Dashboard (Reference: slide_12_key_investment_metrics.html)
- Grid layout for metric cards
- Large value displays with labels
- Color-coded positive/negative values
- Icons or visual indicators

### 6. Text/Content Slide (Reference: slide_13_risk_assessment_mitigation_strategy.html)
- Structured sections with headers
- Risk level indicators with colors
- Mitigation strategy lists
- Clean typography hierarchy

## Instructions for Creating New Slides

### When the user provides content:

1. **Identify the slide type** from the templates above
2. **Copy the exact structure** from the reference slide in slides_complete/
3. **Maintain all CSS classes and styles** exactly as they appear
4. **Use the same animation timings and effects**
5. **Apply the color palette consistently**
6. **Keep responsive units** (vw, vh) for sizing
7. **Include hover effects and transitions** where appropriate

### File Naming Convention
```
slide_[number]_[descriptive_name_with_underscores].html
```
Example: `slide_14_market_opportunity_analysis.html`

### Required HTML Structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Slide Title]</title>
    <!-- Include Chart.js or Plotly if needed -->
    <style>
        /* Include all base styles from template */
        /* Add slide-specific styles */
    </style>
</head>
<body>
    <div class="presentation-container">
        <div class="slide active" id="slide[number]">
            <h1>[Title]</h1>
            <div class="subtitle">[Subtitle]</div>
            <!-- Content following template structure -->
        </div>
    </div>
    <!-- Include JavaScript if needed -->
</body>
</html>
```

## Checklist for New Slides

- [ ] Matches color palette exactly
- [ ] Uses correct typography sizes and weights
- [ ] Includes appropriate animations with correct timing
- [ ] Has hover effects on interactive elements
- [ ] Uses responsive units (vw/vh) for sizing
- [ ] Follows the structure of the reference template
- [ ] Maintains consistent spacing and padding
- [ ] Includes transitions (0.3s ease) on interactive elements
- [ ] Background and border styles match existing slides
- [ ] Any charts/graphs follow existing configuration patterns

## JavaScript Guidelines

If the slide requires JavaScript:
1. Use the same libraries (Chart.js 3.9.1 or Plotly latest)
2. Match chart configurations from existing slides
3. Include console.log statements for debugging
4. Add DOMContentLoaded event listener for initialization
5. Use the same color arrays and styling options

## Testing
After creating a new slide:
1. Verify it displays correctly at different screen sizes
2. Check all animations trigger properly
3. Test any interactive elements
4. Ensure consistency with existing slides 5-13
5. Validate that it works standalone (before navigation is added)
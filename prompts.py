"""
Prompt templates for the Data Blog Generator
"""

NARRATIVE_TEMPLATE = """Given the following data analysis context, suggest {num_ideas} unique narrative approaches for a blog post:

Context: {context}

Requirements:
1. Each narrative should have a clear angle or perspective
2. Focus on engaging storytelling
3. Consider the target audience of data professionals

Output each narrative idea on a new line, starting with a number and a brief title, followed by a one-sentence description.
"""

IMAGE_ANALYSIS_TEMPLATE = """Analyze the following data visualization image and provide key observations:

Image Description: {image_desc}
Image Type: {image_type}

Provide:
1. Main insight from the visualization
2. Key data points or trends
3. Suggested placement in the blog post (introduction, methodology, findings, etc.)
"""

BLOG_STRUCTURE_TEMPLATE = """Create a detailed outline for a data science blog post using the following elements:

Context: {context}
Chosen Narrative: {chosen_narrative}
Image Analyses: {image_analyses}

Create a comprehensive outline with the following sections:
1. Title
2. Introduction
3. Background & Context
4. Methodology
5. Key Findings
6. Analysis & Insights
7. Conclusion

For each section, provide:
- Main points to cover
- Suggested image placements using [IMAGE_X] notation
- Key messages or takeaways
"""

CONTENT_TEMPLATE = """Write a comprehensive data science blog post following this structure:

{blog_structure}

Requirements:
1. Maintain a professional yet engaging tone
2. Include technical details while remaining accessible
3. Integrate images seamlessly using [IMAGE_X] placeholders
4. Add appropriate transitions between sections
5. Include code snippets or technical explanations where relevant

Context: {context}
Narrative Approach: {chosen_narrative}
"""

# System messages for different chains
SYSTEM_MESSAGES = {
    'narrative': "You are a creative data science blog post writer specializing in crafting engaging narratives.",
    'image_analysis': "You are an expert in analyzing data visualizations and extracting meaningful insights.",
    'structure': "You are a professional blog post architect who excels at organizing technical content.",
    'content': "You are an expert data science writer who creates engaging, informative content while maintaining technical accuracy."
}

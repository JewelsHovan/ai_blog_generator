import os
from typing import List, Dict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
import json
from PIL import Image
import io
import base64
import openai
import dotenv
from prompts import (
    NARRATIVE_TEMPLATE,
    IMAGE_ANALYSIS_TEMPLATE,
    BLOG_STRUCTURE_TEMPLATE,
    CONTENT_TEMPLATE,
    SYSTEM_MESSAGES
)

class DataBlogGenerator:
    def __init__(self, openai_api_key: str = None, model_name: str = "openai/gpt-4o-mini"):
        """
        Initialize the Data Blog Generator using LangChain components with OpenRouter
        
        :param openai_api_key: OpenRouter API key
        :param model_name: Model to use (default: openai/gpt-4o-mini)
        """
        # Load environment variables from .env file
        dotenv.load_dotenv()

        if openai_api_key:
            os.environ['OPEN_ROUTER_API_KEY'] = openai_api_key
        elif not os.getenv('OPEN_ROUTER_API_KEY'):
            raise ValueError("OpenRouter API Key must be provided either as argument or in environment variable")
        
        # Configure OpenRouter
        openai.api_base = "https://openrouter.ai/api/v1"
        
        # Initialize ChatOpenAI with OpenRouter
        self.llm = ChatOpenAI(
            model_name=model_name,
            openai_api_base="https://openrouter.ai/api/v1",
            openai_api_key=os.getenv('OPEN_ROUTER_API_KEY'),
            temperature=0.7
        )
        
        # Initialize chain components
        self._setup_chains()
    
    def _setup_chains(self):
        """Setup the LangChain components using LCEL"""
        # Narrative Ideas Chain
        narrative_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=SYSTEM_MESSAGES['narrative']),
            HumanMessagePromptTemplate.from_template(NARRATIVE_TEMPLATE)
        ])
        
        def parse_narrative_ideas(text: str) -> List[str]:
            """Parse narrative ideas from text output"""
            return [idea.strip() for idea in text.split('\n') if idea.strip()]
        
        self.narrative_chain = (
            narrative_prompt 
            | self.llm 
            | StrOutputParser() 
            | RunnableLambda(parse_narrative_ideas)
        )

        # Image Analysis Chain
        image_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=SYSTEM_MESSAGES['image_analysis']),
            HumanMessagePromptTemplate.from_template(IMAGE_ANALYSIS_TEMPLATE)
        ])
        
        self.image_analysis_chain = (
            image_prompt 
            | self.llm 
            | StrOutputParser()
        )

        # Blog Structure Chain
        structure_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=SYSTEM_MESSAGES['structure']),
            HumanMessagePromptTemplate.from_template(BLOG_STRUCTURE_TEMPLATE)
        ])
        
        self.structure_chain = (
            structure_prompt 
            | self.llm 
            | StrOutputParser()
        )

        # Content Generation Chain
        content_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=SYSTEM_MESSAGES['content']),
            HumanMessagePromptTemplate.from_template(CONTENT_TEMPLATE)
        ])
        
        self.content_chain = (
            content_prompt 
            | self.llm 
            | StrOutputParser()
        )

    def _analyze_image(self, image_path: str) -> Dict[str, str]:
        """
        Analyze an image and extract relevant information
        
        :param image_path: Path to the image file
        :return: Dictionary with image analysis results
        """
        # Get image type and basic info
        with Image.open(image_path) as img:
            image_type = img.format
            size = img.size
        
        # Get filename for reference
        image_desc = os.path.basename(image_path)
        
        # Run image analysis chain
        analysis = self.image_analysis_chain.invoke({
            "image_desc": image_desc,
            "image_type": image_type
        })
        
        return {
            'path': image_path,
            'type': image_type,
            'analysis': analysis
        }

    def generate_narrative_ideas(self, context: str, num_ideas: int = 3) -> List[str]:
        """
        Generate potential narrative ideas for the blog post using LangChain
        
        :param context: Background context of the data analysis
        :param num_ideas: Number of narrative ideas to generate
        :return: List of narrative ideas
        """
        return self.narrative_chain.invoke({
            "context": context,
            "num_ideas": num_ideas
        })

    def generate_blog_post(self, context: str, image_paths: List[str], chosen_narrative: str) -> Dict[str, str]:
        """
        Generate a blog post using a sequence of LangChain chains
        
        :param context: Background context of the data analysis
        :param image_paths: List of paths to visualization images
        :param chosen_narrative: The selected narrative approach
        :return: Dictionary with blog post sections
        """
        # Step 1: Analyze all images
        image_analyses = [self._analyze_image(img_path) for img_path in image_paths]
        image_analyses_text = "\n".join(f"Image {i+1}: {analysis['analysis']}" 
                                      for i, analysis in enumerate(image_analyses))

        # Step 2: Generate blog structure
        blog_structure = self.structure_chain.invoke({
            "context": context,
            "chosen_narrative": chosen_narrative,
            "image_analyses": image_analyses_text
        })

        # Step 3: Generate full blog content
        blog_content = self.content_chain.invoke({
            "blog_structure": blog_structure,
            "context": context,
            "chosen_narrative": chosen_narrative
        })

        # Parse the blog post
        title = blog_content.split('\n')[0]
        content = '\n'.join(blog_content.split('\n')[1:])

        return {
            'title': title,
            'content': content,
            'full_post': blog_content,
            'structure': blog_structure
        }

    def save_blog_post(self, blog_post: Dict[str, str], output_dir: str = 'blog_posts'):
        """
        Save the generated blog post to a markdown file
        
        :param blog_post: Dictionary containing blog post sections
        :param output_dir: Directory to save the blog post
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename
        filename = f"{blog_post['title'].lower().replace(' ', '_')}.md"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write(blog_post['full_post'])
        
        print(f"Blog post saved to {filepath}")
        return filepath

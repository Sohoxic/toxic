import markdown
import os
import shutil
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import yaml
from jinja2 import Environment, FileSystemLoader
import logging

class StaticSiteGenerator:
    def __init__(self, content_dir="content", output_dir="dist", template_dir="templates"):
         
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.content_dir = Path(content_dir)
        self.output_dir = Path(output_dir)
        self.template_dir = Path(template_dir)
        
        # Create required directories
        self._setup_directories()
        
        # Initialize Jinja2 environment
        self._setup_jinja()
        
        # Configure Markdown parser
        self.md = markdown.Markdown(
            extensions=['meta', 'fenced_code', 'codehilite', 'tables']
        )

    def _setup_directories(self):
        """Create and verify all required directories."""
        try:
            # Create directories if they don't exist -> the exist_ok parameter is used to avoid errors if the directory already exists
            self.content_dir.mkdir(exist_ok=True)
            self.output_dir.mkdir(exist_ok=True)
            self.template_dir.mkdir(exist_ok=True)
            
            self.logger.info(f"Content directory: {self.content_dir.absolute()}")
            self.logger.info(f"Output directory: {self.output_dir.absolute()}")
            self.logger.info(f"Template directory: {self.template_dir.absolute()}")
        except Exception as e:
            self.logger.error(f"Error setting up directories: {str(e)}")
            raise

    def _setup_jinja(self):
        """Initializing Jinja2 environment and verifying template existence."""
        try:
            self.env = Environment(loader=FileSystemLoader(str(self.template_dir)))
            
            # Create default template if it doesn't exist
            default_template = self.template_dir / 'default.html'
            if not default_template.exists():
                self.logger.info("Creating default template...")
                self._create_default_template()
        except Exception as e:
            self.logger.error(f"Error setting up Jinja2: {str(e)}")
            raise

    def _create_default_template(self):
        """Create a default template if none exists."""
        default_template = """
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>{{ title }}</title>
                    </head>
                    <body>
                        <header>
                            <h1>{{ title }}</h1>
                        </header>
                        <main>
                            {{ content | safe }}
                        </main>
                        <footer>
                            <p>&copy; 2024 Your Site</p>
                        </footer>
                    </body>
                    </html>
                """
        template_path = self.template_dir / 'default.html'
        template_path.write_text(default_template.strip())
        self.logger.info(f"Created default template at {template_path}")

    def parse_markdown(self, content):
        """Parse markdown content and extract metadata."""
        try:
            if content.startswith('---'):
                parts = content.split('---', 2)[1:]
                # print(parts[0])
                frontmatter = yaml.safe_load(parts[0])
                markdown_content = parts[1]
            else:
                frontmatter = {}
                markdown_content = content
                
            html_content = self.md.convert(markdown_content)
            return frontmatter, html_content
        except Exception as e:
            self.logger.error(f"Error parsing markdown: {str(e)}")
            raise

    def process_file(self, file_path):
        """Process a single markdown file."""
        try:
            self.logger.info(f"Processing {file_path}")
            
            # Read markdown content
            content = file_path.read_text(encoding='utf-8')
            
            # Parse markdown and get metadata
            frontmatter, html_content = self.parse_markdown(content)
            
            # Get template
            template_name = frontmatter.get('template', 'default.html')
            # print(template_name)
            template = self.env.get_template(template_name)
            
            # Create context dictionary for template rendering
            context = {
                'content': html_content,
                **frontmatter  # Include all frontmatter variables
            }
            
            # Render HTML
            output = template.render(**context)
            
            # Create output path
            rel_path = file_path.relative_to(self.content_dir)
            output_path = self.output_dir / rel_path.with_suffix('.html')
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write output
            output_path.write_text(output, encoding='utf-8')
            
            self.logger.info(f"Successfully generated {output_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error processing {file_path}: {str(e)}")
            return False

    def copy_assets(self):
        """Copy static assets to output directory."""
        assets_dir = Path('assets')
        if assets_dir.exists():
            output_assets = self.output_dir / 'assets'
            shutil.copytree(assets_dir, output_assets, dirs_exist_ok=True)
            self.logger.info("Copied assets to output directory")

    def build(self):
        """Build the entire site."""
        start_time = time.time()
        
        # Check if content directory is empty
        md_files = list(self.content_dir.rglob('*.md'))
        if not md_files:
            self.logger.warning("No markdown files found. Creating sample content...")
            self._create_sample_content()
            md_files = list(self.content_dir.rglob('*.md'))
        
        self.logger.info(f"Found {len(md_files)} markdown files")
        
        # Process files in parallel
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(self.process_file, md_files))
        
        # Copy assets
        self.copy_assets()
        
        # Print build statistics
        success_count = sum(results)
        total_time = time.time() - start_time
        self.logger.info(f"Built {success_count}/{len(md_files)} files in {total_time:.2f} seconds")

    def _create_sample_content(self):
        """Create a sample markdown file if no content exists."""
        sample_content = """---
title: Welcome to Your New Site
template: default.html
---

# Welcome to Your Static Site

This is a sample page generated automatically. You can:

1. Add more markdown files to the `content` directory
2. Modify the templates in the `templates` directory
3. Add CSS and other assets to the `assets` directory

## Next Steps

1. Create your first post
2. Customize the template
3. Add some styling
"""
        sample_file = self.content_dir / 'index.md'
        sample_file.write_text(sample_content)
        self.logger.info(f"Created sample content at {sample_file}")

if __name__ == '__main__':
    generator = StaticSiteGenerator()
    generator.build()
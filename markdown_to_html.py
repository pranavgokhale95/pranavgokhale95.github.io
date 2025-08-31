#!/usr/bin/env python3
"""
Markdown to Static HTML Website Generator
Converts markdown files to a clean, modern blog website
"""

import os
import re
import markdown
from datetime import datetime
from pathlib import Path
import math

class MarkdownToHTML:
    def __init__(self):
        self.posts = []
        self.tags = {}
        
    def calculate_reading_time(self, text):
        """Calculate estimated reading time (average 200 words per minute)"""
        words = len(text.split())
        minutes = math.ceil(words / 200)
        return minutes
        
    def extract_metadata(self, content):
        """Extract metadata from markdown front matter"""
        metadata = {}
        lines = content.split('\n')
        
        if lines and lines[0].startswith('---'):
            i = 1
            while i < len(lines) and not lines[i].startswith('---'):
                if ':' in lines[i]:
                    key, value = lines[i].split(':', 1)
                    metadata[key.strip()] = value.strip()
                i += 1
            content = '\n'.join(lines[i+1:])
            
        return metadata, content
        
    def fix_image_paths(self, html_content):
        """Fix image paths from Jekyll syntax to relative paths"""
        # Replace Jekyll image syntax with relative paths
        # {{ site.image-dir }}/image.jpg -> ../assets/images/image.jpg
        html_content = html_content.replace('{{ site.image-dir }}', '../assets/images')
        
        # Also handle other common Jekyll image patterns
        html_content = html_content.replace('{{ site.baseurl }}/assets/images', '../assets/images')
        html_content = html_content.replace('{{ site.url }}/assets/images', '../assets/images')
        
        return html_content
        
    def process_posts(self):
        """Process all markdown files in _posts directory"""
        posts_dir = Path('_posts')
        if not posts_dir.exists():
            print("_posts directory not found!")
            return
            
        for md_file in posts_dir.glob('*.markdown'):
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            metadata, markdown_content = self.extract_metadata(content)
            
            # Generate filename
            filename = md_file.stem
            html_filename = f"{filename}.html"
            
            # Convert markdown to HTML
            html_content = markdown.markdown(markdown_content, extensions=['codehilite', 'tables'])
            
            # Fix image paths - convert Jekyll syntax to relative paths
            html_content = self.fix_image_paths(html_content)
            
            # Calculate reading time
            reading_time = self.calculate_reading_time(markdown_content)
            
            # Extract tags - handle posts without tags gracefully
            tags = metadata.get('tags', '').split(',') if metadata.get('tags') else []
            if not tags and metadata.get('category'):
                # Use category as a tag if no tags are specified
                tags = [metadata.get('category', 'general')]
            elif not tags:
                tags = ['general']
            tags = [tag.strip() for tag in tags if tag.strip()]
            
            post_data = {
                'title': metadata.get('title', filename),
                'date': metadata.get('date', ''),
                'tags': tags,
                'content': html_content,
                'filename': html_filename,
                'reading_time': reading_time,
                'slug': filename
            }
            
            self.posts.append(post_data)
            
            # Organize by tags
            for tag in tags:
                if tag not in self.tags:
                    self.tags[tag] = []
                self.tags[tag].append(post_data)
                
        # Sort posts by date
        self.posts.sort(key=lambda x: x.get('date', ''), reverse=True)
        
    def generate_post_html(self, post):
        """Generate individual post HTML"""
        post_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{post['title']}</title>
    <link rel="stylesheet" href="../style.css">
</head>
<body>
    <div class="container">
        <header class="post-header">
            <h1>{post['title']}</h1>
            <div class="post-meta">
                <span class="date">{post['date']}</span>
                <span class="reading-time">📖 {post['reading_time']} min read</span>
            </div>
            <div class="tags">
                {''.join([f'<span class="tag">{tag}</span>' for tag in post['tags']])}
            </div>
        </header>
        
        <main class="post-content">
            {post['content']}
        </main>
        
        <footer class="post-footer">
            <a href="../index.html" class="back-link">← Back to Posts</a>
        </footer>
    </div>
</body>
</html>"""
        
        return post_template
        
    def generate_index_html(self):
        """Generate main index.html page"""
        # Generate tag-organized post list
        tag_sections = ""
        for tag, posts in self.tags.items():
            tag_sections += f"""
            <div class="tag-section">
                <h3 class="tag-header">{tag}</h3>
                <div class="posts-list">
                    {''.join([f'''
                    <article class="post-preview">
                        <h4><a href="posts_output/{post['filename']}">{post['title']}</a></h4>
                        <div class="post-meta">
                            <span class="date">{post['date']}</span>
                            <span class="reading-time">📖 {post['reading_time']} min read</span>
                        </div>
                        <div class="tags">
                            {''.join([f'<span class="tag">{tag}</span>' for tag in post['tags']])}
                        </div>
                    </article>
                    ''' for post in posts])}
                </div>
            </div>"""
            
        index_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pranav's Blog</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header class="main-header">
            <h1>Pranav's Blog</h1>
            <nav>
                <a href="index.html" class="active">Posts</a>
                <a href="about.html">About</a>
            </nav>
        </header>
        
        <main class="main-content">
            <aside class="sidebar">
                <h2>Posts by Tags</h2>
                {tag_sections}
            </aside>
            
            <section class="content-area">
                <h2>Recent Posts</h2>
                <div class="recent-posts">
                    {''.join([f'''
                    <article class="post-preview featured">
                        <h3><a href="posts_output/{post['filename']}">{post['title']}</a></h3>
                        <div class="post-meta">
                            <span class="date">{post['date']}</span>
                            <span class="reading-time">📖 {post['reading_time']} min read</span>
                        </div>
                        <div class="tags">
                            {''.join([f'<span class="tag">{tag}</span>' for tag in post['tags']])}
                        </div>
                    </article>
                    ''' for post in self.posts[:5]])}
                </div>
            </section>
        </main>
    </div>
</body>
</html>"""
        
        return index_template
        
    def generate_about_html(self):
        """Generate about.html page"""
        about_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header class="main-header">
            <h1>About</h1>
            <nav>
                <a href="index.html">Posts</a>
                <a href="about.html" class="active">About</a>
            </nav>
        </header>
        
        <main class="about-content">
            <div class="about-text">
                <h2>About Me</h2>
                <p>This is the about page. You can edit the about.markdown file to customize this content.</p>
            </div>
        </main>
    </div>
</body>
</html>"""
        
        return about_template
        
    def generate_website(self):
        """Generate the complete website"""
        print("Processing markdown files...")
        self.process_posts()
        
        if not self.posts:
            print("No posts found!")
            return
            
        # Create output directories
        os.makedirs('posts_output', exist_ok=True)
        
        # Generate individual post pages
        print("Generating post pages...")
        for post in self.posts:
            post_html = self.generate_post_html(post)
            with open(f"posts_output/{post['filename']}", 'w', encoding='utf-8') as f:
                f.write(post_html)
            print(f"Generated: posts_output/{post['filename']}")
            
        # Generate main index.html
        print("Generating index.html...")
        index_html = self.generate_index_html()
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(index_html)
        print("Generated: index.html")
        
        # Generate about.html
        print("Generating about.html...")
        about_html = self.generate_about_html()
        with open('about.html', 'w', encoding='utf-8') as f:
            f.write(about_html)
        print("Generated: about.html")
        
        print("Website generation complete!")

if __name__ == "__main__":
    generator = MarkdownToHTML()
    generator.generate_website()

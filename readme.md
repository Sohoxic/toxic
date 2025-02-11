# toxic

Welcome to `toxic` by Sohoxic, a fast and lightweight static site generator that converts markdown files into a beautifully styled dark theme website. Built with Python, `toxic` transforms your markdown content into beautifully styled websites with minimal effort.

## Key Features

Here's what makes Toxic special:

* **Dark Theme First**: Carefully crafted dark color scheme that reduces eye strain 😜
* **Lightning Fast**: Built with Python for optimal performance (supports parallel processing of md files)
* **Smart Defaults**: Pre-configured with Roboto Mono for excellent readability.
* **Responsive design**
* **Quick rebuild times**
* **Code syntax highlighting**
* **YAML frontmatter support**

> The best static site generator is the one that stays out of your way while making your content shine. `toxic` does exactly that, with style.

## Why Choose `toxic`?

`toxic` was born from the need for a lightweight, fast, and aesthetically pleasing static site generator that prioritizes dark theme design. Its architecture and thoughtful defaults make it perfect for developers who want to focus on content rather than configuration.

### Technical Foundation

```python
def generate_site():
    """
    Core function that powers `toxic`'s site generation
    """
    process_markdown()
    apply_dark_theme()
    optimize_assets()
    return "Beautiful dark-themed site"
```

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone this repository or download the files:
```bash
git clone <your-repository-url>
cd <project-directory>
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
your-site/
├── toxic.py          # The static site generator script
├── content/             # Your markdown files go here
├── templates/           # HTML templates
├── assets/             # Static assets (CSS, images, etc.)
│   └── css/
│       └── style.css
└── dist/               # Generated site (output directory)
```

## Usage

### 1. Create a New Post

Create a markdown file in the `content` directory with YAML frontmatter:

```markdown
---
title: My First Post
template: default.html
---

# Welcome to My Blog

This is my first blog post.
```

### 2. Build the Site

Run the generator:
```bash
python toxic.py
```

### 3. View Your Site

Open `dist/your-post.html` in a web browser to see your generated page.

## Customization

### Modifying the Theme

The dark theme CSS is located in `assets/css/style.css`. You can modify:
- Colors (using CSS variables at the top)
- Typography
- Spacing
- Layout

### Template Customization

Modify `templates/default.html` to change the HTML structure.

> `toxic` gives you the power to create without getting in your way. It's the static site generator that developers have been waiting for.


## Deployment

### GitHub Pages

1. Create a new repository on GitHub
2. Push your code:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```
3. Enable GitHub Pages in repository settings
4. Set the source to the `dist` directory

### Netlify

1. Create a `netlify.toml`:
```toml
[build]
  publish = "dist"
  command = "python generator.py"
```
2. Connect your repository to Netlify
3. Deploy!

### Vercel

1. Create a `vercel.json`:
```json
{
  "buildCommand": "python generator.py",
  "outputDirectory": "dist"
}
```
2. Connect your repository to Vercel
3. Deploy!

> Remember, `toxic` is more than just a static site generator - it's a complete solution for developers who appreciate the elegance of dark themes and the power of simplicity.

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - feel free to use this in your own projects!